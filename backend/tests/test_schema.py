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
    """GET /api/schema/enums returns all enum values with metadata."""
    response = await client.get("/api/schema/enums")
    assert response.status_code == 200

    data = response.json()

    # All enum types are present
    assert "task_status" in data
    assert "task_type" in data
    assert "agent_run_status" in data

    # Values match Python enums (extract values from objects)
    status_values = {opt["value"] for opt in data["task_status"]}
    type_values = {opt["value"] for opt in data["task_type"]}
    run_status_values = {opt["value"] for opt in data["agent_run_status"]}

    assert status_values == {s.value for s in TaskStatus}
    assert type_values == {t.value for t in TaskType}
    assert run_status_values == {s.value for s in AgentRunStatus}


async def test_get_enums_has_labels(client: AsyncClient) -> None:
    """Enum options have human-readable labels."""
    response = await client.get("/api/schema/enums")
    data = response.json()

    # All options have value and label
    for status in data["task_status"]:
        assert "value" in status
        assert "label" in status
        assert "description" in status

    for task_type in data["task_type"]:
        assert "value" in task_type
        assert "label" in task_type
        assert "icon" in task_type
        assert "prefix" in task_type

    for run_status in data["agent_run_status"]:
        assert "value" in run_status
        assert "label" in run_status


async def test_get_enums_task_type_metadata(client: AsyncClient) -> None:
    """Task type options have icon and prefix for UI rendering."""
    response = await client.get("/api/schema/enums")
    data = response.json()

    # Check specific task type has expected metadata
    research_type = next(t for t in data["task_type"] if t["value"] == "research")
    assert research_type["label"] == "Research"
    assert research_type["icon"] == "MagnifyingGlass"
    assert research_type["prefix"] == "RES"

    dev_type = next(t for t in data["task_type"] if t["value"] == "dev")
    assert dev_type["label"] == "Development"
    assert dev_type["icon"] == "Code"
    assert dev_type["prefix"] == "DEV"


async def test_schema_fields_have_descriptions(client: AsyncClient) -> None:
    """All schema fields have non-empty descriptions."""
    response = await client.get("/api/schema/task")
    data = response.json()

    for field in data["fields"]:
        assert "description" in field
        assert len(field["description"]) > 0, (
            f"Field {field['name']} has empty description"
        )
