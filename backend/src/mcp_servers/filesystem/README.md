# 📁 Filesystem MCP Server

> Sandboxed filesystem operations for agent workspace access

## 📋 Contents

| File | Description |
|------|-------------|
| `server.py` | MCP server implementation |

## 🏗️ Architecture

Provides sandboxed filesystem access within workspace boundaries:

```
┌─────────────────┐
│  Claude Agent   │
└────────┬────────┘
         │ MCP call
         ▼
┌─────────────────┐
│ Filesystem MCP  │
│ - read_file     │
│ - write_file    │
│ - list_dir      │
└────────┬────────┘
         │ sandboxed
         ▼
┌─────────────────┐
│  Workspace      │
│  /path/to/proj  │
└─────────────────┘
```

## 🔧 Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Write file contents |
| `list_directory` | List directory contents |
| `create_directory` | Create new directory |
| `delete_file` | Delete file |

## 🔒 Security

- All paths are sandboxed to `WORKSPACE_PATH`
- Path traversal attacks are prevented
- Only operates within project boundaries

## ⚙️ Configuration

Environment variable required:
```bash
WORKSPACE_PATH=/path/to/project
```
