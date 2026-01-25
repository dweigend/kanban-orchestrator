"""Type definitions for agent orchestration."""

from dataclasses import dataclass

from src.models.agent_run import AgentRunStatus


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
