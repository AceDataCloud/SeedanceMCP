"""Unit tests for video generation tools."""

from unittest.mock import AsyncMock, patch

import pytest

from tools.video_tools import seedance_generate_video, seedance_generate_video_from_image


class TestSeedanceGenerateVideo:
    """Tests for seedance_generate_video tool."""

    @pytest.mark.asyncio
    async def test_frames_and_duration_mutually_exclusive(self) -> None:
        """Test that providing both frames and duration (both non-None) returns an error."""
        result = await seedance_generate_video(
            prompt="A test video",
            frames=29,
            duration=10,
        )
        assert "mutually exclusive" in result

    @pytest.mark.asyncio
    async def test_frames_without_duration_is_valid(self, mock_video_response: dict) -> None:
        """Test that providing frames without duration is valid."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            result = await seedance_generate_video(
                prompt="A test video",
                frames=29,
            )
            assert "mutually exclusive" not in result

    @pytest.mark.asyncio
    async def test_frames_parameter_sent_to_api(self, mock_video_response: dict) -> None:
        """Test that frames parameter is sent to the API instead of duration."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video(
                prompt="A test video",
                frames=29,
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["frames"] == 29
            assert "duration" not in call_kwargs

    @pytest.mark.asyncio
    async def test_duration_used_when_frames_not_provided(
        self, mock_video_response: dict
    ) -> None:
        """Test that duration is used when frames is not provided."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video(
                prompt="A test video",
                duration=8,
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["duration"] == 8
            assert "frames" not in call_kwargs

    @pytest.mark.asyncio
    async def test_execution_expires_after_default(self, mock_video_response: dict) -> None:
        """Test that execution_expires_after defaults to 172800."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video(prompt="A test video")
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["execution_expires_after"] == 172800

    @pytest.mark.asyncio
    async def test_execution_expires_after_custom(self, mock_video_response: dict) -> None:
        """Test that custom execution_expires_after is sent to the API."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video(
                prompt="A test video",
                execution_expires_after=3600,
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["execution_expires_after"] == 3600


class TestSeedanceGenerateVideoFromImage:
    """Tests for seedance_generate_video_from_image tool."""

    @pytest.mark.asyncio
    async def test_frames_and_duration_mutually_exclusive(self) -> None:
        """Test that providing both frames and duration (both non-None) returns an error."""
        result = await seedance_generate_video_from_image(
            prompt="A test video",
            first_frame_url="https://example.com/image.jpg",
            frames=29,
            duration=10,
        )
        assert "mutually exclusive" in result

    @pytest.mark.asyncio
    async def test_frames_without_duration_is_valid(self, mock_video_response: dict) -> None:
        """Test that providing frames without duration is valid."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            result = await seedance_generate_video_from_image(
                prompt="A test video",
                first_frame_url="https://example.com/image.jpg",
                frames=29,
            )
            assert "mutually exclusive" not in result

    @pytest.mark.asyncio
    async def test_frames_parameter_sent_to_api(self, mock_video_response: dict) -> None:
        """Test that frames parameter is sent to the API instead of duration."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video_from_image(
                prompt="A test video",
                first_frame_url="https://example.com/image.jpg",
                frames=33,
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["frames"] == 33
            assert "duration" not in call_kwargs

    @pytest.mark.asyncio
    async def test_execution_expires_after_default(self, mock_video_response: dict) -> None:
        """Test that execution_expires_after defaults to 172800."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video_from_image(
                prompt="A test video",
                first_frame_url="https://example.com/image.jpg",
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["execution_expires_after"] == 172800

    @pytest.mark.asyncio
    async def test_execution_expires_after_custom(self, mock_video_response: dict) -> None:
        """Test that custom execution_expires_after is sent to the API."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video_from_image(
                prompt="A test video",
                first_frame_url="https://example.com/image.jpg",
                execution_expires_after=7200,
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["execution_expires_after"] == 7200
