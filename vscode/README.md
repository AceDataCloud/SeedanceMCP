# Seedance MCP

ByteDance Seedance — dance and motion video generation from text or image.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-seedance) [![PyPI](https://img.shields.io/pypi/v/mcp-seedance.svg?label=PyPI)](https://pypi.org/project/mcp-seedance/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://seedance.mcp.acedata.cloud/mcp)

Generate Seedance AI dance/motion videos. Configurable resolution, aspect ratio, duration, and optional audio.

This extension registers the **seedance** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `seedance` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=seedance_mcp_vscode_api_key) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a video task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Seedance MCP: Set Ace Data Cloud API Key**
- **Seedance MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://seedance.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

## VS Code Setup Guide

For screenshots, token setup, project-level and user-level `mcp.json`, and Copilot Agent Mode examples, see:

- [Seedance MCP VS Code guide](https://platform.acedata.cloud/documents/promotion_article_mcp_seedance_vscode?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=seedance_mcp_vscode_documents_promotion_article_mcp_seedance_vscode)
- [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=seedance_mcp_vscode_documents_promotion_article_mcp_all_vscode)

### Example prompts

- "Generate a Seedance video of a stylized robot dancing breakdance on a rooftop."
- "Animate https://example.com/character.png into a Seedance clip, vertical 9:16, 8 seconds."

---

## Tool Reference

**7 tools** available via this server.

| Tool | Description |
| --- | --- |
| `seedance_generate_video` | Generate AI video from a text prompt using ByteDance Seedance. |
| `seedance_generate_video_from_image` | Generate AI video using reference images with ByteDance Seedance. |
| `seedance_get_task` | Query the status and result of a video generation task. |
| `seedance_get_tasks_batch` | Query multiple video generation tasks at once. |
| `seedance_list_models` | List all available Seedance models with their capabilities and pricing. |
| `seedance_list_resolutions` | List all available resolutions and aspect ratios for Seedance. |
| `seedance_list_actions` | List all available Seedance API actions and corresponding tools. |

## Pricing

From $0.15 per clip. Free trial credit on sign-up. See full pricing at [https://platform.acedata.cloud/documents/seedance-mcp](https://platform.acedata.cloud/documents/seedance-mcp?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=seedance_mcp_vscode_quick_start).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.seedance
Server label: Seedance MCP
Server URL  : https://seedance.mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or $ACEDATACLOUD_API_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{
  "servers": {
    "seedance": {
      "type": "http",
      "url": "https://seedance.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
      "description": "Ace Data Cloud API key",
      "password": true
    }
  ]
}
```

### Alternative: local stdio (no network roundtrip)

For offline dev, air-gapped environments, or pinning to a specific PyPI
version, install [`uv`](https://docs.astral.sh/uv/) and use:

```jsonc
{
  "servers": {
    "seedance": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-seedance"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-seedance`](https://pypi.org/project/mcp-seedance/) on demand.

---

## Links

- **Hosted endpoint:** https://seedance.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-seedance`](https://pypi.org/project/mcp-seedance/)
- **Source repository:** https://github.com/AceDataCloud/SeedanceMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=seedance_mcp_vscode_platform
- **MCP documentation:** https://platform.acedata.cloud/documents/seedance-mcp?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=seedance_mcp_vscode_quick_start

## License

MIT — see [LICENSE](LICENSE).
