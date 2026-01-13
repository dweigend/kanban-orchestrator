"""Task CRUD operations with async SQLAlchemy."""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import EventType, TaskEvent, event_bus
from src.api.schemas import TaskCreate, TaskUpdate
from src.models.task import Task


async def create_task(db: AsyncSession, task_data: TaskCreate) -> Task:
    """Create a new task in the database."""
    task = Task(
        id=str(uuid4()),
        title=task_data.title,
        status=task_data.status,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    await event_bus.publish(
        TaskEvent(
            event_type=EventType.TASK_CREATED,
            data={"id": task.id, "title": task.title, "status": task.status},
        )
    )
    return task


async def get_task(db: AsyncSession, task_id: str) -> Task | None:
    """Get a single task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def get_all_tasks(db: AsyncSession) -> list[Task]:
    """Get all tasks ordered by creation date."""
    result = await db.execute(select(Task).order_by(Task.created_at.desc()))
    return list(result.scalars().all())


async def update_task(
    db: AsyncSession,
    task_id: str,
    task_data: TaskUpdate,
) -> Task | None:
    """Update an existing task. Returns None if not found."""
    task = await get_task(db, task_id)
    if not task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    await event_bus.publish(
        TaskEvent(
            event_type=EventType.TASK_UPDATED,
            data={"id": task.id, "title": task.title, "status": task.status},
        )
    )
    return task


async def delete_task(db: AsyncSession, task_id: str) -> bool:
    """Delete a task. Returns True if deleted, False if not found."""
    task = await get_task(db, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()

    await event_bus.publish(
        TaskEvent(
            event_type=EventType.TASK_DELETED,
            data={"id": task_id},
        )
    )
    return True
