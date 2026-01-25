# 📊 Models

> SQLAlchemy database models

## 📋 Contents

| File | Description |
|------|-------------|
| `task.py` | Task model with status, priority, subtasks |
| `project.py` | Project container for tasks |
| `agent_run.py` | Agent execution history |

## 🏗️ Schema

### Task
```python
Task:
  - id: UUID (primary key)
  - title: str
  - description: str
  - status: TaskStatus (TODO, IN_PROGRESS, DONE, etc.)
  - priority: Priority (LOW, MEDIUM, HIGH)
  - parent_id: UUID (for subtasks)
  - created_at: datetime
  - updated_at: datetime
```

### Project
```python
Project:
  - id: UUID (primary key)
  - name: str
  - workspace_path: str
  - created_at: datetime
```

### AgentRun
```python
AgentRun:
  - id: UUID (primary key)
  - task_id: UUID (foreign key)
  - status: str
  - model: str
  - started_at: datetime
  - finished_at: datetime
```

## 🔧 Usage

```python
from src.models import Task, Project, AgentRun
from src.database import get_db

with get_db() as db:
    tasks = db.query(Task).all()
```
