# MCP Seedance

[![PyPI version](https://img.shields.io/pypi/v/mcp-seedance.svg)](https://pypi.org/project/mcp-seedance/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-seedance.svg)](https://pypi.org/project/mcp-seedance/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [ByteDance Seedance](https://seedance.ai) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI videos directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Video** - Create AI-generated videos from text prompts
- **Image to Video** - Animate images with first frame, last frame, and reference image control
- **Multiple Models** - Support for Seedance 1.5 Pro, 1.0 Pro, 1.0 Pro Fast, 1.0 Lite T2V/I2V
- **Multiple Resolutions** - 480p, 720p (default), and 1080p output
- **Flexible Aspect Ratios** - 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, and adaptive
- **Audio Generation** - Generate synchronized audio for videos (1.5 Pro)
- **Service Tiers** - Default (priority) and Flex (cost-effective) processing
- **Task Tracking** - Monitor generation progress and retrieve results

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud):

1. Sign up or log in
2. Navigate to [Seedance Videos API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8)
3. Click "Acquire" to get your token

### 2. Install

```bash
# Clone the repository
git clone https://github.com/AceDataCloud/MCPSeedance.git
cd MCPSeedance

# Install with pip
pip install -e .

# Or with uv (recommended)
uv pip install -e .
```

### 3. Configure

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API token
echo "ACEDATACLOUD_API_TOKEN=your_token_here" > .env
```

### 4. Run

```bash
# Run the server
mcp-seedance

# Or with Python directly
python main.py
```

## Claude Desktop Integration

Add to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "seedance": {
      "command": "mcp-seedance",
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Or if using uv:

```json
{
  "mcpServers": {
    "seedance": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-seedance", "mcp-seedance"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## Remote HTTP Mode (Hosted)

AceDataCloud hosts a managed MCP server that you can connect to directly — **no local installation required**.

**Endpoint**: `https://seedance.mcp.acedata.cloud/mcp`

All requests require a Bearer token in the `Authorization` header. Get your token from [AceDataCloud Platform](https://platform.acedata.cloud).

### Claude Desktop (Remote)

```json
{
  "mcpServers": {
    "seedance": {
      "type": "streamable-http",
      "url": "https://seedance.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your_api_token_here"
      }
    }
  }
}
```

### Cursor / VS Code

In your MCP client settings, add:

- **Type**: `streamable-http`
- **URL**: `https://seedance.mcp.acedata.cloud/mcp`
- **Headers**: `Authorization: Bearer your_api_token_here`

### cURL Test

```bash
# Health check (no auth required)
curl https://seedance.mcp.acedata.cloud/health

# MCP initialize (requires Bearer token)
curl -X POST https://seedance.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer your_api_token_here" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### Self-Hosting with Docker

```bash
docker pull ghcr.io/acedatacloud/mcp-seedance:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-seedance:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header and uses it for upstream API calls.

## Available Tools

### Video Generation

| Tool                                 | Description                                     |
| ------------------------------------ | ----------------------------------------------- |
| `seedance_generate_video`            | Generate video from a text prompt               |
| `seedance_generate_video_from_image` | Generate video using reference/start/end images |

### Tasks

| Tool                       | Description                  |
| -------------------------- | ---------------------------- |
| `seedance_get_task`        | Query a single task status   |
| `seedance_get_tasks_batch` | Query multiple tasks at once |

### Information

| Tool                        | Description                       |
| --------------------------- | --------------------------------- |
| `seedance_list_models`      | List available Seedance models    |
| `seedance_list_resolutions` | List available output resolutions |
| `seedance_list_actions`     | List available API actions        |

## Usage Examples

### Generate Video from Prompt

```
User: Create a video of a cat playing with a ball of yarn

Claude: I'll generate a video for you.
[Calls seedance_generate_video with prompt="A cute cat playfully batting a ball of yarn"]
```

### Animate an Image

```
User: Turn this image into a video: https://example.com/landscape.jpg

Claude: I'll create a video from your image.
[Calls seedance_generate_video_from_image with first_frame_url and appropriate prompt]
```

### Generate with Audio

```
User: Create a video of rain falling with sound

Claude: I'll generate a video with synchronized audio.
[Calls seedance_generate_video with prompt="Rain falling on a quiet street" and generate_audio=True, model="doubao-seedance-1-5-pro-250528"]
```

## Available Models

| Model                                 | Description       | Features                   |
| ------------------------------------- | ----------------- | -------------------------- |
| `doubao-seedance-1-5-pro-250528`      | 1.5 Pro           | Audio generation, T2V, I2V |
| `doubao-seedance-1-0-pro-250528`      | 1.0 Pro (default) | High quality T2V, I2V      |
| `doubao-seedance-1-0-pro-fast-250528` | 1.0 Pro Fast      | Faster generation          |
| `doubao-seedance-1-0-lite-t2v-250528` | 1.0 Lite T2V      | Lightweight text-to-video  |
| `doubao-seedance-1-0-lite-i2v-250528` | 1.0 Lite I2V      | Lightweight image-to-video |

## Available Aspect Ratios

| Aspect Ratio | Description          | Use Case                   |
| ------------ | -------------------- | -------------------------- |
| `16:9`       | Landscape (default)  | YouTube, TV, presentations |
| `9:16`       | Portrait             | TikTok, Instagram Reels    |
| `1:1`        | Square               | Instagram posts            |
| `4:3`        | Traditional          | Classic video format       |
| `3:4`        | Portrait traditional | Portrait content           |
| `21:9`       | Ultrawide            | Cinematic content          |
| `adaptive`   | Adaptive             | Auto-detect from image     |

## Configuration

### Environment Variables

| Variable                      | Description                 | Default                          |
| ----------------------------- | --------------------------- | -------------------------------- |
| `ACEDATACLOUD_API_TOKEN`      | API token from AceDataCloud | **Required**                     |
| `ACEDATACLOUD_API_BASE_URL`   | API base URL                | `https://api.acedata.cloud`      |
| `SEEDANCE_DEFAULT_MODEL`      | Default model               | `doubao-seedance-1-0-pro-250528` |
| `SEEDANCE_DEFAULT_RESOLUTION` | Default resolution          | `720p`                           |
| `SEEDANCE_DEFAULT_RATIO`      | Default aspect ratio        | `16:9`                           |
| `SEEDANCE_DEFAULT_DURATION`   | Default duration (seconds)  | `5`                              |
| `SEEDANCE_REQUEST_TIMEOUT`    | Request timeout in seconds  | `1800`                           |
| `LOG_LEVEL`                   | Logging level               | `INFO`                           |

### Command Line Options

```bash
mcp-seedance --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/MCPSeedance.git
cd MCPSeedance

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=core --cov=tools

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy core tools
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Project Structure

```
MCPSeedance/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Seedance API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── video_tools.py     # Video generation tools
│   ├── task_tools.py      # Task query tools
│   └── info_tools.py      # Information tools
├── prompts/                # MCP prompts
│   └── __init__.py        # Prompt templates
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_integration.py
│   └── test_utils.py
├── deploy/                 # Deployment configs
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── .gitignore
├── CHANGELOG.md
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud Seedance API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8):

- [Seedance Videos API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8) - Video generation
- [Seedance Tasks API](https://platform.acedata.cloud/documents/c09d6a1b-3cca-4f7c-add3-8c14be60da3c) - Task queries

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [ByteDance Seedance](https://seedance.ai)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
