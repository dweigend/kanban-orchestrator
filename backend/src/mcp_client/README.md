# 🔌 MCP Client

> MCP server registry and configuration for agent orchestration

## 📋 Contents

| File | Description |
|------|-------------|
| `registry.py` | MCP server registration and loading |

## 🏗️ Architecture

The MCP Client manages connections to external MCP servers that the orchestrator **uses**.

```
┌─────────────────────┐
│  Kanban Orchestrator │
│  (MCP Client)        │
└─────────┬───────────┘
          │ uses
          ▼
┌─────────────────────┐
│  External MCPs      │
│  - filesystem       │
│  - github_simple    │
│  - perplexity       │
│  - openalex         │
└─────────────────────┘
```

## ⚙️ Configuration

MCP servers are configured in `.kanban/mcps.yaml`:

```yaml
servers:
  filesystem:
    enabled: true
    command: python
    args: ["-m", "src.mcp_servers.filesystem.server"]
    env:
      WORKSPACE_PATH: "${WORKSPACE_PATH}"
```

## 🔧 Usage

```python
from src.mcp_client.registry import load_mcp_config, get_enabled_servers

# Load config
config = load_mcp_config()

# Get enabled servers for agent
servers = get_enabled_servers(allowed_mcps=["filesystem", "github_simple"])
```
