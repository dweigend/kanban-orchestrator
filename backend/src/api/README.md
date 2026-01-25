# 🌐 API Layer

> FastAPI routes, schemas, and services

## 📋 Contents

| File | Description |
|------|-------------|
| `schemas.py` | Pydantic models for API requests/responses |
| `events.py` | SSE event publishing utilities |
| `task_service.py` | Task CRUD operations |
| `project_service.py` | Project management |
| `routes/` | FastAPI route handlers |

## 🏗️ Architecture

```
api/
├── schemas.py          # All Pydantic models
├── events.py           # SSE broadcasting
├── task_service.py     # Task business logic
├── project_service.py  # Project business logic
└── routes/
    ├── agent.py        # Agent execution endpoints
    ├── events.py       # SSE endpoint
    ├── projects.py     # Project CRUD
    ├── schema.py       # Dynamic schema endpoint
    ├── settings.py     # Settings endpoints
    └── tasks.py        # Task CRUD
```

## 🔧 Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tasks` | List all tasks |
| `POST` | `/api/tasks` | Create task |
| `PATCH` | `/api/tasks/{id}` | Update task |
| `DELETE` | `/api/tasks/{id}` | Delete task |
| `POST` | `/api/agent/run/{id}` | Execute agent |
| `POST` | `/api/agent/plan/{id}` | Plan task decomposition |
| `GET` | `/api/events` | SSE stream |

## 📡 SSE Events

The API publishes real-time events via SSE:
- `task_created` - New task created
- `task_updated` - Task status changed
- `task_deleted` - Task removed
- `agent_log` - Live agent output
