"""Video generation tools for Seedance API."""

import re
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_DURATION,
    DEFAULT_MODEL,
    DEFAULT_RATIO,
    DEFAULT_RESOLUTION,
    AspectRatio,
    OmniReferenceTaskType,
    OutputFormat,
    Resolution,
    SeedanceModel,
    SeedanceWebSearchTool,
)
from core.utils import format_video_result


def _generation_controls(
    prompt: str,
    *,
    resolution: Resolution | None,
    ratio: AspectRatio | None,
    duration: int | None,
    frames: int | None,
    seed: int | None,
    camera_fixed: bool | None,
    watermark: bool | None,
    default_ratio: AspectRatio = DEFAULT_RATIO,
) -> dict[str, Any]:
    """Only apply defaults when neither a named nor an inline option is set."""
    inline = {name.lower() for name in re.findall(r"--(\w+)(?:\s+|=)", prompt)}
    values: dict[str, Any] = {}
    for key, value, default, aliases in (
        ("resolution", resolution, DEFAULT_RESOLUTION, {"rs", "resolution"}),
        ("ratio", ratio, default_ratio, {"rt", "ratio"}),
        ("camerafixed", camera_fixed, False, {"cf", "camerafixed"}),
        ("watermark", watermark, False, {"wm", "watermark"}),
    ):
        if value is not None:
            values[key] = value
        elif not inline.intersection(aliases):
            values[key] = default
    if frames is not None:
        values["frames"] = frames
    elif duration is not None:
        values["duration"] = duration
    elif not inline.intersection({"frames", "dur", "duration"}):
        values["duration"] = DEFAULT_DURATION
    if seed is not None:
        values["seed"] = seed
    return values


