"""Task planning and decomposition logic."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import EventType, TaskEvent, event_bus
from src.models.task import Task, TaskStatus

from .executor import _publish_task_update

if TYPE_CHECKING:
    from src.models.project import Project


async def _create_placeholder_subtasks(
    parent: Task,
    db: AsyncSession,
) -> list[Task]:
    """Create Setup/Implement/Finalize subtasks for a parent task."""
    subtask_plans = [
        {
            "title": f"Setup for: {parent.title}",
            "description": "Initial setup and configuration",
            "steps": [
                {"text": "Analyze requirements", "done": False},
                {"text": "Set up environment", "done": False},
            ],
        },
        {
            "title": f"Implement: {parent.title}",
            "description": "Core implementation work",
            "steps": [
                {"text": "Write implementation", "done": False},
                {"text": "Add error handling", "done": False},
                {"text": "Test locally", "done": False},
            ],
        },
        {
            "title": f"Finalize: {parent.title}",
            "description": "Cleanup and documentation",
            "steps": [
                {"text": "Add documentation", "done": False},
                {"text": "Final review", "done": False},
            ],
        },
    ]

    created_subtasks: list[Task] = []
    for plan in subtask_plans:
        subtask = Task(
            id=str(uuid4()),
            title=plan["title"],
            description=plan["description"],
            status=TaskStatus.TODO,
            type=parent.type,
            project_id=parent.project_id,
            parent_id=parent.id,
            steps=plan["steps"],
        )
        db.add(subtask)
        created_subtasks.append(subtask)

    return created_subtasks


def _build_planning_prompt(task: Task, project: Project | None) -> str:
    """Build the prompt for task decomposition."""
    parts = [f"# Task to Decompose: {task.title}"]

    if task.description:
        parts.append(f"\n## Description\n{task.description}")

    if project:
        parts.append(f"\n## Workspace\n{project.workspace_path}")

    parts.append("\n## Instructions")
    parts.append(
        "Break this task into 2-5 subtasks. Each subtask should be:\n"
        "- A concrete, actionable piece of work\n"
        "- Completable by an AI agent\n"
        "- Include 2-5 specific implementation steps\n\n"
        "Return a structured decomposition with subtasks and steps."
    )

    return "\n".join(parts)


async def plan_task_decomposition(
    db: AsyncSession,
    task: Task,
    project: Project | None,
) -> list[Task]:
    """Use Claude to decompose a task into subtasks.

    Creates real Task entities with parent_id set to the original task.
    Sets parent task status to NEEDS_REVIEW for user approval.
    """
    # Update parent task status to show planning is in progress
    task.status = TaskStatus.IN_PROGRESS
    await db.commit()
    await _publish_task_update(task)

    # TODO: Future - Use Claude SDK structured output for intelligent decomposition
    # For now, create a template-based decomposition
    created_subtasks = await _create_placeholder_subtasks(task, db)

    # Update parent status to NEEDS_REVIEW
    task.status = TaskStatus.NEEDS_REVIEW
    await db.commit()

    # Publish events for all created subtasks
    for subtask in created_subtasks:
        await db.refresh(subtask)
        await event_bus.publish(
            TaskEvent(
                event_type=EventType.TASK_CREATED,
                data={
                    "id": subtask.id,
                    "title": subtask.title,
                    "description": subtask.description,
                    "result": subtask.result,
                    "status": subtask.status,
                    "type": subtask.type,
                    "project_id": subtask.project_id,
                    "parent_id": subtask.parent_id,
                    "steps": subtask.steps,
                    "created_at": (
                        subtask.created_at.isoformat() if subtask.created_at else None
                    ),
                },
            )
        )

    # Publish parent update
    await _publish_task_update(task)

    return created_subtasks
