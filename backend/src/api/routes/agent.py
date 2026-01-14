"""Agent execution API endpoints."""

from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.orchestrator import run_task, stop_agent_run
from src.api.schemas import AgentRunCreate, AgentRunResponse
from src.database import get_db
from src.models.agent_run import AgentRun, AgentRunStatus
from src.models.project import Project
from src.models.task import Task

router = APIRouter(prefix="/api/agent", tags=["agent"])


async def _run_task_background(
    task_id: str,
    project_id: str | None,
    mcp_tools: list[str] | None,
) -> None:
    """Background task runner."""
    from src.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        # Fetch task
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            return

        # Fetch project if available
        project = None
        if project_id:
            result = await db.execute(select(Project).where(Project.id == project_id))
            project = result.scalar_one_or_none()

        await run_task(db, task, project, mcp_tools)


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
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if task already has an active run
    result = await db.execute(
        select(AgentRun).where(
            AgentRun.task_id == run_data.task_id,
            AgentRun.status == AgentRunStatus.RUNNING,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409, detail="Task already has an active agent run"
        )

    # Start background task
    background_tasks.add_task(
        _run_task_background,
        task.id,
        task.project_id,
        ["filesystem"],  # Default MCP tools
    )

    # Return placeholder response (actual run is created in background)
    return AgentRunResponse(
        id="pending",
        task_id=run_data.task_id,
        status=AgentRunStatus.PENDING,
        error_message=None,
        started_at=None,  # type: ignore
        completed_at=None,
    )


@router.post("/stop/{run_id}", status_code=status.HTTP_200_OK)
async def stop_agent(
    run_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Stop a running agent."""
    result = await db.execute(select(AgentRun).where(AgentRun.id == run_id))
    agent_run = result.scalar_one_or_none()
    if not agent_run:
        raise HTTPException(status_code=404, detail="Agent run not found")

    if agent_run.status != AgentRunStatus.RUNNING:
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
        raise HTTPException(status_code=404, detail="Agent run not found")
    return AgentRunResponse.model_validate(agent_run)
