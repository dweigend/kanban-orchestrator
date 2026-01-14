"""Pydantic schemas for API request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field

from src.models.agent_run import AgentRunStatus
from src.models.task import TaskStatus


# --- Project Schemas ---


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


# --- Task Schemas ---


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    project_id: str | None = None
    parent_id: str | None = None


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None


class TaskResponse(BaseModel):
    """Schema for task API responses."""

    id: str
    title: str
    description: str | None
    status: TaskStatus
    project_id: str | None
    parent_id: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Agent Run Schemas ---


class AgentRunCreate(BaseModel):
    """Schema for starting an agent run."""

    task_id: str


class AgentRunResponse(BaseModel):
    """Schema for agent run API responses."""

    id: str
    task_id: str
    status: AgentRunStatus
    error_message: str | None
    started_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}
