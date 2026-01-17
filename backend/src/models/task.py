"""SQLAlchemy Task model for database persistence."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.agent_run import AgentRun
    from src.models.project import Project


class TaskStatus(StrEnum):
    """Valid task statuses for Kanban workflow."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    NEEDS_REVIEW = "needs_review"
    DONE = "done"


class TaskType(StrEnum):
    """Task type categories for visual distinction."""

    RESEARCH = "research"
    DEV = "dev"
    NOTES = "notes"
    NEUTRAL = "neutral"


class Task(Base):
    """Task model with project association and agent support."""

    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)  # Agent result
    status: Mapped[str] = mapped_column(String(20), default=TaskStatus.TODO)
    type: Mapped[str] = mapped_column(String(20), default=TaskType.NEUTRAL)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Project association
    project_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=True
    )

    # Sub-task support
    parent_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("tasks.id"), nullable=True
    )

    # Relationships
    project: Mapped[Project | None] = relationship("Project", back_populates="tasks")
    parent: Mapped[Task | None] = relationship(
        "Task", remote_side="Task.id", back_populates="subtasks"
    )
    subtasks: Mapped[list[Task]] = relationship("Task", back_populates="parent")
    agent_runs: Mapped[list[AgentRun]] = relationship(
        "AgentRun", back_populates="task", cascade="all, delete-orphan"
    )
