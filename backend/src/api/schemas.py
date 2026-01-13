"""Pydantic schemas for API request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field

from src.models.task import TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=255)
    status: TaskStatus = TaskStatus.TODO


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: str | None = Field(None, min_length=1, max_length=255)
    status: TaskStatus | None = None


class TaskResponse(BaseModel):
    """Schema for task API responses."""

    id: str
    title: str
    status: TaskStatus
    created_at: datetime

    model_config = {"from_attributes": True}
