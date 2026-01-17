"""Schema API endpoints for dynamic frontend rendering."""

from fastapi import APIRouter

from src.api.schemas import EntitySchema, FieldType, SchemaField
from src.models.agent_run import AgentRunStatus
from src.models.task import TaskStatus, TaskType

router = APIRouter(prefix="/api/schema", tags=["schema"])


@router.get("/task", response_model=EntitySchema)
def get_task_schema() -> EntitySchema:
    """Returns field definitions for Task forms."""
    return EntitySchema(
        fields=[
            SchemaField(
                name="title",
                type=FieldType.TEXT,
                required=True,
                description="Brief task title displayed on the Kanban card",
            ),
            SchemaField(
                name="description",
                type=FieldType.TEXTAREA,
                description="Detailed task description with context and requirements",
            ),
            SchemaField(
                name="status",
                type=FieldType.SELECT,
                options=[s.value for s in TaskStatus],
                description="Kanban column position",
            ),
            SchemaField(
                name="type",
                type=FieldType.SELECT,
                options=[t.value for t in TaskType],
                description="Task category for visual distinction",
            ),
            SchemaField(
                name="result",
                type=FieldType.READONLY,
                description="AI agent output after task completion",
            ),
            SchemaField(
                name="created_at",
                type=FieldType.DATETIME,
                description="Task creation timestamp",
            ),
        ]
    )


@router.get("/project", response_model=EntitySchema)
def get_project_schema() -> EntitySchema:
    """Returns field definitions for Project forms."""
    return EntitySchema(
        fields=[
            SchemaField(
                name="name",
                type=FieldType.TEXT,
                required=True,
                description="Human-readable project name",
            ),
            SchemaField(
                name="workspace_path",
                type=FieldType.TEXT,
                required=True,
                description="Absolute filesystem path to the project workspace",
            ),
            SchemaField(
                name="created_at",
                type=FieldType.DATETIME,
                description="Project creation timestamp",
            ),
        ]
    )


@router.get("/agent-run", response_model=EntitySchema)
def get_agent_run_schema() -> EntitySchema:
    """Returns field definitions for AgentRun display."""
    return EntitySchema(
        fields=[
            SchemaField(
                name="status",
                type=FieldType.SELECT,
                options=[s.value for s in AgentRunStatus],
                description="Current run status",
            ),
            SchemaField(
                name="error_message",
                type=FieldType.READONLY,
                description="Error details if status is 'failed'",
            ),
            SchemaField(
                name="logs",
                type=FieldType.READONLY,
                description="Agent log entries for debugging",
            ),
            SchemaField(
                name="created_at",
                type=FieldType.DATETIME,
                description="Run creation timestamp",
            ),
            SchemaField(
                name="started_at",
                type=FieldType.DATETIME,
                description="Timestamp when agent started running",
            ),
            SchemaField(
                name="completed_at",
                type=FieldType.DATETIME,
                description="Timestamp when run finished",
            ),
        ]
    )


@router.get("/enums")
def get_all_enums() -> dict[str, list[str]]:
    """Returns all enum values for dropdowns and validation."""
    return {
        "task_status": [s.value for s in TaskStatus],
        "task_type": [t.value for t in TaskType],
        "agent_run_status": [s.value for s in AgentRunStatus],
    }
