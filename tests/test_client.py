"""Unit tests for HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.client import SeedanceClient
from core.exceptions import SeedanceAPIError, SeedanceAuthError, SeedanceTimeoutError


@pytest.fixture
def test_client() -> SeedanceClient:
    """Create a client instance for testing."""
    return SeedanceClient(api_token="test-token", base_url="https://api.test.com")


class TestSeedanceClient:
    """Tests for SeedanceClient class."""

    def test_init_with_params(self) -> None:
        """Test client initialization with explicit parameters."""
        c = SeedanceClient(api_token="my-token", base_url="https://custom.api.com")
        assert c.api_token == "my-token"
        assert c.base_url == "https://custom.api.com"

    def test_get_headers(self, test_client: SeedanceClient) -> None:
        """Test that headers are correctly generated."""
        headers = test_client._get_headers()
        assert headers["accept"] == "application/json"
        assert headers["authorization"] == "Bearer test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self) -> None:
        """Test that missing token raises auth error."""
        c = SeedanceClient(api_token="", base_url="https://api.test.com")
        with pytest.raises(SeedanceAuthError, match="not configured"):
            c._get_headers()

    def test_with_async_callback_injects_default_callback(
        self, test_client: SeedanceClient
    ) -> None:
        """Test async submission injects an internal callback when missing."""
        payload = test_client._with_async_callback({"model": "doubao-seedance-1-0-pro-250528"})
        assert payload["callback_url"] == "https://api.acedata.cloud/health"

    def test_with_async_callback_preserves_explicit_callback(
        self, test_client: SeedanceClient
    ) -> None:
        """Test async submission preserves a user-provided callback."""
        payload = test_client._with_async_callback(
            {
                "model": "doubao-seedance-1-0-pro-250528",
                "callback_url": "https://example.com/webhook",
            }
        )
        assert payload["callback_url"] == "https://example.com/webhook"

    @pytest.mark.asyncio
    async def test_request_success(
        self,
        test_client: SeedanceClient,
        mock_video_response: dict,
    ) -> None:
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_video_response

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            result = await test_client.request(
                "/seedance/videos",
                {"model": "doubao-seedance-1-0-pro-250528"},
            )
            assert result == mock_video_response

    @pytest.mark.asyncio
    async def test_request_auth_error_401(self, test_client: SeedanceClient) -> None:
        """Test 401 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"code": "unauthorized", "message": "Invalid API token"}
        }
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "Invalid API token"

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(SeedanceAuthError, match="Invalid API token"):
                await test_client.request("/seedance/videos", {})

    @pytest.mark.asyncio
    async def test_request_timeout(self, test_client: SeedanceClient) -> None:
        """Test timeout raises timeout error."""
        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(SeedanceTimeoutError, match="timed out"):
                await test_client.request("/seedance/videos", {})

    @pytest.mark.asyncio
    async def test_request_http_error(self, test_client: SeedanceClient) -> None:
        """Test HTTP error raises API error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "error": {"code": "internal_error", "message": "Internal Server Error"}
        }
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "Internal Server Error"

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(SeedanceAPIError, match="Internal Server Error") as exc_info:
                await test_client.request("/seedance/videos", {})

            assert exc_info.value.status_code == 500
