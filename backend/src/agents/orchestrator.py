"""Orchestrator Agent for executing tasks with Claude Agent SDK."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

from claude_agent_sdk import query
from claude_agent_sdk.types import ClaudeAgentOptions
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import EventType, TaskEvent, event_bus
from src.models.agent_run import AgentRun, AgentRunStatus
from src.models.task import Task, TaskStatus
from src.mcp_servers.registry import get_mcp_config

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


async def _create_git_checkpoint(workspace: Path, task_id: str) -> bool:
    """Create a git checkpoint before task execution."""
    try:
        result = subprocess.run(
            ["git", "add", "-A"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return False

        result = subprocess.run(
            ["git", "commit", "-m", f"checkpoint: 📍 before task-{task_id[:8]}"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Return code 1 means nothing to commit, which is fine
        return result.returncode in (0, 1)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


async def _create_git_commit(workspace: Path, message: str) -> bool:
    """Create a git commit after successful task completion."""
    try:
        result = subprocess.run(
            ["git", "add", "-A"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return False

        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode in (0, 1)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


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


async def run_task(
    db: AsyncSession,
    task: Task,
    project: Project | None,
    mcp_tools: list[str] | None = None,
) -> AgentResult:
    """Execute a task using the Claude Agent SDK.

    Args:
        db: Database session
        task: The task to execute
        project: The project containing workspace path
        mcp_tools: List of MCP tools to enable (default: ["filesystem"])
    """
    if mcp_tools is None:
        mcp_tools = ["filesystem"]

    workspace_path = project.workspace_path if project else "."
    workspace = Path(workspace_path).resolve()

    # Create agent run record
    agent_run = AgentRun(
        id=str(uuid4()),
        task_id=task.id,
        status=AgentRunStatus.RUNNING,
    )
    db.add(agent_run)
    await db.commit()

    # Update task status
    task.status = TaskStatus.IN_PROGRESS
    await db.commit()

    # Publish status update
    await event_bus.publish(
        TaskEvent(
            event_type=EventType.TASK_UPDATED,
            data={
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "agent_run_id": agent_run.id,
            },
        )
    )

    # Git checkpoint
    if workspace.exists():
        await _create_git_checkpoint(workspace, task.id)

    # Build options
    mcp_config = get_mcp_config(mcp_tools, str(workspace))
    options = ClaudeAgentOptions(
        cwd=str(workspace),
        mcp_servers=mcp_config,
        permission_mode="bypassPermissions",
        max_turns=50,
    )

    prompt = _build_prompt(task, project)
    logs: list[dict[str, str]] = []

    try:
        async for message in query(prompt=prompt, options=options):
            # Log each message
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": getattr(message, "type", "unknown"),
                "content": str(message)[:500],  # Truncate for storage
            }
            logs.append(log_entry)

            # Stream log to frontend via SSE
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

            # Check for completion
            if hasattr(message, "type") and message.type == "result":
                if hasattr(message, "subtype") and message.subtype == "success":
                    # Success - create commit
                    await _create_git_commit(workspace, f"feat: ✨ {task.title}")

                    agent_run.status = AgentRunStatus.COMPLETED
                    agent_run.completed_at = datetime.now(timezone.utc)
                    task.status = TaskStatus.DONE
                    await db.commit()

                    await event_bus.publish(
                        TaskEvent(
                            event_type=EventType.TASK_UPDATED,
                            data={
                                "id": task.id,
                                "title": task.title,
                                "status": task.status,
                            },
                        )
                    )

                    return AgentResult(
                        status=AgentRunStatus.COMPLETED,
                        message="Task completed successfully",
                    )

    except Exception as e:
        # Handle errors
        error_msg = str(e)
        agent_run.status = AgentRunStatus.FAILED
        agent_run.error_message = error_msg
        agent_run.completed_at = datetime.now(timezone.utc)
        task.status = TaskStatus.TODO  # Reset to TODO on failure
        await db.commit()

        await event_bus.publish(
            TaskEvent(
                event_type=EventType.TASK_UPDATED,
                data={
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "error": error_msg,
                },
            )
        )

        return AgentResult(
            status=AgentRunStatus.FAILED,
            error=error_msg,
        )

    # If we get here without explicit result, mark as completed
    agent_run.status = AgentRunStatus.COMPLETED
    agent_run.completed_at = datetime.now(timezone.utc)
    task.status = TaskStatus.DONE
    await db.commit()

    return AgentResult(
        status=AgentRunStatus.COMPLETED,
        message="Task execution finished",
    )


async def stop_agent_run(db: AsyncSession, agent_run: AgentRun) -> bool:
    """Stop a running agent (placeholder for future implementation)."""
    # TODO: Implement actual process termination
    agent_run.status = AgentRunStatus.CANCELLED
    agent_run.completed_at = datetime.now(timezone.utc)
    await db.commit()
    return True
