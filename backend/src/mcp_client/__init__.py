"""MCP Client - Registry and config for external MCPs that Kanban uses."""

from .registry import (
    MCP_REGISTRY,
    get_available_mcps,
    get_defaults,
    get_mcp_config,
    load_mcp_registry,
)

__all__ = [
    "MCP_REGISTRY",
    "get_available_mcps",
    "get_defaults",
    "get_mcp_config",
    "load_mcp_registry",
]
