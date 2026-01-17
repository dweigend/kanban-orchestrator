"""Project API endpoint tests."""

from httpx import AsyncClient


async def test_create_project(client: AsyncClient) -> None:
    """POST /api/projects creates a new project."""
    response = await client.post(
        "/api/projects",
        json={"name": "Test Project", "workspace_path": "/tmp/test"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["workspace_path"] == "/tmp/test"
    assert "id" in data


async def test_create_project_validation_error(client: AsyncClient) -> None:
    """POST /api/projects rejects empty name."""
    response = await client.post(
        "/api/projects",
        json={"name": "", "workspace_path": "/tmp"},
    )
    assert response.status_code == 422


async def test_list_projects_empty(client: AsyncClient) -> None:
    """GET /api/projects returns empty list initially."""
    response = await client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []


async def test_list_projects(client: AsyncClient) -> None:
    """GET /api/projects returns all projects."""
    await client.post(
        "/api/projects",
        json={"name": "Project 1", "workspace_path": "/tmp/p1"},
    )
    await client.post(
        "/api/projects",
        json={"name": "Project 2", "workspace_path": "/tmp/p2"},
    )

    response = await client.get("/api/projects")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_project(client: AsyncClient) -> None:
    """GET /api/projects/{id} returns single project."""
    create_response = await client.post(
        "/api/projects",
        json={"name": "Get Me", "workspace_path": "/tmp/get"},
    )
    project_id = create_response.json()["id"]

    response = await client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Get Me"


async def test_get_project_not_found(client: AsyncClient) -> None:
    """GET /api/projects/{id} returns 404 for unknown ID."""
    response = await client.get("/api/projects/nonexistent-id")
    assert response.status_code == 404


async def test_update_project(client: AsyncClient) -> None:
    """PUT /api/projects/{id} updates project fields."""
    create_response = await client.post(
        "/api/projects",
        json={"name": "Original", "workspace_path": "/tmp/orig"},
    )
    project_id = create_response.json()["id"]

    response = await client.put(
        f"/api/projects/{project_id}",
        json={"name": "Updated"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


async def test_update_project_not_found(client: AsyncClient) -> None:
    """PUT /api/projects/{id} returns 404 for unknown ID."""
    response = await client.put(
        "/api/projects/nonexistent-id",
        json={"name": "Nope"},
    )
    assert response.status_code == 404


async def test_delete_project(client: AsyncClient) -> None:
    """DELETE /api/projects/{id} removes project."""
    create_response = await client.post(
        "/api/projects",
        json={"name": "Delete Me", "workspace_path": "/tmp/del"},
    )
    project_id = create_response.json()["id"]

    response = await client.delete(f"/api/projects/{project_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = await client.get(f"/api/projects/{project_id}")
    assert get_response.status_code == 404


async def test_delete_project_not_found(client: AsyncClient) -> None:
    """DELETE /api/projects/{id} returns 404 for unknown ID."""
    response = await client.delete("/api/projects/nonexistent-id")
    assert response.status_code == 404
