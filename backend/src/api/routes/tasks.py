"""Task CRUD API endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import task_service
from src.api.schemas import TaskCreate, TaskResponse, TaskUpdate
from src.database import get_db
from src.models.task import Task

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Create a new task."""
    task = await task_service.create_task(db, task_data)
    return TaskResponse.model_validate(task)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)) -> list[TaskResponse]:
    """Get all tasks."""
    tasks = await task_service.get_all_tasks(db)
    return [TaskResponse.model_validate(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Get a single task by ID."""
    task = await task_service.get_task(db, task_id)
    if not task:
        logger.warning("Task not found: %s", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Update an existing task."""
    task = await task_service.update_task(db, task_id, task_data)
    if not task:
        logger.warning("Task not found for update: %s", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a task."""
    deleted = await task_service.delete_task(db, task_id)
    if not deleted:
        logger.warning("Task not found for deletion: %s", task_id)
        raise HTTPException(status_code=404, detail="Task not found")


@router.get("/{task_id}/subtasks", response_model=list[TaskResponse])
async def get_subtasks(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> list[TaskResponse]:
    """Get all subtasks of a parent task."""
    # Verify parent task exists
    parent = await task_service.get_task(db, task_id)
    if not parent:
        logger.warning("Parent task not found: %s", task_id)
        raise HTTPException(status_code=404, detail="Parent task not found")

    # Query subtasks
    result = await db.execute(
        select(Task).where(Task.parent_id == task_id).order_by(Task.created_at.asc())
    )
    subtasks = result.scalars().all()
    return [TaskResponse.model_validate(t) for t in subtasks]
