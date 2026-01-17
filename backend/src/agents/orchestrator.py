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
    data = {"id": task.id, "title": task.title, "status": task.status}
    if extra_data:
        data.update(extra_data)
    await event_bus.publish(TaskEvent(event_type=EventType.TASK_UPDATED, data=data))


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
                    create_commit(workspace, f"feat: {task.title}")
                    await _finalize_run(
                        db, agent_run, task, AgentRunStatus.COMPLETED, TaskStatus.DONE
                    )
                    await _publish_task_update(task)
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
        return AgentResult(status=AgentRunStatus.FAILED, error=error_msg)

    # If we get here without explicit result, mark as completed
    await _finalize_run(db, agent_run, task, AgentRunStatus.COMPLETED, TaskStatus.DONE)
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
