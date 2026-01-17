"""Schema API endpoint tests."""

from httpx import AsyncClient

from src.models.agent_run import AgentRunStatus
from src.models.task import TaskStatus, TaskType


async def test_get_task_schema(client: AsyncClient) -> None:
    """GET /api/schema/task returns task field definitions."""
    response = await client.get("/api/schema/task")
    assert response.status_code == 200

    data = response.json()
    assert "fields" in data

    # Check required fields are present
    field_names = [f["name"] for f in data["fields"]]
    assert "title" in field_names
    assert "description" in field_names
    assert "status" in field_names
    assert "type" in field_names
    assert "result" in field_names
    assert "created_at" in field_names


async def test_get_task_schema_field_types(client: AsyncClient) -> None:
    """Task schema fields have correct types."""
    response = await client.get("/api/schema/task")
    data = response.json()

    fields_by_name = {f["name"]: f for f in data["fields"]}

    assert fields_by_name["title"]["type"] == "text"
    assert fields_by_name["title"]["required"] is True

    assert fields_by_name["description"]["type"] == "textarea"
    assert fields_by_name["status"]["type"] == "select"
    assert fields_by_name["result"]["type"] == "readonly"
    assert fields_by_name["created_at"]["type"] == "datetime"


async def test_get_task_schema_select_options(client: AsyncClient) -> None:
    """Task schema select fields include valid options."""
    response = await client.get("/api/schema/task")
    data = response.json()

    fields_by_name = {f["name"]: f for f in data["fields"]}

    # Status options match TaskStatus enum
    status_options = fields_by_name["status"]["options"]
    assert set(status_options) == {s.value for s in TaskStatus}

    # Type options match TaskType enum
    type_options = fields_by_name["type"]["options"]
    assert set(type_options) == {t.value for t in TaskType}


async def test_get_project_schema(client: AsyncClient) -> None:
    """GET /api/schema/project returns project field definitions."""
    response = await client.get("/api/schema/project")
    assert response.status_code == 200

    data = response.json()
    field_names = [f["name"] for f in data["fields"]]

    assert "name" in field_names
    assert "workspace_path" in field_names
    assert "created_at" in field_names


async def test_get_agent_run_schema(client: AsyncClient) -> None:
    """GET /api/schema/agent-run returns agent run field definitions."""
    response = await client.get("/api/schema/agent-run")
    assert response.status_code == 200

    data = response.json()
    field_names = [f["name"] for f in data["fields"]]

    assert "status" in field_names
    assert "error_message" in field_names
    assert "logs" in field_names
    assert "created_at" in field_names
    assert "started_at" in field_names
    assert "completed_at" in field_names


async def test_get_enums(client: AsyncClient) -> None:
    """GET /api/schema/enums returns all enum values."""
    response = await client.get("/api/schema/enums")
    assert response.status_code == 200

    data = response.json()

    # All enum types are present
    assert "task_status" in data
    assert "task_type" in data
    assert "agent_run_status" in data

    # Values match Python enums
    assert set(data["task_status"]) == {s.value for s in TaskStatus}
    assert set(data["task_type"]) == {t.value for t in TaskType}
    assert set(data["agent_run_status"]) == {s.value for s in AgentRunStatus}


async def test_schema_fields_have_descriptions(client: AsyncClient) -> None:
    """All schema fields have non-empty descriptions."""
    response = await client.get("/api/schema/task")
    data = response.json()

    for field in data["fields"]:
        assert "description" in field
        assert len(field["description"]) > 0, (
            f"Field {field['name']} has empty description"
        )
