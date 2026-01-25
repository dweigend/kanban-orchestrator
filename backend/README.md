# 🔧 Backend

> FastAPI + Claude Agent SDK for task orchestration

## 📋 Quick Start

```bash
# Install dependencies
uv sync

# Run server
uv run python main.py
```

Server runs at `http://localhost:8000`

## 📁 Structure

```
backend/
├── src/
│   ├── agents/       # Claude SDK Agent Orchestrator
│   ├── api/          # FastAPI Routes + Services
│   ├── mcp_client/   # MCP config for servers we USE
│   ├── mcp_servers/  # MCP servers we EXPOSE
│   ├── models/       # SQLAlchemy Models
│   └── services/     # Business Logic
├── tests/            # Pytest tests
├── main.py           # Entry point
└── pyproject.toml    # Dependencies
```

## 🔧 Commands

```bash
# Development
uv run python main.py

# Lint + Format
uv run ruff check --fix . && uv run ruff format .

# Type Check
uvx ty check

# Test
uv run pytest

# All checks
uv run ruff check --fix . && uv run ruff format . && uvx ty check
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tasks` | List all tasks |
| `POST` | `/api/tasks` | Create task |
| `PATCH` | `/api/tasks/{id}` | Update task |
| `DELETE` | `/api/tasks/{id}` | Delete task |
| `POST` | `/api/agent/run/{id}` | Run agent on task |
| `GET` | `/api/events` | SSE stream |

## ⚙️ Configuration

Copy example files and configure:

```bash
cp .kanban/mcps.yaml.example .kanban/mcps.yaml
cp .kanban/settings.json.example .kanban/settings.json
```

## 📚 Tech Stack

- **Runtime**: Python 3.12+
- **Framework**: FastAPI
- **Database**: SQLite + SQLAlchemy
- **AI**: Claude Agent SDK
- **Package Manager**: uv
