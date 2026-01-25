# 🛤️ Routes

> FastAPI route handlers

## 📋 Contents

| File | Description |
|------|-------------|
| `agent.py` | Agent execution endpoints |
| `events.py` | SSE stream endpoint |
| `projects.py` | Project CRUD |
| `schema.py` | Dynamic schema endpoint |
| `settings.py` | Settings endpoints |
| `tasks.py` | Task CRUD |

## 🏗️ Endpoints

### Tasks (`tasks.py`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tasks` | List tasks |
| `POST` | `/api/tasks` | Create task |
| `PATCH` | `/api/tasks/{id}` | Update task |
| `DELETE` | `/api/tasks/{id}` | Delete task |

### Agent (`agent.py`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/agent/run/{id}` | Run agent |
| `POST` | `/api/agent/plan/{id}` | Plan decomposition |
| `POST` | `/api/agent/stop/{id}` | Stop agent |
| `POST` | `/api/agent/execute-subtasks/{id}` | Execute subtasks |

### Events (`events.py`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/events` | SSE stream |

### Settings (`settings.py`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/settings` | Get settings |
| `PUT` | `/api/settings` | Save settings |

## 🔧 Pattern

Routes are thin - they validate input and delegate to services:

```python
@router.post("/api/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return await task_service.create(db, task)
```
