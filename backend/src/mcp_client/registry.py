"""MCP Server Registry for dynamic tool loading from YAML config."""

import os
from pathlib import Path
from typing import TypedDict

import yaml


class MCPServerConfig(TypedDict, total=False):
    """Configuration for an MCP server."""

    command: str
    args: list[str]
    env: dict[str, str]


class MCPOption(TypedDict):
    """MCP server option for schema endpoint."""

    value: str
    label: str
    description: str


class MCPDefaults(TypedDict):
    """Default MCP configuration."""

    allowed_mcps: list[str]
    template: str | None


# Path to YAML config file
CONFIG_PATH = Path(__file__).parent.parent.parent / ".kanban" / "mcps.yaml"

# Default YAML content for auto-creation
DEFAULT_CONFIG = """\
# MCP Server Registry Configuration
# Defines available MCP servers for agent orchestration

defaults:
  allowed_mcps:
    - filesystem
  template: null

servers:
  filesystem:
    enabled: true
    command: python
    args: ["-m", "src.mcp_servers.filesystem.server"]
    env:
      WORKSPACE_PATH: "${WORKSPACE_PATH}"
    description: "Filesystem operations in workspace"

  perplexity:
    enabled: false
    command: npx
    args: ["-y", "@anthropic/mcp-server-perplexity"]
    env:
      PERPLEXITY_API_KEY: "${PERPLEXITY_API_KEY}"
    description: "Web search and research"
"""


def _ensure_config_exists() -> None:
    """Create default config file if it doesn't exist."""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(DEFAULT_CONFIG)


def load_mcp_registry() -> dict:
    """Load MCP registry from YAML config file.

    Returns:
        Parsed YAML content with 'defaults' and 'servers' sections.
    """
    _ensure_config_exists()
    return yaml.safe_load(CONFIG_PATH.read_text())  # type: ignore[no-any-return]


def get_defaults() -> MCPDefaults:
    """Get default MCP configuration.

    Returns:
        Dictionary with 'allowed_mcps' list and optional 'template'.
    """
    config = load_mcp_registry()
    defaults = config.get("defaults", {})
    return MCPDefaults(
        allowed_mcps=defaults.get("allowed_mcps", ["filesystem"]),
        template=defaults.get("template"),
    )


def get_available_mcps() -> list[MCPOption]:
    """Get list of available (enabled) MCPs for schema endpoint.

    Returns:
        List of MCPOption dicts with value, label, description.
    """
    config = load_mcp_registry()
    servers = config.get("servers", {})

    options: list[MCPOption] = []
    for name, server in servers.items():
        if server.get("enabled", False):
            options.append(
                MCPOption(
                    value=name,
                    label=name.replace("_", " ").title(),
                    description=server.get("description", ""),
                )
            )
    return options


def _resolve_env_value(
    value: str,
    workspace_path: str,
    sandbox_dir: str | None = None,
) -> str:
    """Resolve environment variable placeholders in a value.

    Supports:
        ${WORKSPACE_PATH} - Resolved to workspace_path parameter
        ${SANDBOX_DIR} - Resolved to sandbox_dir parameter
        ${VAR_NAME} - Resolved from OS environment
    """
    if not (value.startswith("${") and value.endswith("}")):
        return value

    env_var = value[2:-1]
    if env_var == "WORKSPACE_PATH":
        return workspace_path
    if env_var == "SANDBOX_DIR" and sandbox_dir:
        return sandbox_dir
    return os.environ.get(env_var, "")


def get_mcp_config(
    tool_names: list[str],
    workspace_path: str,
    sandbox_dir: str | None = None,
) -> dict[str, MCPServerConfig]:
    """Build MCP config for workflow based on required tools.

    Args:
        tool_names: List of MCP tool names to include
        workspace_path: Path to the workspace directory
        sandbox_dir: Optional sandbox directory path

    Returns:
        Dictionary of MCP server configurations with environment variables resolved
    """
    config = load_mcp_registry()
    servers = config.get("servers", {})
    result: dict[str, MCPServerConfig] = {}

    for name in tool_names:
        if name not in servers:
            continue

        server = servers[name]
        if not server.get("enabled", False):
            continue

        # Build resolved config
        env = server.get("env", {})
        resolved_env: dict[str, str] = {}
        for key, value in env.items():
            resolved_env[key] = _resolve_env_value(value, workspace_path, sandbox_dir)

        result[name] = MCPServerConfig(
            command=server["command"],
            args=server.get("args", []),
            env=resolved_env,
        )

    return result


# Backward compatibility - expose registry as dict for existing code
def _load_legacy_registry() -> dict[str, MCPServerConfig]:
    """Load registry in legacy format (without env resolution)."""
    config = load_mcp_registry()
    servers = config.get("servers", {})
    result: dict[str, MCPServerConfig] = {}

    for name, server in servers.items():
        if server.get("enabled", False):
            result[name] = MCPServerConfig(
                command=server["command"],
                args=server.get("args", []),
                env=server.get("env", {}),
            )
    return result


MCP_REGISTRY = _load_legacy_registry()
