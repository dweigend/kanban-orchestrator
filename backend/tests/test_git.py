"""Git service tests."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from src.services.git import create_checkpoint, create_commit


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """Create a temporary git repository."""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=tmp_path,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=tmp_path,
        capture_output=True,
    )
    # Create initial commit
    (tmp_path / "README.md").write_text("# Test")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"], cwd=tmp_path, capture_output=True
    )
    return tmp_path


def test_create_checkpoint_with_changes(git_repo: Path) -> None:
    """create_checkpoint commits staged changes."""
    # Create new file
    (git_repo / "test.txt").write_text("Hello")

    result = create_checkpoint(git_repo, "task-12345678")
    assert result is True

    # Verify commit was created
    log = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=git_repo,
        capture_output=True,
        text=True,
    )
    assert "checkpoint: before task-task-123" in log.stdout


def test_create_checkpoint_no_changes(git_repo: Path) -> None:
    """create_checkpoint succeeds even when nothing to commit."""
    # No changes made
    result = create_checkpoint(git_repo, "task-12345678")
    assert result is True  # Return code 1 (nothing to commit) is treated as success


def test_create_checkpoint_not_git_repo(tmp_path: Path) -> None:
    """create_checkpoint returns False for non-git directory."""
    result = create_checkpoint(tmp_path, "task-12345678")
    assert result is False


def test_create_checkpoint_nonexistent_path() -> None:
    """create_checkpoint returns False for nonexistent path."""
    result = create_checkpoint(Path("/nonexistent/path"), "task-12345678")
    assert result is False


def test_create_checkpoint_timeout() -> None:
    """create_checkpoint handles subprocess timeout."""
    with patch("src.services.git.subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="git", timeout=30)
        result = create_checkpoint(Path("/tmp"), "task-12345678")
        assert result is False


def test_create_commit_with_changes(git_repo: Path) -> None:
    """create_commit commits changes with custom message."""
    # Create new file
    (git_repo / "feature.txt").write_text("New feature")

    result = create_commit(git_repo, "feat: add new feature")
    assert result is True

    # Verify commit message
    log = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=git_repo,
        capture_output=True,
        text=True,
    )
    assert "feat: add new feature" in log.stdout


def test_create_commit_no_changes(git_repo: Path) -> None:
    """create_commit succeeds when nothing to commit."""
    result = create_commit(git_repo, "empty commit")
    assert result is True


def test_create_commit_not_git_repo(tmp_path: Path) -> None:
    """create_commit returns False for non-git directory."""
    result = create_commit(tmp_path, "test commit")
    assert result is False
