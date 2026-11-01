"""Informational tools for Seedance API."""

from core.server import mcp


@mcp.tool()
async def seedance_list_models() -> str:
    """List all available Seedance models with their capabilities.

    Shows all available model options with their features and strengths.
    Use this to understand which model to choose for your video generation.

    Returns:
        Table of all models with descriptions and capabilities.
    """
    return """Available Seedance Models:

| Model | Type | Strengths | Audio |
|-------|------|-----------|------- |
| doubao-seedance-2-5-260628 | 2.5 | Latest flagship, up to 30s, multimodal reference, edit/extend | Yes |
| doubao-seedance-2-0-260128 | 2.0 | Latest generation, highest quality, multimodal reference, up to 4k (default) | Yes |
| doubao-seedance-2-0-fast-260128 | 2.0 Fast | Latest generation, faster, up to 720p | Yes |
| doubao-seedance-2-0-mini-260615 | 2.0 Mini | Latest generation, lightweight, cheapest within 2.0, up to 720p | Yes |
| doubao-seedance-1-5-pro-251215 | Flagship | 1.5, high quality, audio support | Yes |
| doubao-seedance-1-0-pro-250528 | Standard | Balanced quality and speed | No |
| doubao-seedance-1-0-pro-fast-251015 | Fast | Cost-optimized, faster generation | No |
| doubao-seedance-1-0-lite-t2v-250428 | Lite T2V | Lightweight text-to-video | No |
| doubao-seedance-1-0-lite-i2v-250428 | Lite I2V | Lightweight image-to-video | No |

Model Selection Guide:
- Latest flagship: doubao-seedance-2-5-260628 (up to 30s, multimodal reference, edit/extend)
- Default / highest resolution: doubao-seedance-2-0-260128 (up to 4k)
- Latest fast: doubao-seedance-2-0-fast-260128
- Latest lightweight / cheapest within 2.0: doubao-seedance-2-0-mini-260615
- 1.5 flagship (audio): doubao-seedance-1-5-pro-251215
- 1.0 standard: doubao-seedance-1-0-pro-250528
- Fastest/cheapest 1.0: doubao-seedance-1-0-pro-fast-251015
- Text-only lightweight: doubao-seedance-1-0-lite-t2v-250428
- Image-to-video lightweight: doubao-seedance-1-0-lite-i2v-250428

Notes:
- Current pricing: https://platform.acedata.cloud/services/seedance?tab=pricing
- Prices are billed in Credits and depend on the model, resolution, duration, audio and reference media.
- USD conversion depends on the current credit package; this tool does not quote a fixed USD rate.
- Audio generation (generate_audio) is supported by the 1.5 Pro and 2.x models
- Seedance 2.0 adds multimodal reference inputs; Seedance 2.5 adds pure-audio reference, larger limits, edit, and extend
- Resolution affects cost: 480p < 720p < 1080p < 4k ('4k' is doubao-seedance-2-0-260128 only; 2.5 maxes at 1080p; 2-0-fast / 2-0-mini max at 720p)
"""


@mcp.tool()
async def seedance_list_resolutions() -> str:
    """List all available resolutions and aspect ratios for Seedance.

    Shows all available resolution and aspect ratio options with use cases.

    Returns:
        Tables of resolutions and aspect ratios with descriptions.
    """
    return """Available Seedance Resolutions:

| Resolution | Description | Best For |
|------------|-------------|----------|
| 480p | Low resolution | Previews, drafts, cost savings |
| 720p | HD (default) | General use, social media |
| 1080p | Full HD | High-quality production |
| 4k | Ultra HD | Highest detail (doubao-seedance-2-0-260128 only) |

Available Aspect Ratios:

| Ratio | Description | Use Case |
|-------|-------------|----------|
| 16:9 | Landscape (default) | YouTube, TV, presentations |
| 9:16 | Portrait | TikTok, Instagram Reels, mobile |
| 1:1 | Square | Instagram posts, social media |
| 4:3 | Traditional TV | Classic video, presentations |
| 3:4 | Portrait traditional | Portrait content |
| 21:9 | Ultrawide | Cinematic, movies |
| adaptive | Auto-detect | Matches input image ratio (I2V only) |

Recommended:
- 16:9 for most video content
- 9:16 for mobile-first platforms
- Use 'adaptive' when working with image-to-video to match source
"""


@mcp.tool()
async def seedance_list_actions() -> str:
    """List all available Seedance API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Seedance MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    return """Available Seedance Actions and Tools:

Video Generation:
- seedance_generate_video: Create video from a text prompt (T2V)
- seedance_generate_video_from_image: Create video using reference images (I2V)

Task Management:
- seedance_get_task: Check status of a single generation
- seedance_get_tasks_batch: Check status of multiple generations

Information:
- seedance_list_models: Show available models and pricing
- seedance_list_resolutions: Show available resolutions and ratios
- seedance_list_actions: Show this action reference (you are here)

Workflow Examples:

1. Quick text-to-video:
   seedance_generate_video -> seedance_get_task

2. Image-to-video (animate an image):
   seedance_generate_video_from_image (with first_frame_url) -> seedance_get_task

3. Video transition between two images:
   seedance_generate_video_from_image (with first_frame_url + last_frame_url)

4. Style-guided generation:
   seedance_generate_video_from_image (with reference_image_urls)

5. Async generation (for production):
   seedance_generate_video (with callback_url) -> webhook notification

6. Budget-friendly generation:
   seedance_generate_video (with model=fast, resolution='480p')

7. High-quality with audio:
   seedance_generate_video (with model=1.5-pro, generate_audio=true)

Tips:
- Use descriptive prompts for better results
- Include motion descriptions: "walking", "flying", "zooming in"
- Specify style: "cinematic", "realistic", "artistic", "anime"
- 1.5 Pro and 2.x models support audio generation
- Use seed parameter for reproducible results
- Use return_last_frame=true when planning to extend videos
"""
