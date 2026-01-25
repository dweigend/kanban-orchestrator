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

import shutil
from pathlib import Path
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import EventType, TaskEvent, event_bus
from src.api.schemas import TaskCreate, TaskUpdate
from src.models.task import Task, TaskStatus

# Sandbox output directory base
OUTPUT_DIR = Path("output")


def generate_sandbox_dir(task_id: str) -> str:
    """Generate sandbox directory path for a task."""
    return f"output/{task_id}/"


async def copy_sandbox_to_target(sandbox_dir: str, target_path: str) -> bool:
    """Copy sandbox contents to target path.

    Returns True if successful, False if sandbox is empty or doesn't exist.
    """
    sandbox = Path(sandbox_dir)
    target = Path(target_path)

    if not sandbox.exists():
        return False

    target.mkdir(parents=True, exist_ok=True)

    for item in sandbox.iterdir():
        if item.is_file():
            shutil.copy2(item, target / item.name)
        elif item.is_dir():
            shutil.copytree(item, target / item.name, dirs_exist_ok=True)

    return True


def _task_to_event_data(task: Task) -> dict:
    """Convert task to event payload with all fields.

    Ensures SSE events contain complete task data so frontend
    doesn't lose fields like 'type' or 'description' on updates.
    """
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "result": task.result,
        "status": task.status,
        "type": task.type,
        "project_id": task.project_id,
        "parent_id": task.parent_id,
        "steps": task.steps,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        # Delegation fields (Phase 11B)
        "sandbox_dir": task.sandbox_dir,
        "target_path": task.target_path,
        "read_paths": task.read_paths,
        "allowed_mcps": task.allowed_mcps,
        "template": task.template,
        "source": task.source,
    }


async def create_task(db: AsyncSession, task_data: TaskCreate) -> Task:
    """Create a new task in the database.

    Automatically generates sandbox_dir and creates the directory.
    Publishes task_created event with full task data.
    """
    # Convert steps from Pydantic models to dicts for JSON storage
    steps_input = task_data.steps
    steps_data = [s.model_dump() for s in steps_input] if steps_input else None

    # Generate unique ID and sandbox directory
    task_id = str(uuid4())
    sandbox_dir = generate_sandbox_dir(task_id)

    # Ensure sandbox directory exists
    Path(sandbox_dir).mkdir(parents=True, exist_ok=True)

    task = Task(
        id=task_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        type=task_data.type,
        project_id=task_data.project_id,
        parent_id=task_data.parent_id,
        steps=steps_data,
        # Delegation fields (Phase 11B)
        sandbox_dir=sandbox_dir,
        target_path=task_data.target_path,
        read_paths=task_data.read_paths,
        allowed_mcps=task_data.allowed_mcps,
        template=task_data.template,
        source=task_data.source,
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

    Copy-to-target: When status changes to DONE and target_path is set,
    copies sandbox contents to target directory.

    Returns:
        Updated task or None if not found.
    """
    task = await get_task(db, task_id)
    if not task:
        return None

    # Track status change for copy-to-target
    old_status = task.status

    # Apply only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        # Convert steps Pydantic models to dicts for JSON storage
        if field == "steps" and value is not None:
            value = [step if isinstance(step, dict) else step for step in value]
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    # Copy to target when transitioning to DONE (if target_path is set)
    new_status = task.status
    if (
        old_status != TaskStatus.DONE
        and new_status == TaskStatus.DONE
        and task.target_path
        and task.sandbox_dir
    ):
        await copy_sandbox_to_target(task.sandbox_dir, task.target_path)

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
