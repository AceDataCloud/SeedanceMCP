"""Exercise the actual HTTP app and auth dependency without model/task calls."""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from mcp.server.auth.provider import ProviderTokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from pydantic import AnyHttpUrl
from redis.exceptions import ConnectionError as RedisConnectionError
from starlette.testclient import TestClient

import main
import tools  # noqa: F401
from core import http_health, server
from core.oauth import AceDataCloudOAuthProvider


def http_app(monkeypatch, redis):
    """Use main's unchanged route/middleware assembly and real OAuth verifier."""
    monkeypatch.setenv("MCP_SERVER_URL", "https://seedance.example.test")
    monkeypatch.setenv("MCP_OAUTH_REDIS_URL", "redis://private.invalid:6379/0")
    monkeypatch.setenv("MCP_OAUTH_REDIS_PASSWORD", "private-fixture-password")
    monkeypatch.setattr(http_health.Redis, "from_url", lambda *_a, **_k: redis)
    provider = AceDataCloudOAuthProvider(redis_client=redis, state_key="0" * 64)
    host = FastMCP(
        "seedance-http-regression",
        token_verifier=ProviderTokenVerifier(provider),
        auth=AuthSettings(
            issuer_url=AnyHttpUrl("https://seedance.example.test"),
            resource_server_url=AnyHttpUrl("https://seedance.example.test"),
            required_scopes=["mcp:access"],
            validate_token_resource=False,
        ),
    )
    for tool in server.mcp._tool_manager.list_tools():
        host.add_tool(tool.fn, name=tool.name)
    monkeypatch.setattr(main, "mcp", host)
    monkeypatch.setattr(server, "oauth_provider", None)
    captured = []
    monkeypatch.setattr("uvicorn.run", lambda app, **_kwargs: captured.append(app))
    monkeypatch.setattr(sys, "argv", ["mcp-seedance", "--transport", "http"])
    main.main()
    return captured[0]


def dependency():
    redis = AsyncMock()
    redis.ping.return_value = True
    redis.exists.return_value = 0
    return redis


def message(client, protocol, method, params, identifier=None, token="fixture-key"):
    body = {"jsonrpc": "2.0", "method": method, "params": params}
    if identifier is not None:
        body["id"] = identifier
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
        "MCP-Protocol-Version": protocol,
    }
    if token is not None:
        headers["Authorization"] = "Bearer " + token
    return client.post("/mcp", headers=headers, json=body)


@pytest.mark.parametrize("protocol", ["2025-06-18", "2025-11-25"])
def test_ready_auth_initialize_notification_and_tools_list(monkeypatch, protocol):
    redis = dependency()
    with TestClient(http_app(monkeypatch, redis), base_url="http://127.0.0.1:8000") as client:
        assert client.get("/health").json() == {"status": "ok"}
        assert client.get("/ready").json() == {"status": "ready"}
        response = message(
            client,
            protocol,
            "initialize",
            {
                "protocolVersion": protocol,
                "capabilities": {},
                "clientInfo": {"name": "readiness-test", "version": "1"},
            },
            1,
        )
        assert response.status_code == 200
        assert response.json()["result"]["protocolVersion"] == protocol
        assert message(client, protocol, "notifications/initialized", {}).status_code == 202
        result = message(client, protocol, "tools/list", {}, 2)
        assert result.status_code == 200
        assert len(result.json()["result"]["tools"]) == 7
        assert message(client, protocol, "tools/list", {}, 3, token=None).status_code == 401
        redis.exists.return_value = 1
        assert message(client, protocol, "tools/list", {}, 4).status_code == 401
    redis.aclose.assert_awaited_once()


def test_redis_refusal_withdraws_readiness_without_changing_auth_or_liveness(monkeypatch):
    redis = dependency()
    redis.ping.side_effect = RedisConnectionError("private.invalid private-fixture-password")
    redis.exists.side_effect = RedisConnectionError("private.invalid private-fixture-password")
    with TestClient(
        http_app(monkeypatch, redis),
        base_url="http://127.0.0.1:8000",
        raise_server_exceptions=False,
    ) as client:
        assert client.get("/health").status_code == 200
        ready = client.get("/ready")
        assert ready.status_code == 503
        assert ready.json() == {"status": "unavailable"}
        assert "private" not in ready.text
        # A dependency failure does not bypass the existing revocation check.
        assert message(client, "2025-11-25", "tools/list", {}, 1).status_code == 500
        assert message(client, "2025-11-25", "tools/list", {}, 2, token=None).status_code == 401


@pytest.mark.asyncio
async def test_readiness_timeout_is_bounded_and_does_not_block_event_loop(monkeypatch):
    redis = dependency()
    started = asyncio.Event()

    async def delayed_ping():
        started.set()
        await asyncio.sleep(10)

    redis.ping.side_effect = delayed_ping
    monkeypatch.setenv("MCP_SERVER_URL", "https://seedance.example.test")
    monkeypatch.setenv("MCP_OAUTH_REDIS_URL", "redis://private.invalid:6379")
    monkeypatch.setattr(http_health.Redis, "from_url", lambda *_a, **_k: redis)
    monkeypatch.setattr(http_health, "READINESS_TIMEOUT_SECONDS", 0.02)
    probe = http_health.OAuthReadinessProbe()
    task = asyncio.create_task(probe.ready())
    await started.wait()
    await asyncio.sleep(0)
    assert not task.done()  # another coroutine ran while Redis awaited
    assert await asyncio.wait_for(task, timeout=0.2) is False
    await probe.close()


@pytest.mark.asyncio
async def test_hosted_missing_redis_fails_readiness_and_local_mode_remains_supported(monkeypatch):
    monkeypatch.delenv("MCP_OAUTH_REDIS_URL", raising=False)
    monkeypatch.setenv("MCP_SERVER_URL", "https://seedance.example.test")
    assert await http_health.OAuthReadinessProbe().ready() is False
    monkeypatch.delenv("MCP_SERVER_URL")
    assert await http_health.OAuthReadinessProbe().ready() is True


def test_only_seedance_readiness_probe_changes():
    source = (Path(__file__).parents[1] / "deploy/production/deployment.yaml").read_text()
    assert "livenessProbe:\n            httpGet:\n              path: /health" in source
    assert "readinessProbe:\n            httpGet:\n              path: /ready" in source
    assert "replicas: 2" in source
    assert "failureThreshold: 1" in source
