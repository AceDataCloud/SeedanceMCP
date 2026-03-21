# MCP Seedance

<!-- mcp-name: io.github.AceDataCloud/mcp-seedance -->

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

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the [API documentation page](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8)
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://seedance.mcp.acedata.cloud/mc`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://seedance.mcp.acedata.cloud/mc`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "seedance": {
      "type": "streamable-http",
      "url": "https://seedance.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cursor / Windsurf

Add to your MCP config (`.cursor/mcp.json` or `.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "seedance": {
      "type": "streamable-http",
      "url": "https://seedance.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### VS Code (Copilot)

Add to your VS Code MCP config (`.vscode/mcp.json`):

```json
{
  "servers": {
    "seedance": {
      "type": "streamable-http",
      "url": "https://seedance.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

Or install the [Ace Data Cloud MCP extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.acedatacloud-mcp) for VS Code, which bundles all 11 MCP servers with one-click setup.

#### JetBrains IDEs

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**
2. Click **Add** → **HTTP**
3. Paste:

```json
{
  "mcpServers": {
    "seedance": {
      "url": "https://seedance.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### cURL Test

```bash
# Health check (no auth required)
curl https://seedance.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://seedance.mcp.acedata.cloud/mc \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-seedance
# or
uvx mcp-seedance

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-seedance

# Run (HTTP mode for remote access)
mcp-seedance --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "seedance": {
      "command": "uvx",
      "args": ["mcp-seedance"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-seedance:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-seedance:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

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
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
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
