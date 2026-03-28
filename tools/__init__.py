"""Tools module for Seedance MCP server."""

# Import all tools to register them with the MCP server
from tools import info_tools, task_tools, video_tools

__all__ = [
    "video_tools",
    "task_tools",
    "info_tools",
]
