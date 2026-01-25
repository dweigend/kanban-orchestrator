# 🧪 Tests

> Pytest test suite for backend

## 📋 Contents

| File | Description |
|------|-------------|
| `conftest.py` | Pytest fixtures |
| `test_tasks.py` | Task CRUD tests |
| `test_agent.py` | Agent execution tests |
| `test_projects.py` | Project tests |
| `test_settings.py` | Settings tests |
| `test_schema.py` | Schema endpoint tests |
| `test_events.py` | SSE event tests |
| `test_git.py` | Git service tests |
| `test_mcp_server.py` | MCP server tests |

## 🔧 Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_tasks.py

# Run specific test
uv run pytest tests/test_tasks.py::test_create_task -v
```

## 🏗️ Fixtures

```python
# conftest.py provides:
@pytest.fixture
def client():
    """FastAPI test client"""

@pytest.fixture
def db():
    """Test database session"""

@pytest.fixture
def sample_task():
    """Sample task for testing"""
```

## 🎯 Test Pattern

```python
def test_create_task(client, db):
    response = client.post("/api/tasks", json={
        "title": "Test Task"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
```
