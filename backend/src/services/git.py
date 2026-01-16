"""Git operations for task checkpoints."""

import subprocess
from pathlib import Path


def create_checkpoint(workspace: Path, task_id: str) -> bool:
    """Create a git checkpoint before task execution.

    Stages all changes and creates a checkpoint commit.
    Returns True if successful (or nothing to commit), False on error.
    """
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
            ["git", "commit", "-m", f"checkpoint: before task-{task_id[:8]}"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Return code 1 means nothing to commit, which is fine
        return result.returncode in (0, 1)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def create_commit(workspace: Path, message: str) -> bool:
    """Create a git commit after successful task completion.

    Stages all changes and commits with the given message.
    Returns True if successful (or nothing to commit), False on error.
    """
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
