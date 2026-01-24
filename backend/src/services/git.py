"""Git operations for task checkpoints."""

import subprocess
from pathlib import Path


def _run_git_command(cmd: list[str], cwd: Path, timeout: int = 30) -> bool:
    """Run git command with error handling.

    Returns True on success or exit code 1 (nothing to commit).
    Returns False on error or timeout.
    """
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode in (0, 1)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def create_checkpoint(workspace: Path, task_id: str) -> bool:
    """Create a git checkpoint before task execution.

    Stages all changes and creates a checkpoint commit.
    Returns True if successful (or nothing to commit), False on error.
    """
    if not _run_git_command(["git", "add", "-A"], workspace):
        return False
    return _run_git_command(
        ["git", "commit", "-m", f"checkpoint: before task-{task_id[:8]}"], workspace
    )


def create_commit(workspace: Path, message: str) -> bool:
    """Create a git commit after successful task completion.

    Stages all changes and commits with the given message.
    Returns True if successful (or nothing to commit), False on error.
    """
    if not _run_git_command(["git", "add", "-A"], workspace):
        return False
    return _run_git_command(["git", "commit", "-m", message], workspace)
