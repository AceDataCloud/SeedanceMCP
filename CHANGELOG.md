# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-08

### Added

- Initial release of MCP Seedance Server
- Video generation tools:
  - `seedance_generate_video` - Generate video from text prompts (T2V)
  - `seedance_generate_video_from_image` - Generate video using reference images (I2V)
- Task tracking:
  - `seedance_get_task` - Query single task status
  - `seedance_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `seedance_list_models` - List available models and pricing
  - `seedance_list_resolutions` - List available resolutions and ratios
  - `seedance_list_actions` - List available actions
- Support for 5 Seedance models:
  - doubao-seedance-1-5-pro-251215 (flagship with audio)
  - doubao-seedance-1-0-pro-250528 (standard)
  - doubao-seedance-1-0-pro-fast-251015 (fast/cheap)
  - doubao-seedance-1-0-lite-t2v-250428 (lightweight T2V)
  - doubao-seedance-1-0-lite-i2v-250428 (lightweight I2V)
- Multiple resolutions: 480p, 720p, 1080p
- Multiple aspect ratios: 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, adaptive
- Audio generation support (1.5 Pro model)
- First frame / last frame / reference image support
- Flex service tier (50% cost savings)
- Seed-based reproducible generation
- Camera fixed mode
- Watermark option
- Last frame extraction for video chaining
- Async callback URL support
- stdio and HTTP transport modes
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/SeedanceMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/SeedanceMCP/releases/tag/v0.1.0
