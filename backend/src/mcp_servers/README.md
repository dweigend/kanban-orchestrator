# 📡 MCP Servers

> MCP servers exposed by Kanban Orchestrator

## 📋 Contents

| File | Description |
|------|-------------|
| `kanban_server.py` | Kanban board MCP for Claude Code |
| `filesystem/` | Filesystem operations MCP |

## 🏗️ Architecture

These are MCP servers that the Kanban Orchestrator **exposes** to external tools.

```
┌─────────────────────┐
│  Claude Code        │
│  (MCP Client)       │
└─────────┬───────────┘
          │ uses
          ▼
┌─────────────────────┐
│  Kanban MCP Server  │
│  - list_tasks       │
│  - create_task      │
│  - update_task      │
│  - run_agent        │
└─────────────────────┘
```

## 🔧 Kanban Server

Provides Kanban board access via MCP:

| Tool | Description |
|------|-------------|
| `list_tasks` | Get all tasks |
| `create_task` | Create new task |
| `update_task` | Update task status |
| `run_agent` | Execute agent on task |

### Configuration

In Claude Code's `.mcp.json`:

```json
{
  "mcpServers": {
    "kanban": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.mcp_servers.kanban_server"],
      "cwd": "backend"
    }
  }
}
```

## 📁 Filesystem Server

Provides sandboxed filesystem access within workspace boundaries.
