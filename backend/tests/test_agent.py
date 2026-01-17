"""Agent API endpoint tests."""

from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient


@pytest.fixture(autouse=True)
def mock_background_tasks(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock BackgroundTasks to prevent actual background execution in tests.

    Background tasks use a separate DB session which doesn't share the
    test's in-memory database, causing hangs and errors.
    """
    mock = MagicMock()
    monkeypatch.setattr(
        "src.api.routes.agent.BackgroundTasks.add_task",
        lambda self, *args, **kwargs: mock(*args, **kwargs),
    )
    return mock


async def test_list_agent_runs_empty(client: AsyncClient) -> None:
    """GET /api/agent/runs returns empty list initially."""
    response = await client.get("/api/agent/runs")
    assert response.status_code == 200
    assert response.json() == []


async def test_start_agent_run_task_not_found(client: AsyncClient) -> None:
    """POST /api/agent/run returns 404 for unknown task."""
    response = await client.post(
        "/api/agent/run",
        json={"task_id": "nonexistent-task-id"},
    )
    assert response.status_code == 404


async def test_start_agent_run(client: AsyncClient) -> None:
    """POST /api/agent/run returns 202 with real AgentRun.

    Note: Background task execution is not tested here as it uses a separate
    DB connection. We only verify the HTTP response and AgentRun creation.
    """
    # Create task first
    task_response = await client.post("/api/tasks", json={"title": "Agent Test"})
    task_id = task_response.json()["id"]

    response = await client.post("/api/agent/run", json={"task_id": task_id})
    assert response.status_code == 202
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "pending"
    # Real UUID is assigned immediately (not placeholder)
    assert data["id"] != "pending"
    assert len(data["id"]) == 36  # UUID format
    assert "created_at" in data


async def test_start_agent_run_conflict(client: AsyncClient) -> None:
    """POST /api/agent/run returns 409 when task already has active run."""
    # Create task
    task_response = await client.post("/api/tasks", json={"title": "Conflict Test"})
    task_id = task_response.json()["id"]

    # First run should succeed
    response1 = await client.post("/api/agent/run", json={"task_id": task_id})
    assert response1.status_code == 202

    # Second run should fail with 409
    response2 = await client.post("/api/agent/run", json={"task_id": task_id})
    assert response2.status_code == 409
    assert "already has an active agent run" in response2.json()["detail"]


async def test_get_agent_run_not_found(client: AsyncClient) -> None:
    """GET /api/agent/runs/{id} returns 404 for unknown ID."""
    response = await client.get("/api/agent/runs/nonexistent-id")
    assert response.status_code == 404


async def test_stop_agent_not_found(client: AsyncClient) -> None:
    """POST /api/agent/stop/{id} returns 404 for unknown ID."""
    response = await client.post("/api/agent/stop/nonexistent-id")
    assert response.status_code == 404


async def test_stop_agent_not_running(client: AsyncClient) -> None:
    """POST /api/agent/stop returns 400 when agent is not running."""
    # Create task and start run (status will be PENDING)
    task_response = await client.post("/api/tasks", json={"title": "Stop Test"})
    task_id = task_response.json()["id"]

    run_response = await client.post("/api/agent/run", json={"task_id": task_id})
    run_id = run_response.json()["id"]

    # Try to stop a PENDING agent (not RUNNING)
    response = await client.post(f"/api/agent/stop/{run_id}")
    assert response.status_code == 400
    assert "not running" in response.json()["detail"]


async def test_list_agent_runs_with_filters(client: AsyncClient) -> None:
    """GET /api/agent/runs with filter parameters."""
    # Create two tasks and start runs
    task1_response = await client.post("/api/tasks", json={"title": "Filter Test 1"})
    task1_id = task1_response.json()["id"]

    task2_response = await client.post("/api/tasks", json={"title": "Filter Test 2"})
    task2_id = task2_response.json()["id"]

    await client.post("/api/agent/run", json={"task_id": task1_id})
    await client.post("/api/agent/run", json={"task_id": task2_id})

    # Filter by task_id
    response = await client.get(f"/api/agent/runs?task_id={task1_id}")
    assert response.status_code == 200
    runs = response.json()
    assert len(runs) == 1
    assert runs[0]["task_id"] == task1_id

    # Filter by status
    response = await client.get("/api/agent/runs?status=pending")
    assert response.status_code == 200
    runs = response.json()
    assert len(runs) == 2
    assert all(r["status"] == "pending" for r in runs)


async def test_get_agent_run(client: AsyncClient) -> None:
    """GET /api/agent/runs/{id} returns agent run details."""
    # Create task and start run
    task_response = await client.post("/api/tasks", json={"title": "Get Run Test"})
    task_id = task_response.json()["id"]

    run_response = await client.post("/api/agent/run", json={"task_id": task_id})
    run_id = run_response.json()["id"]

    # Get the run
    response = await client.get(f"/api/agent/runs/{run_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == run_id
    assert data["task_id"] == task_id
    assert data["status"] == "pending"
