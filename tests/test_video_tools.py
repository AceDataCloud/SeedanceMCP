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
    async def test_duration_used_when_frames_not_provided(self, mock_video_response: dict) -> None:
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
    @pytest.mark.parametrize(
        "model",
        [
            "doubao-seedance-2-5-260628",
            "doubao-seedance-2-0-260128",
            "doubao-seedance-2-0-fast-260128",
        ],
    )
    async def test_new_models_parameter_sent_to_api(
        self, model: str, mock_video_response: dict
    ) -> None:
        """Test that newly added model values are accepted and sent to the API."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video(
                prompt="A test video",
                model=model,
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["model"] == model

    @pytest.mark.asyncio
    async def test_seedance_25_options_sent_to_api(self, mock_video_response: dict) -> None:
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video(
                prompt="A test video",
                model="doubao-seedance-2-5-260628",
                duration=30,
                output_format="mov",
                tools=[
                    {
                        "type": "web_search",
                        "limit": 5,
                        "max_keyword": 3,
                        "sources": ["search_engine"],
                    }
                ],
                priority=9,
                safety_identifier="anonymous-user-123",
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["duration"] == 30
            assert call_kwargs["output_format"] == "mov"
            assert call_kwargs["tools"] == [
                {
                    "type": "web_search",
                    "limit": 5,
                    "max_keyword": 3,
                    "sources": ["search_engine"],
                }
            ]
            assert call_kwargs["priority"] == 9
            assert call_kwargs["safety_identifier"] == "anonymous-user-123"

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
    @pytest.mark.parametrize(
        "model",
        [
            "doubao-seedance-2-5-260628",
            "doubao-seedance-2-0-260128",
            "doubao-seedance-2-0-fast-260128",
        ],
    )
    async def test_new_models_parameter_sent_to_api(
        self, model: str, mock_video_response: dict
    ) -> None:
        """Test that newly added model values are accepted and sent to the API."""
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video_from_image(
                prompt="A test video",
                first_frame_url="https://example.com/image.jpg",
                model=model,
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["model"] == model

    @pytest.mark.asyncio
    async def test_seedance_25_multimodal_roles_and_options(
        self, mock_video_response: dict
    ) -> None:
        with patch("tools.video_tools.client") as mock_client:
            mock_client.generate_video = AsyncMock(return_value=mock_video_response)
            await seedance_generate_video_from_image(
                prompt="Extend the shot",
                reference_video_urls=["https://example.com/video.mp4"],
                reference_audio_urls=["https://example.com/audio.mp3"],
                model="doubao-seedance-2-5-260628",
                ratio="adaptive",
                duration=30,
                omni_reference_task_type="reference",
                output_format="mov",
                tools=[{"type": "web_search"}],
                priority=8,
                safety_identifier="anonymous-user-456",
            )
            call_kwargs = mock_client.generate_video.call_args[1]
            assert call_kwargs["content"][1]["role"] == "reference_audio"
            assert call_kwargs["content"][2]["role"] == "reference_video"
            assert call_kwargs["omni_reference_task_type"] == "reference"
            assert call_kwargs["output_format"] == "mov"
            assert call_kwargs["tools"] == [{"type": "web_search"}]
            assert call_kwargs["priority"] == 8
            assert call_kwargs["safety_identifier"] == "anonymous-user-456"

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


def test_seedance_tools_expose_metered_controls():
    from inspect import signature

    from tools.video_tools import seedance_generate_video

    params = signature(
        seedance_generate_video.fn
        if hasattr(seedance_generate_video, "fn")
        else seedance_generate_video
    ).parameters
    assert "priority" in params
    assert "safety_identifier" in params


@pytest.mark.parametrize("image_mode", [False, True])
async def test_inline_controls_are_not_overridden_by_omitted_arguments(image_mode):
    from core.server import mcp

    name = "seedance_generate_video_from_image" if image_mode else "seedance_generate_video"
    args = {"prompt": "A bird --rs 1080p --rt 9:16 --dur 10 --cf true --wm true --seed 23"}
    if image_mode:
        args["first_frame_url"] = "https://example.com/image.jpg"
    with patch(
        "tools.video_tools.client.generate_video", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await mcp.call_tool(name, args)
    body = call.await_args.kwargs
    assert not {"resolution", "ratio", "duration", "camerafixed", "watermark", "seed"}.intersection(
        body
    )


async def test_named_controls_still_override_inline_values_and_explicit_false():
    from core.server import mcp

    with patch(
        "tools.video_tools.client.generate_video", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await mcp.call_tool(
            "seedance_generate_video",
            {
                "prompt": "A bird --rs 1080p --rt 9:16 --dur 10 --cf true --wm true --seed 23",
                "resolution": "480p",
                "ratio": "1:1",
                "duration": 8,
                "camera_fixed": False,
                "watermark": False,
                "seed": -1,
            },
        )
    body = call.await_args.kwargs
    assert {
        key: body[key]
        for key in ("resolution", "ratio", "duration", "camerafixed", "watermark", "seed")
    } == {
        "resolution": "480p",
        "ratio": "1:1",
        "duration": 8,
        "camerafixed": False,
        "watermark": False,
        "seed": -1,
    }


async def test_inline_frames_do_not_gain_default_duration():
    with patch(
        "tools.video_tools.client.generate_video", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await seedance_generate_video(prompt="A bird --frames 33")
    assert "duration" not in call.await_args.kwargs


async def test_omitted_controls_preserve_defaults_and_seedance_25_frame_ratio():
    with patch(
        "tools.video_tools.client.generate_video", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await seedance_generate_video(prompt="A bird")
        assert call.await_args.kwargs["resolution"] == "720p"
        assert call.await_args.kwargs["ratio"] == "16:9"
        assert call.await_args.kwargs["duration"] == 5
        await seedance_generate_video_from_image(
            prompt="A bird",
            first_frame_url="https://example.com/frame.jpg",
            model="doubao-seedance-2-5-260628",
        )
        assert call.await_args.kwargs["ratio"] == "adaptive"
