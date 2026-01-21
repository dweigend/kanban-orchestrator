"""Pydantic schemas for API request/response validation.

This module defines all API contracts between frontend and backend.
Schemas are designed for both API validation AND LLM structured output.

Design Principles:
- Every field has a description (LLMs use these for understanding)
- Examples provided via json_schema_extra (helps LLM generation)
- Validators for business logic
- from_attributes=True for ORM model conversion

Schemas by domain:
- Project: ProjectCreate, ProjectUpdate, ProjectResponse
- Task: TaskCreate, TaskUpdate, TaskResponse
- AgentRun: AgentRunCreate, AgentRunResponse

IMPORTANT: Keep these schemas in sync with:
- Backend models: src/models/*.py
- Frontend types: frontend/src/lib/types/*.ts
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from src.models.agent_run import AgentRunStatus
from src.models.task import TaskStatus, TaskType


# ─────────────────────────────────────────────────────────────
# Project Schemas
# ─────────────────────────────────────────────────────────────


class ProjectCreate(BaseModel):
    """Create a new project workspace for task organization."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable project name",
        examples=["My Research Project", "Web App Development"],
    )
    workspace_path: str = Field(
        ...,
        min_length=1,
        max_length=1024,
        description="Absolute filesystem path to the project workspace directory",
        examples=["/home/user/projects/my-app", "/Users/dev/workspace"],
    )


class ProjectUpdate(BaseModel):
    """Update an existing project. Only provided fields will be modified."""

    name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="New project name",
    )
    workspace_path: str | None = Field(
        None,
        min_length=1,
        max_length=1024,
        description="New workspace path",
    )


class ProjectResponse(BaseModel):
    """Project data returned by API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Unique project identifier (UUID)")
    name: str = Field(description="Human-readable project name")
    workspace_path: str = Field(description="Filesystem path to project workspace")
    created_at: datetime = Field(description="Project creation timestamp (ISO 8601)")


# ─────────────────────────────────────────────────────────────
# Task Schemas
# ─────────────────────────────────────────────────────────────


class TaskCreate(BaseModel):
    """Create a new task on the Kanban board.

    Tasks represent work items that can be processed by AI agents.
    Each task has a type (research/dev/notes) and moves through
    status columns (todo → in_progress → done).
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Research Kanban methodologies",
                    "description": "Find best practices for Kanban in software teams",
                    "type": "research",
                },
                {
                    "title": "Implement user authentication",
                    "description": "Add JWT-based auth to the API",
                    "type": "dev",
                    "status": "todo",
                },
            ]
        }
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Brief task title displayed on the Kanban card",
        examples=["Research AI agents", "Fix login bug", "Write documentation"],
    )
    description: str | None = Field(
        None,
        description="Detailed task description with context and requirements",
        examples=["Investigate how AI agents can automate research tasks..."],
    )
    status: TaskStatus = Field(
        TaskStatus.TODO,
        description="Initial Kanban column: todo, in_progress, needs_review, or done",
    )
    type: TaskType = Field(
        TaskType.NEUTRAL,
        description="Task category for visual distinction: research, dev, notes, or neutral",
    )
    project_id: str | None = Field(
        None,
        description="UUID of parent project (optional)",
    )
    parent_id: str | None = Field(
        None,
        description="UUID of parent task for subtask hierarchy (optional)",
    )


class TaskUpdate(BaseModel):
    """Update an existing task. Only provided fields will be modified."""

    title: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="New task title",
    )
    description: str | None = Field(
        None,
        description="New task description",
    )
    status: TaskStatus | None = Field(
        None,
        description="New Kanban status: todo, in_progress, needs_review, or done",
    )
    type: TaskType | None = Field(
        None,
        description="New task type: research, dev, notes, or neutral",
    )


