"""Orchestrator Agent for executing tasks with Claude Agent SDK.

This module re-exports all agent orchestration functions for backward compatibility.
"""

# Re-export types
from .types import AgentLogEntry, AgentResult

# Re-export executor functions
from .executor import execute_agent_run, stop_agent_run

# Re-export planner functions
from .planner import plan_task_decomposition

# Re-export subtask executor
from .subtask_executor import execute_subtasks_sequentially

__all__ = [
    # Types
    "AgentLogEntry",
    "AgentResult",
    # Executor
    "execute_agent_run",
    "stop_agent_run",
    # Planner
    "plan_task_decomposition",
    # Subtask Executor
    "execute_subtasks_sequentially",
]
