"""MCP Client - Registry and config for external MCPs that Kanban uses."""

from .registry import MCP_REGISTRY, get_mcp_config

__all__ = ["MCP_REGISTRY", "get_mcp_config"]
