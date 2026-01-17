"""Task API endpoint tests."""

from httpx import AsyncClient


async def test_create_task(client: AsyncClient) -> None:
    """POST /api/tasks creates a new task."""
    response = await client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "todo"
    assert "id" in data


async def test_create_task_minimal(client: AsyncClient) -> None:
    """POST /api/tasks with only required fields."""
    response = await client.post("/api/tasks", json={"title": "Minimal"})
    assert response.status_code == 201
    assert response.json()["description"] is None


async def test_create_task_validation_error(client: AsyncClient) -> None:
    """POST /api/tasks rejects empty title."""
    response = await client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


async def test_list_tasks_empty(client: AsyncClient) -> None:
    """GET /api/tasks returns empty list initially."""
    response = await client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


async def test_list_tasks(client: AsyncClient) -> None:
    """GET /api/tasks returns all tasks."""
    await client.post("/api/tasks", json={"title": "Task 1"})
    await client.post("/api/tasks", json={"title": "Task 2"})

    response = await client.get("/api/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_task(client: AsyncClient) -> None:
    """GET /api/tasks/{id} returns single task."""
    create_response = await client.post("/api/tasks", json={"title": "Get Me"})
    task_id = create_response.json()["id"]

    response = await client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"


async def test_get_task_not_found(client: AsyncClient) -> None:
    """GET /api/tasks/{id} returns 404 for unknown ID."""
    response = await client.get("/api/tasks/nonexistent-id")
    assert response.status_code == 404


async def test_update_task(client: AsyncClient) -> None:
    """PUT /api/tasks/{id} updates task fields."""
    create_response = await client.post("/api/tasks", json={"title": "Original"})
    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "status": "in_progress"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["status"] == "in_progress"


async def test_update_task_not_found(client: AsyncClient) -> None:
    """PUT /api/tasks/{id} returns 404 for unknown ID."""
    response = await client.put(
        "/api/tasks/nonexistent-id",
        json={"title": "Nope"},
    )
    assert response.status_code == 404


async def test_delete_task(client: AsyncClient) -> None:
    """DELETE /api/tasks/{id} removes task."""
    create_response = await client.post("/api/tasks", json={"title": "Delete Me"})
    task_id = create_response.json()["id"]

    response = await client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = await client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


async def test_delete_task_not_found(client: AsyncClient) -> None:
    """DELETE /api/tasks/{id} returns 404 for unknown ID."""
    response = await client.delete("/api/tasks/nonexistent-id")
    assert response.status_code == 404
