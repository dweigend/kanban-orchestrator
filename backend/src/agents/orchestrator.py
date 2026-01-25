"""Orchestrator Agent for executing tasks with Claude Agent SDK."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from claude_agent_sdk import query
from claude_agent_sdk.types import ClaudeAgentOptions
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import EventType, TaskEvent, event_bus
from src.mcp_client import get_mcp_config
from src.models.agent_run import AgentRun, AgentRunStatus
from src.models.task import Task, TaskStatus
from src.services.git import create_checkpoint, create_commit

if TYPE_CHECKING:
    from src.models.project import Project


@dataclass
class AgentLogEntry:
    """Single log entry from agent execution."""

    timestamp: str
    type: str
    content: str


@dataclass
class AgentResult:
    """Result of an agent run."""

    status: AgentRunStatus
    message: str | None = None
    error: str | None = None


def _build_prompt(task: Task, project: Project | None) -> str:
    """Build the agent prompt from task data."""
    parts = [f"# Task: {task.title}"]

    if task.description:
        parts.append(f"\n## Description\n{task.description}")

    if project:
        parts.append(f"\n## Workspace\n{project.workspace_path}")
        parts.append(
            "\nWork within this workspace directory. Create files and folders as needed."
        )

    parts.append("\n## Instructions")
    parts.append(
        "Complete this task. If you need clarification, explain what you need."
    )
    parts.append("When done, provide a summary of what was accomplished.")

    return "\n".join(parts)


async def _publish_task_update(
    task: Task, extra_data: dict[str, str] | None = None
) -> None:
    """Publish a task update event via SSE."""
    data = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "result": task.result,
        "status": task.status,
        "type": task.type,
        "project_id": task.project_id,
        "parent_id": task.parent_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
    }
    if extra_data:
        data.update(extra_data)
    await event_bus.publish(TaskEvent(event_type=EventType.TASK_UPDATED, data=data))


async def _publish_finished_log(
    task_id: str, agent_run_id: str, error: str | None = None
) -> None:
    """Publish a 'finished' log entry to signal agent completion."""
    content = error if error else "Agent execution completed"
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "finished",
        "content": content,
    }
    await event_bus.publish(
        TaskEvent(
            event_type=EventType.AGENT_LOG,
            data={
                "task_id": task_id,
                "agent_run_id": agent_run_id,
                "log": log_entry,
            },
        )
    )


async def _finalize_run(
    db: AsyncSession,
    agent_run: AgentRun,
    task: Task,
    status: AgentRunStatus,
    task_status: TaskStatus,
    error_msg: str | None = None,
) -> None:
    """Finalize agent run and task with given statuses."""
    agent_run.status = status
    agent_run.completed_at = datetime.now(timezone.utc)
    if error_msg:
        agent_run.error_message = error_msg
    task.status = task_status
    await db.commit()


async def execute_agent_run(
    db: AsyncSession,
    agent_run: AgentRun,
    task: Task,
    project: Project | None,
    mcp_tools: list[str] | None = None,
) -> AgentResult:
    """Execute an existing agent run using the Claude Agent SDK.

    Args:
        db: Database session
        agent_run: The pre-created AgentRun (in PENDING status)
        task: The task to execute
        project: The project containing workspace path
        mcp_tools: List of MCP tools to enable (default: ["filesystem"])
    """
    if mcp_tools is None:
        mcp_tools = ["filesystem"]

    workspace_path = project.workspace_path if project else "."
    workspace = Path(workspace_path).resolve()

    # Transition to RUNNING and set started_at
    agent_run.status = AgentRunStatus.RUNNING
    agent_run.started_at = datetime.now(timezone.utc)
    await db.commit()

    # Update task status and notify
    task.status = TaskStatus.IN_PROGRESS
    await db.commit()
    await _publish_task_update(task, {"agent_run_id": agent_run.id})

    # Git checkpoint before execution
    if workspace.exists():
        create_checkpoint(workspace, task.id)

    # Build agent options
    mcp_config = get_mcp_config(mcp_tools, str(workspace))
    options = ClaudeAgentOptions(
        cwd=str(workspace),
        mcp_servers=mcp_config,
        permission_mode="bypassPermissions",
        max_turns=50,
    )

    prompt = _build_prompt(task, project)

    try:
        async for message in query(prompt=prompt, options=options):
            # Determine message type from class name (SDK types don't have .type attr)
            msg_class = message.__class__.__name__
            msg_type = msg_class.replace(
                "Message", ""
            ).lower()  # ResultMessage → result

            # Stream log to frontend via SSE
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": msg_type,
                "content": str(message)[:500],
            }
            await event_bus.publish(
                TaskEvent(
                    event_type=EventType.AGENT_LOG,
                    data={
                        "task_id": task.id,
                        "agent_run_id": agent_run.id,
                        "log": log_entry,
                    },
                )
            )

            # Check for success result
            if msg_type == "result":
                if getattr(message, "subtype", None) == "success":
                    # Save agent result to task
                    task.result = getattr(message, "result", None)
                    create_commit(workspace, f"feat: {task.title}")
                    await _finalize_run(
                        db, agent_run, task, AgentRunStatus.COMPLETED, TaskStatus.DONE
                    )
                    await _publish_task_update(task)
                    await _publish_finished_log(task.id, agent_run.id)
                    return AgentResult(
                        status=AgentRunStatus.COMPLETED,
                        message="Task completed successfully",
                    )

    except Exception as e:
        error_msg = str(e)
        await _finalize_run(
            db,
            agent_run,
            task,
            AgentRunStatus.FAILED,
            TaskStatus.TODO,
            error_msg,
        )
        await _publish_task_update(task, {"error": error_msg})
        await _publish_finished_log(task.id, agent_run.id, error_msg)
        return AgentResult(status=AgentRunStatus.FAILED, error=error_msg)

    # If we get here without explicit result, mark as completed
    await _finalize_run(db, agent_run, task, AgentRunStatus.COMPLETED, TaskStatus.DONE)
    await _publish_finished_log(task.id, agent_run.id)
    return AgentResult(
        status=AgentRunStatus.COMPLETED, message="Task execution finished"
    )


async def stop_agent_run(db: AsyncSession, agent_run: AgentRun) -> bool:
    """Stop a running agent (placeholder for future implementation)."""
    # TODO: Implement actual process termination
    agent_run.status = AgentRunStatus.CANCELLED
    agent_run.completed_at = datetime.now(timezone.utc)
    await db.commit()
    return True


# ─────────────────────────────────────────────────────────────
# Task Planning & Decomposition
# ─────────────────────────────────────────────────────────────


async def _create_placeholder_subtasks(
    parent: Task,
    db: AsyncSession,
) -> list[Task]:
    """Create Setup/Implement/Finalize subtasks for a parent task."""
    from uuid import uuid4

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
    from src.api.events import EventType, TaskEvent, event_bus

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


async def execute_subtasks_sequentially(
    db: AsyncSession,
    parent_task: Task,
    project: Project | None,
) -> None:
    """Execute all subtasks of a parent task one by one.

    Called after user approves the plan.
    """
    from sqlalchemy import select
    from uuid import uuid4

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
