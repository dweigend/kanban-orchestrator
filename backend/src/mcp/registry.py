"""MCP Server Registry for dynamic tool loading."""

import os
from typing import TypedDict


class MCPServerConfig(TypedDict):
    """Configuration for an MCP server."""

    command: str
    args: list[str]
    env: dict[str, str]


# Registry of available MCP servers
MCP_REGISTRY: dict[str, MCPServerConfig] = {
    "filesystem": {
        "command": "python",
        "args": ["-m", "src.mcp.filesystem.server"],
        "env": {"WORKSPACE_PATH": "${WORKSPACE_PATH}"},
    },
    # Future MCPs:
    # "perplexity": {
    #     "command": "python",
    #     "args": ["-m", "src.mcp_servers.perplexity.server"],
    #     "env": {"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"},
    # },
}


def get_mcp_config(
    tool_names: list[str], workspace_path: str
) -> dict[str, MCPServerConfig]:
    """Build MCP config for workflow based on required tools.

    Args:
        tool_names: List of MCP tool names to include
        workspace_path: Path to the workspace directory

    Returns:
        Dictionary of MCP server configurations with environment variables resolved
    """
    config: dict[str, MCPServerConfig] = {}

    for name in tool_names:
        if name not in MCP_REGISTRY:
            continue

        server = MCP_REGISTRY[name].copy()
        env = server.get("env", {}).copy()

        # Resolve environment variables
        resolved_env: dict[str, str] = {}
        for key, value in env.items():
            if value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                if env_var == "WORKSPACE_PATH":
                    resolved_env[key] = workspace_path
                else:
                    resolved_env[key] = os.environ.get(env_var, "")
            else:
                resolved_env[key] = value

        server["env"] = resolved_env
        config[name] = server

    return config
