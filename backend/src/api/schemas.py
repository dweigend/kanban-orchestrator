"""Pydantic schemas for API request/response validation.

This module defines all API contracts between frontend and backend.
All schemas use `from_attributes=True` to enable ORM model conversion.

Schemas are organized by domain:
- Project: ProjectCreate, ProjectUpdate, ProjectResponse
- Task: TaskCreate, TaskUpdate, TaskResponse
- AgentRun: AgentRunCreate, AgentRunResponse

IMPORTANT: Keep these schemas in sync with:
- Backend models: src/models/*.py
- Frontend types: frontend/src/lib/types/*.ts
"""

from datetime import datetime

from pydantic import BaseModel, Field

from src.models.agent_run import AgentRunStatus
from src.models.task import TaskStatus, TaskType


# ─────────────────────────────────────────────────────────────
# Project Schemas
# ─────────────────────────────────────────────────────────────


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(..., min_length=1, max_length=255)
    workspace_path: str = Field(..., min_length=1, max_length=1024)


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""

    name: str | None = Field(None, min_length=1, max_length=255)
    workspace_path: str | None = Field(None, min_length=1, max_length=1024)


class ProjectResponse(BaseModel):
    """Schema for project API responses."""

    id: str
    name: str
    workspace_path: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────────────
# Task Schemas
# ─────────────────────────────────────────────────────────────


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Fields:
        title: Required task title (1-255 chars)
        description: Optional detailed description
        status: Initial status (default: todo)
        type: Task category for visual distinction (default: neutral)
        project_id: Optional project association
        parent_id: Optional parent task for subtasks
    """

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    type: TaskType = TaskType.NEUTRAL
    project_id: str | None = None
    parent_id: str | None = None


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    All fields are optional - only provided fields will be updated.
    """

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None
    type: TaskType | None = None


class TaskResponse(BaseModel):
    """Schema for task API responses.

    This is the canonical task format returned by all endpoints.
    Keep in sync with frontend Task interface.
    """

    id: str
    title: str
    description: str | None
    result: str | None  # Agent result (temporary until Schema-Driven UI)
    status: TaskStatus
    type: TaskType
    project_id: str | None
    parent_id: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────────────
# Agent Run Schemas
# ─────────────────────────────────────────────────────────────


class AgentRunCreate(BaseModel):
    """Schema for starting an agent run."""

    task_id: str


class AgentRunResponse(BaseModel):
    """Schema for agent run API responses.

    Fields:
        id: Unique run identifier (real UUID, not placeholder)
        task_id: Associated task
        status: Current run status (pending → running → completed/failed/cancelled)
        logs: JSON string of log entries (nullable)
        error_message: Error details if status is 'failed'
        started_at: None for PENDING, set when agent starts RUNNING
        completed_at: Set when run finishes (any terminal state)
    """

    id: str
    task_id: str
    status: AgentRunStatus
    logs: str | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}
