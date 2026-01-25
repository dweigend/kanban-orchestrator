# 🔧 Services

> Business logic and external integrations

## 📋 Contents

| File | Description |
|------|-------------|
| `git.py` | Git operations (checkpoint, commit) |

## 🏗️ Architecture

Services handle business logic outside of API routes:
- Keep routes thin (validation + delegation)
- Services contain the actual logic
- Can be reused across different routes

## 🔧 Usage

```python
from src.services.git import create_checkpoint, create_commit

# Create checkpoint before agent run
checkpoint_hash = create_checkpoint(
    workspace_path="/path/to/project",
    message="checkpoint: before agent run"
)

# Create commit after successful changes
commit_hash = create_commit(
    workspace_path="/path/to/project",
    message="feat: implement feature"
)
```

## 📚 Git Service

### create_checkpoint()
Creates a git commit to save current state before agent execution.
Returns commit hash or None if nothing to commit.

### create_commit()
Creates a git commit after successful agent execution.
Returns commit hash or None if nothing to commit.