@mcp.tool()
async def seedance_generate_video(
    prompt: Annotated[
        str,
        Field(
            description=(
                "Description of the video to generate. Max 1000 characters. "
                "Be descriptive about the scene, motion, style, and mood. "
                "You can also include inline parameters like "
                "'--rs 720p --rt 16:9 --dur 5'. "
                "Examples: 'A cat walking through a garden with butterflies', "
                "'Cinematic aerial shot of mountains at sunset'"
            )
        ),
    ],
    model: Annotated[
        SeedanceModel,
        Field(
            description=(
                "Model version to use. Options: "
                "'doubao-seedance-2-5-260628' (latest flagship, up to 30 seconds, "
                "multimodal reference, edit/extend), "
                "'doubao-seedance-2-0-260128' (default, highest resolution, supports 4k), "
                "'doubao-seedance-2-0-fast-260128' (latest generation, faster, up to 720p), "
                "'doubao-seedance-2-0-mini-260615' (latest generation, lightweight, "
                "cheapest within the 2.0 series, up to 720p), "
                "'doubao-seedance-1-5-pro-251215' (1.5 flagship, supports audio), "
                "'doubao-seedance-1-0-pro-250528' (1.0 standard), "
                "'doubao-seedance-1-0-pro-fast-251015' (1.0 fast, cost-optimized), "
                "'doubao-seedance-1-0-lite-t2v-250428' (lightweight text-to-video), "
                "'doubao-seedance-1-0-lite-i2v-250428' (lightweight image-to-video)."
            )
        ),
    ] = DEFAULT_MODEL,
    resolution: Annotated[
        Resolution | None,
        Field(
            description=(
                "Video resolution. Options: '480p', '720p' (default), '1080p', '4k'. "
                "'4k' is supported only by 'doubao-seedance-2-0-260128'; "
                "'2-5' maxes out at '1080p'; '2-0-fast' and '2-0-mini' max out at '720p'."
            )
        ),
    ] = None,
    ratio: Annotated[
        AspectRatio | None,
        Field(
            description=(
                "Video aspect ratio. Options: '16:9' (landscape, default), "
                "'9:16' (portrait), '1:1' (square), '4:3', '3:4', "
                "'21:9' (ultrawide), 'adaptive'."
            )
        ),
    ] = None,
    duration: Annotated[
        int | None,
        Field(
            description=(
                "Video duration in seconds. 1.0 series: 2–12; 1.5 Pro: 4–12; "
                "2.0 series: 4–15; 2.5: 4–30. Use -1 for auto-duration (1.5 Pro and 2.x). "
                "Default is 5. Mutually exclusive with 'frames'."
            ),
            ge=-1,
            le=30,
        ),
    ] = None,
    frames: Annotated[
        int | None,
        Field(
            description=(
                "Frame count for the generated video (1.0 series only). "
                "Must satisfy 25+4n (e.g. 29, 33, 37, ..., 289). "
                "Mutually exclusive with 'duration'."
            ),
            ge=29,
            le=289,
        ),
    ] = None,
    generate_audio: Annotated[
        bool,
        Field(
            description=(
                "If true, generate audio along with the video. "
                "Supported by 'doubao-seedance-1-5-pro-251215' and the Seedance 2.x series. "
                "Pricing depends on the model and output settings. Default is false."
            )
        ),
    ] = False,
    seed: Annotated[
        int | None,
        Field(
            description=(
                "Random seed for reproducible generation. "
                "Range: -1 to 4294967295. Use -1 for random. Default is -1."
            ),
            ge=-1,
            le=4294967295,
        ),
    ] = None,
    camera_fixed: Annotated[
        bool | None,
        Field(description=("If true, keep the camera fixed. Defaults to false unless set inline.")),
    ] = None,
    watermark: Annotated[
        bool | None,
        Field(description="If true, add a watermark. Defaults to false unless set inline."),
    ] = None,
    return_last_frame: Annotated[
        bool,
        Field(
            description=(
                "If true, also return the last frame of the generated video "
                "as an image URL. Useful for video extension workflows. "
                "Default is false."
            )
        ),
    ] = False,
    output_format: Annotated[
        OutputFormat | None,
        Field(description="Seedance 2.5 output format: mp4 or mov."),
    ] = None,
    tools: Annotated[
        list[SeedanceWebSearchTool] | None,
        Field(
            description="Optional Seedance 2.5 web search tool configuration.",
            max_length=1,
        ),
    ] = None,
    priority: Annotated[
        int,
        Field(description="Seedance 2.5 task priority from 0 to 9.", ge=0, le=9),
    ] = 0,
    safety_identifier: Annotated[
        str | None,
        Field(
            description="Stable anonymous end-user identifier. Do not use personal information.",
            max_length=64,
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description=(
                "Webhook callback URL for asynchronous notifications. "
                "When provided, the API returns immediately with a task_id "
                "and calls this URL when the video is generated."
            )
        ),
    ] = None,
    execution_expires_after: Annotated[
        int,
        Field(
            description=("Task timeout threshold in seconds. Default is 172800 (48 hours)."),
            ge=3600,
            le=259200,
        ),
    ] = 172800,
) -> str:
    """Generate AI video from a text prompt using ByteDance Seedance.

    This is the simplest way to create video - just describe what you want and
    Seedance will generate a high-quality AI video.

    Use this when:
    - You want to create a video from a text description
    - You don't have reference images
    - You want quick text-to-video generation

    For using reference images (first/last frame, reference), use
    seedance_generate_video_from_image instead.

    Returns:
        Task ID and generated video information including URLs and metadata.
    """
    if frames is not None and duration is not None:
        return "Error: 'frames' and 'duration' are mutually exclusive. Provide only one."

    payload: dict[str, Any] = {
        "model": model,
        "content": [{"type": "text", "text": prompt}],
        "return_last_frame": return_last_frame,
        "execution_expires_after": execution_expires_after,
        "priority": priority,
    }

    payload.update(
        _generation_controls(
            prompt,
            resolution=resolution,
            ratio=ratio,
            duration=duration,
            frames=frames,
            seed=seed,
            camera_fixed=camera_fixed,
            watermark=watermark,
        )
    )

    if generate_audio:
        payload["generate_audio"] = True

    if output_format:
        payload["output_format"] = output_format

    if tools:
        payload["tools"] = [
            tool.model_dump(exclude_none=True) if isinstance(tool, SeedanceWebSearchTool) else tool
            for tool in tools
        ]

    if safety_identifier:
        payload["safety_identifier"] = safety_identifier
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def seedance_generate_video_from_image(
    prompt: Annotated[
        str,
        Field(
            description=(
                "Description of the video motion and content. "
                "Describe what should happen in the video, "
                "how objects should move, what transitions to include."
            )
        ),
    ],
    first_frame_url: Annotated[
        str,
        Field(
            description=(
                "URL of the image to use as the first frame of the video. "
                "The video will animate from this image. "
                "Supports https:// URLs or base64 data:image/... URIs."
            )
        ),
    ] = "",
    last_frame_url: Annotated[
        str,
        Field(
            description=(
                "URL of the image to use as the last frame of the video. "
                "The video will animate towards this image. "
                "Supports https:// URLs or base64 data:image/... URIs."
            )
        ),
    ] = "",
    reference_image_urls: Annotated[
        list[str],
        Field(
            description=(
                "List of reference image URLs for style/content guidance. "
                "Subject or style references: up to 9 images for Seedance 2.0 or "
                "30 for Seedance 2.5. "
                "These images influence the look but are not used as frames. "
                "Cannot be combined with first_frame_url or last_frame_url."
            )
        ),
    ] = [],  # noqa: B006
    reference_audio_urls: Annotated[
        list[str],
        Field(
            description=(
                "Reference audio for voice timbre or music: up to 3 for Seedance 2.0 "
                "with image/video input, or 10 for 2.5 (also supports audio-only reference). "
                "Not supported by 1.x models. Combined 2.5 media limit: 50."
            )
        ),
    ] = [],  # noqa: B006
    reference_video_urls: Annotated[
        list[str],
        Field(
            description=(
                "Reference videos for subject, camera, motion or style: up to 3 for "
                "Seedance 2.0 or 10 for 2.5. Not supported by 1.x models. "
                "Combined 2.5 media limit: 50."
            )
        ),
    ] = [],  # noqa: B006
    model: Annotated[
        SeedanceModel,
        Field(
            description=(
                "Model version to use. "
                "Use 'doubao-seedance-2-0-260128' (default) for latest-generation quality "
                "and multimodal reference, 'doubao-seedance-2-0-fast-260128' or "
                "'doubao-seedance-2-0-mini-260615' for faster/cheaper 2.0, or a 1.x model "
                "such as 'doubao-seedance-1-0-lite-i2v-250428' for lightweight I2V."
            )
        ),
    ] = DEFAULT_MODEL,
    resolution: Annotated[
        Resolution | None,
        Field(
            description=(
                "Video resolution. Options: '480p', '720p', '1080p', '4k'. "
                "'4k' is supported only by 'doubao-seedance-2-0-260128'; "
                "'2-5' maxes out at '1080p'; '2-0-fast' and '2-0-mini' max out at '720p'."
            )
        ),
    ] = None,
    ratio: Annotated[
        AspectRatio | None,
        Field(description=("Video aspect ratio. Use 'adaptive' to match your input image ratio.")),
    ] = None,
    duration: Annotated[
        int | None,
        Field(
            description=(
                "Video duration in seconds. 1.0 series: 2–12; 1.5 Pro: 4–12; "
                "2.0 series: 4–15; 2.5: 4–30. Use -1 for auto-duration (1.5 Pro and 2.x). "
                "Default is 5. Mutually exclusive with 'frames'."
            ),
            ge=-1,
            le=30,
        ),
    ] = None,
    frames: Annotated[
        int | None,
        Field(
            description=(
                "Frame count for the generated video (1.0 series only). "
                "Must satisfy 25+4n (e.g. 29, 33, 37, ..., 289). "
                "Mutually exclusive with 'duration'."
            ),
            ge=29,
            le=289,
        ),
    ] = None,
    generate_audio: Annotated[
        bool,
        Field(
            description=(
                "If true, generate audio. Supported by 'doubao-seedance-1-5-pro-251215' "
                "and the Seedance 2.x series. Default is false."
            )
        ),
    ] = False,
    seed: Annotated[
        int | None,
        Field(
            description="Random seed. -1 for random. Default is -1.",
            ge=-1,
            le=4294967295,
        ),
    ] = None,
    camera_fixed: Annotated[
        bool | None,
        Field(description="Keep the camera fixed. Defaults to false unless set inline."),
    ] = None,
    watermark: Annotated[
        bool | None,
        Field(description="Add a watermark. Defaults to false unless set inline."),
    ] = None,
    return_last_frame: Annotated[
        bool,
        Field(
            description=("If true, return the last frame of the generated video. Default is false.")
        ),
    ] = False,
    omni_reference_task_type: Annotated[
        OmniReferenceTaskType | None,
        Field(description="Seedance 2.5 task type: auto, reference, edit, or extend."),
    ] = None,
    output_format: Annotated[
        OutputFormat | None,
        Field(description="Seedance 2.5 output format: mp4 or mov."),
    ] = None,
    tools: Annotated[
        list[SeedanceWebSearchTool] | None,
        Field(
            description="Optional Seedance 2.5 web search tool configuration.",
            max_length=1,
        ),
    ] = None,
    priority: Annotated[
        int,
        Field(description="Seedance 2.5 task priority from 0 to 9.", ge=0, le=9),
    ] = 0,
    safety_identifier: Annotated[
        str | None,
        Field(
            description="Stable anonymous end-user identifier. Do not use personal information.",
            max_length=64,
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
    execution_expires_after: Annotated[
        int,
        Field(
            description=("Task timeout threshold in seconds. Default is 172800 (48 hours)."),
            ge=3600,
            le=259200,
        ),
    ] = 172800,
) -> str:
    """Generate AI video using reference images with ByteDance Seedance.

    This allows you to control the video by specifying first frame, last frame,
    or reference images. Seedance will generate smooth motion based on the inputs.

    Use this when:
    - You have a specific image you want to animate
    - You want to create a video transition between two images
    - You need style guidance from reference images
    - You need precise control over the video's visual content

    Note: reference_image_urls cannot be combined with first_frame_url/last_frame_url.
    At least one image, video, or audio reference must be provided.
    Seedance 2.5 first/last-frame mode requires ratio=adaptive; it is selected when omitted.

    Returns:
        Task ID and generated video information including URLs and metadata.
    """
    if (
        not first_frame_url
        and not last_frame_url
        and not reference_image_urls
        and not reference_audio_urls
        and not reference_video_urls
    ):
        return (
            "Error: At least one of first_frame_url, last_frame_url, "
            "reference_image_urls, reference_audio_urls, or reference_video_urls "
            "must be provided."
        )

    if reference_image_urls and (first_frame_url or last_frame_url):
        return (
            "Error: reference_image_urls cannot be combined with first_frame_url or last_frame_url."
        )

    if frames is not None and duration is not None:
        return "Error: 'frames' and 'duration' are mutually exclusive. Provide only one."

    # Build content array
    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]

    if first_frame_url:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": first_frame_url},
                "role": "first_frame",
            }
        )

    if last_frame_url:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": last_frame_url},
                "role": "last_frame",
            }
        )

    for ref_url in reference_image_urls:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": ref_url},
                "role": "reference_image",
            }
        )

    for audio_url in reference_audio_urls:
        content.append(
            {"type": "audio_url", "audio_url": {"url": audio_url}, "role": "reference_audio"}
        )

    for video_url in reference_video_urls:
        content.append(
            {"type": "video_url", "video_url": {"url": video_url}, "role": "reference_video"}
        )

    payload: dict[str, Any] = {
        "model": model,
        "content": content,
        "return_last_frame": return_last_frame,
        "execution_expires_after": execution_expires_after,
        "priority": priority,
    }

    payload.update(
        _generation_controls(
            prompt,
            resolution=resolution,
            ratio=ratio,
            duration=duration,
            frames=frames,
            seed=seed,
            camera_fixed=camera_fixed,
            watermark=watermark,
            default_ratio=(
                "adaptive"
                if model == "doubao-seedance-2-5-260628" and (first_frame_url or last_frame_url)
                else DEFAULT_RATIO
            ),
        )
    )

    if generate_audio:
        payload["generate_audio"] = True

    if omni_reference_task_type:
        payload["omni_reference_task_type"] = omni_reference_task_type

    if output_format:
        payload["output_format"] = output_format

    if tools:
        payload["tools"] = [
            tool.model_dump(exclude_none=True) if isinstance(tool, SeedanceWebSearchTool) else tool
            for tool in tools
        ]

    if safety_identifier:
        payload["safety_identifier"] = safety_identifier
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
