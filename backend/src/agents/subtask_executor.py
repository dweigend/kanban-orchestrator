"""Sequential subtask execution logic."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.agent_run import AgentRun, AgentRunStatus
from src.models.task import Task, TaskStatus

from .executor import _publish_task_update, execute_agent_run

if TYPE_CHECKING:
    from src.models.project import Project


async def execute_subtasks_sequentially(
    db: AsyncSession,
    parent_task: Task,
    project: Project | None,
) -> None:
    """Execute all subtasks of a parent task one by one.

    Called after user approves the plan.
    """
    # Fetch all subtasks
    result = await db.execute(
        select(Task)
        .where(Task.parent_id == parent_task.id)
        .order_by(Task.created_at.asc())
    )
    subtasks = list(result.scalars().all())

    if not subtasks:
        return

    # Update parent to IN_PROGRESS
    parent_task.status = TaskStatus.IN_PROGRESS
    await db.commit()
    await _publish_task_update(parent_task)

    # Execute each subtask
    for subtask in subtasks:
        # Create agent run for this subtask
        agent_run = AgentRun(
            id=str(uuid4()),
            task_id=subtask.id,
            status=AgentRunStatus.PENDING,
        )
        db.add(agent_run)
        await db.commit()
        await db.refresh(agent_run)

        # Execute the subtask
        await execute_agent_run(db, agent_run, subtask, project)

        # Refresh subtask to get updated status
        await db.refresh(subtask)

    # Check if all subtasks completed successfully
    result = await db.execute(select(Task).where(Task.parent_id == parent_task.id))
    all_subtasks = list(result.scalars().all())
    all_done = all(t.status == TaskStatus.DONE for t in all_subtasks)

    # Update parent status
    parent_task.status = TaskStatus.DONE if all_done else TaskStatus.NEEDS_REVIEW
    await db.commit()
    await _publish_task_update(parent_task)
