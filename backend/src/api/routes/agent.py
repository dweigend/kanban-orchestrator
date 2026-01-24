"""Agent execution API endpoints."""

import logging
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.orchestrator import (
    execute_agent_run,
    execute_subtasks_sequentially,
    plan_task_decomposition,
    stop_agent_run,
)
from src.api.schemas import AgentRunCreate, AgentRunResponse
from src.database import get_db
from src.models.agent_run import AgentRun, AgentRunStatus
from src.models.project import Project
from src.models.task import Task

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/agent", tags=["agent"])


async def _load_task_and_project(
    task_id: str,
    db: AsyncSession,
) -> tuple[Task, Project | None]:
    """Load task and its project from DB."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise ValueError(f"Task {task_id} not found")

    project = None
    if task.project_id:
        result = await db.execute(select(Project).where(Project.id == task.project_id))
        project = result.scalar_one_or_none()

    return task, project


async def _run_agent_background(
    agent_run_id: str,
    task_id: str,
    mcp_tools: list[str] | None,
) -> None:
    """Background task runner - continues an existing AgentRun."""
    from src.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(AgentRun).where(AgentRun.id == agent_run_id))
        agent_run = result.scalar_one_or_none()
        if not agent_run:
            return

        try:
            task, project = await _load_task_and_project(task_id, db)
        except ValueError:
            return

        await execute_agent_run(db, agent_run, task, project, mcp_tools)


@router.post(
    "/run", response_model=AgentRunResponse, status_code=status.HTTP_202_ACCEPTED
)
async def start_agent_run(
    run_data: AgentRunCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> AgentRunResponse:
    """Start an agent run for a task.

    The agent runs in the background and streams progress via SSE.
    """
    # Fetch task
    result = await db.execute(select(Task).where(Task.id == run_data.task_id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning("Task not found for agent run: %s", run_data.task_id)
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if task already has an active run
    result = await db.execute(
        select(AgentRun).where(
            AgentRun.task_id == run_data.task_id,
            AgentRun.status.in_([AgentRunStatus.PENDING, AgentRunStatus.RUNNING]),
        )
    )
    if result.scalar_one_or_none():
        logger.warning("Task already has active run: %s", run_data.task_id)
        raise HTTPException(
            status_code=409, detail="Task already has an active agent run"
        )

    # Create AgentRun with PENDING status BEFORE background task
    agent_run = AgentRun(
        id=str(uuid4()),
        task_id=task.id,
        status=AgentRunStatus.PENDING,
        started_at=None,  # Will be set when agent starts running
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)

    # Start background task with the real agent_run_id
    background_tasks.add_task(
        _run_agent_background,
        agent_run.id,
        task.id,
        ["filesystem"],  # Default MCP tools
    )

    # Return real AgentRun (not placeholder!)
    return AgentRunResponse.model_validate(agent_run)


@router.post("/stop/{run_id}", status_code=status.HTTP_200_OK)
async def stop_agent(
    run_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Stop a running agent."""
    result = await db.execute(select(AgentRun).where(AgentRun.id == run_id))
    agent_run = result.scalar_one_or_none()
    if not agent_run:
        logger.warning("Agent run not found for stop: %s", run_id)
        raise HTTPException(status_code=404, detail="Agent run not found")

    if agent_run.status != AgentRunStatus.RUNNING:
        logger.warning(
            "Stop requested for non-running agent: %s (status: %s)",
            run_id,
            agent_run.status,
        )
        raise HTTPException(status_code=400, detail="Agent is not running")

    success = await stop_agent_run(db, agent_run)
    return {"success": success, "status": agent_run.status}


@router.get("/runs", response_model=list[AgentRunResponse])
async def list_agent_runs(
    task_id: str | None = None,
    status: AgentRunStatus | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[AgentRunResponse]:
    """List agent runs with optional filters."""
    query = select(AgentRun)

    if task_id:
        query = query.where(AgentRun.task_id == task_id)
    if status:
        query = query.where(AgentRun.status == status)

    query = query.order_by(AgentRun.started_at.desc())
    result = await db.execute(query)
    runs = result.scalars().all()

    return [AgentRunResponse.model_validate(run) for run in runs]


@router.get("/runs/{run_id}", response_model=AgentRunResponse)
async def get_agent_run(
    run_id: str,
    db: AsyncSession = Depends(get_db),
) -> AgentRunResponse:
    """Get a specific agent run."""
    result = await db.execute(select(AgentRun).where(AgentRun.id == run_id))
    agent_run = result.scalar_one_or_none()
    if not agent_run:
        logger.warning("Agent run not found: %s", run_id)
        raise HTTPException(status_code=404, detail="Agent run not found")
    return AgentRunResponse.model_validate(agent_run)


# ─────────────────────────────────────────────────────────────
# Task Planning & Execution Endpoints
# ─────────────────────────────────────────────────────────────


async def _plan_task_background(task_id: str) -> None:
    """Background task for AI planning."""
    from src.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        try:
            task, project = await _load_task_and_project(task_id, db)
        except ValueError:
            return

        await plan_task_decomposition(db, task, project)


async def _execute_subtasks_background(task_id: str) -> None:
    """Background task for sequential subtask execution."""
    from src.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        try:
            task, project = await _load_task_and_project(task_id, db)
        except ValueError:
            return

        await execute_subtasks_sequentially(db, task, project)


@router.post("/plan/{task_id}", status_code=status.HTTP_202_ACCEPTED)
async def plan_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Start AI planning for a task.

    The agent will decompose the task into subtasks and set status to NEEDS_REVIEW.
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning("Task not found for planning: %s", task_id)
        raise HTTPException(status_code=404, detail="Task not found")

    # Start background planning
    background_tasks.add_task(_plan_task_background, task.id)

    return {"status": "planning_started", "task_id": task_id}


@router.post("/execute/{task_id}", status_code=status.HTTP_202_ACCEPTED)
async def execute_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Execute all subtasks of a parent task sequentially.

    Called after user approves the plan (task in NEEDS_REVIEW status).
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        logger.warning("Task not found for execution: %s", task_id)
        raise HTTPException(status_code=404, detail="Task not found")

    # Start background execution
    background_tasks.add_task(_execute_subtasks_background, task.id)

    return {"status": "execution_started", "task_id": task_id}
