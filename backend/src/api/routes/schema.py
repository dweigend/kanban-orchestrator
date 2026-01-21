"""Schema API endpoints for dynamic frontend rendering."""

from fastapi import APIRouter

from src.api.schemas import (
    AgentRunStatusOption,
    EntitySchema,
    EnumsResponse,
    FieldType,
    SchemaField,
    TaskStatusOption,
    TaskTypeOption,
)
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


@router.get("/enums", response_model=EnumsResponse)
def get_all_enums() -> EnumsResponse:
    """Returns all enum values with metadata for UI rendering."""
    return EnumsResponse(
        task_status=[
            TaskStatusOption(
                value="todo",
                label="To Do",
                description="Task nicht gestartet",
            ),
            TaskStatusOption(
                value="in_progress",
                label="In Progress",
                description="Task wird bearbeitet",
            ),
            TaskStatusOption(
                value="needs_review",
                label="Needs Review",
                description="Wartet auf Review",
            ),
            TaskStatusOption(
                value="done",
                label="Done",
                description="Task abgeschlossen",
            ),
        ],
        task_type=[
            TaskTypeOption(
                value="research",
                label="Research",
                icon="MagnifyingGlass",
                prefix="RES",
            ),
            TaskTypeOption(
                value="dev",
                label="Development",
                icon="Code",
                prefix="DEV",
            ),
            TaskTypeOption(
                value="notes",
                label="Notes",
                icon="Note",
                prefix="NOTE",
            ),
            TaskTypeOption(
                value="neutral",
                label="General",
                icon="Chat",
                prefix="GEN",
            ),
        ],
        agent_run_status=[
            AgentRunStatusOption(value="pending", label="Pending"),
            AgentRunStatusOption(value="running", label="Running"),
            AgentRunStatusOption(value="needs_review", label="Needs Review"),
            AgentRunStatusOption(value="completed", label="Completed"),
            AgentRunStatusOption(value="failed", label="Failed"),
            AgentRunStatusOption(value="cancelled", label="Cancelled"),
        ],
    )
