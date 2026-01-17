"""Task CRUD operations with async SQLAlchemy.

This module provides database operations for tasks and publishes
events via SSE for real-time frontend updates.

Functions:
    create_task: Create new task and publish creation event
    get_task: Retrieve single task by ID
    get_all_tasks: List all tasks (descending by creation date)
    update_task: Update task fields and publish update event
    delete_task: Remove task and publish deletion event

Events published (via event_bus):
    - task_created: Full task data on creation
    - task_updated: Full task data on update
    - task_deleted: Task ID on deletion
"""

from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import EventType, TaskEvent, event_bus
from src.api.schemas import TaskCreate, TaskUpdate
from src.models.task import Task


def _task_to_event_data(task: Task) -> dict:
    """Convert task to event payload with all fields.

    Ensures SSE events contain complete task data so frontend
    doesn't lose fields like 'type' or 'description' on updates.
    """
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "type": task.type,
        "project_id": task.project_id,
        "parent_id": task.parent_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
    }


async def create_task(db: AsyncSession, task_data: TaskCreate) -> Task:
    """Create a new task in the database.

    Publishes task_created event with full task data.
    """
    task = Task(
        id=str(uuid4()),
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        type=task_data.type,
        project_id=task_data.project_id,
        parent_id=task_data.parent_id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    await event_bus.publish(
        TaskEvent(
            event_type=EventType.TASK_CREATED,
            data=_task_to_event_data(task),
        )
    )
    return task


async def get_task(db: AsyncSession, task_id: str) -> Task | None:
    """Get a single task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def get_all_tasks(db: AsyncSession) -> list[Task]:
    """Get all tasks ordered by creation date (newest first)."""
    result = await db.execute(select(Task).order_by(Task.created_at.desc()))
    return list(result.scalars().all())


async def update_task(
    db: AsyncSession,
    task_id: str,
    task_data: TaskUpdate,
) -> Task | None:
    """Update an existing task.

    Only updates fields that are explicitly provided (non-None).
    Publishes task_updated event with full task data.

    Returns:
        Updated task or None if not found.
    """
    task = await get_task(db, task_id)
    if not task:
        return None

    # Apply only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    await event_bus.publish(
        TaskEvent(
            event_type=EventType.TASK_UPDATED,
            data=_task_to_event_data(task),
        )
    )
    return task


async def delete_task(db: AsyncSession, task_id: str) -> bool:
    """Delete a task by ID.

    Uses SQLAlchemy 2.0 delete statement pattern.
    Publishes task_deleted event.

    Returns:
        True if deleted, False if task not found.
    """
    # Check existence first (for return value)
    task = await get_task(db, task_id)
    if not task:
        return False

    # Delete using statement (SQLAlchemy 2.0 pattern)
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()

    await event_bus.publish(
        TaskEvent(
            event_type=EventType.TASK_DELETED,
            data={"id": task_id},
        )
    )
    return True
