"""Agent API endpoint tests."""

import pytest
from httpx import AsyncClient


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


@pytest.mark.skip(reason="Background task uses separate DB connection, causes hang")
async def test_start_agent_run(client: AsyncClient) -> None:
    """POST /api/agent/run returns 202 for valid task.

    Note: Background task execution is not tested here as it uses a separate
    DB connection. Integration tests would be needed for full flow testing.
    """
    # Create task first
    task_response = await client.post("/api/tasks", json={"title": "Agent Test"})
    task_id = task_response.json()["id"]

    response = await client.post("/api/agent/run", json={"task_id": task_id})
    # Background task may fail due to separate DB connection in tests,
    # but the HTTP response should still be correct
    assert response.status_code == 202
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "pending"
    assert data["id"] == "pending"  # Placeholder until background task creates real run


async def test_get_agent_run_not_found(client: AsyncClient) -> None:
    """GET /api/agent/runs/{id} returns 404 for unknown ID."""
    response = await client.get("/api/agent/runs/nonexistent-id")
    assert response.status_code == 404


async def test_stop_agent_not_found(client: AsyncClient) -> None:
    """POST /api/agent/stop/{id} returns 404 for unknown ID."""
    response = await client.post("/api/agent/stop/nonexistent-id")
    assert response.status_code == 404