class TaskResponse(BaseModel):
    """Task data returned by API endpoints.

    This is the canonical task format used across the system.
    The result field contains AI agent output after task completion.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Unique task identifier (UUID)")
    title: str = Field(description="Brief task title displayed on Kanban card")
    description: str | None = Field(
        description="Detailed task description with context and requirements"
    )
    result: str | None = Field(
        description="AI agent output/result after task completion (populated by agent)"
    )
    status: TaskStatus = Field(
        description="Current Kanban column: todo, in_progress, needs_review, or done"
    )
    type: TaskType = Field(
        description="Task category: research, dev, notes, or neutral"
    )
    project_id: str | None = Field(description="Parent project UUID (if assigned)")
    parent_id: str | None = Field(description="Parent task UUID (for subtasks)")
    created_at: datetime = Field(description="Task creation timestamp (ISO 8601)")


# ─────────────────────────────────────────────────────────────
# Agent Run Schemas
# ─────────────────────────────────────────────────────────────


class AgentRunCreate(BaseModel):
    """Start an AI agent run for a specific task.

    The agent will process the task and populate the result field.
    """

    task_id: str = Field(
        ...,
        description="UUID of the task to process",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class AgentRunResponse(BaseModel):
    """Agent run status and metadata returned by API endpoints.

    Lifecycle: pending → running → completed/failed/cancelled
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Unique run identifier (UUID)")
    task_id: str = Field(description="UUID of the associated task")
    created_at: datetime = Field(description="Run creation timestamp (ISO 8601)")
    status: AgentRunStatus = Field(
        description="Current run status: pending, running, completed, failed, or cancelled"
    )
    logs: str | None = Field(
        description="JSON string of agent log entries (for debugging)"
    )
    error_message: str | None = Field(description="Error details if status is 'failed'")
    started_at: datetime | None = Field(
        description="Timestamp when agent started running (None if pending)"
    )
    completed_at: datetime | None = Field(
        description="Timestamp when run finished (any terminal state)"
    )


# ─────────────────────────────────────────────────────────────
# Schema Metadata (for dynamic frontend rendering)
# ─────────────────────────────────────────────────────────────


class FieldType(StrEnum):
    """UI rendering hints for form fields."""

    TEXT = "text"
    TEXTAREA = "textarea"
    SELECT = "select"
    READONLY = "readonly"
    DATETIME = "datetime"


class SchemaField(BaseModel):
    """Field definition for dynamic form rendering."""

    name: str = Field(description="Field identifier matching the API field name")
    type: FieldType = Field(description="UI component type for rendering")
    required: bool = Field(default=False, description="Whether field is required")
    description: str = Field(default="", description="Help text for the field")
    options: list[str] | None = Field(
        default=None, description="Valid values for select fields"
    )


class EntitySchema(BaseModel):
    """Schema definition for an entity type (Task, Project, AgentRun)."""

    fields: list[SchemaField] = Field(description="Ordered list of field definitions")


# ─────────────────────────────────────────────────────────────
# Enum Option Schemas (for schema-driven UI)
# ─────────────────────────────────────────────────────────────


class EnumOption(BaseModel):
    """Base enum option with value and label."""

    value: str = Field(description="Enum value used in API")
    label: str = Field(description="Human-readable display label")


class TaskStatusOption(EnumOption):
    """Task status with description for tooltips."""

    description: str = Field(description="Status description for tooltips")


class TaskTypeOption(EnumOption):
    """Task type with icon and prefix for UI rendering."""

    icon: str = Field(description="Phosphor icon name")
    prefix: str = Field(description="Short prefix for task IDs (e.g., RES, DEV)")


class AgentRunStatusOption(EnumOption):
    """Agent run status option."""

    pass


class EnumsResponse(BaseModel):
    """Response containing all enum options with metadata."""

    task_status: list[TaskStatusOption] = Field(
        description="Task status options for Kanban columns"
    )
    task_type: list[TaskTypeOption] = Field(description="Task type options with icons")
    agent_run_status: list[AgentRunStatusOption] = Field(
        description="Agent run status options"
    )
