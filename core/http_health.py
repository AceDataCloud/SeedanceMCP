"""Bounded, read-only readiness for the hosted OAuth revocation dependency."""

import asyncio
import os

from redis.asyncio import Redis

READINESS_TIMEOUT_SECONDS = 0.75


class OAuthReadinessProbe:
    """Check Redis availability without changing authentication or OAuth state.

    Liveness remains process-only. A failed readiness check must not make an
    authenticated request pass when its revocation store is unavailable.
    """

    def __init__(self) -> None:
        self._required = bool(os.getenv("MCP_SERVER_URL"))
        url = os.getenv("MCP_OAUTH_REDIS_URL", "")
        self._client: Redis | None = (
            Redis.from_url(
                url,
                password=os.getenv("MCP_OAUTH_REDIS_PASSWORD") or None,
                socket_connect_timeout=READINESS_TIMEOUT_SECONDS,
                socket_timeout=READINESS_TIMEOUT_SECONDS,
                retry_on_timeout=False,
            )
            if url
            else None
        )

    async def ready(self) -> bool:
        if self._client is None:
            return not self._required
        try:
            return bool(
                await asyncio.wait_for(self._client.ping(), timeout=READINESS_TIMEOUT_SECONDS)
            )
        except Exception:
            # Public readiness never exposes the store address, password or error.
            return False

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
