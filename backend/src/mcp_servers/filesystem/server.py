"""Filesystem MCP Server for workspace file operations.

This MCP server provides sandboxed file I/O within a specified workspace directory.
"""

import os
from pathlib import Path

from mcp.server import FastMCP  # type: ignore[import-untyped]

# Get workspace from environment
WORKSPACE_PATH = os.environ.get("WORKSPACE_PATH", ".")
workspace = Path(WORKSPACE_PATH).resolve()

# Create FastMCP server
mcp = FastMCP("Filesystem MCP")


def _validate_path(path: str) -> Path:
    """Validate that path is within workspace. Raises ValueError if not."""
    full_path = (workspace / path).resolve()
    if not str(full_path).startswith(str(workspace)):
        raise ValueError(f"Path {path} is outside workspace")
    return full_path


@mcp.tool()
def read_file(path: str) -> str:
    """Read contents of a file within the workspace.

    Args:
        path: Relative path to the file from workspace root
    """
    file_path = _validate_path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")
    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to a file within the workspace.

    Args:
        path: Relative path to the file from workspace root
        content: Content to write to the file
    """
    file_path = _validate_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return f"Successfully wrote {len(content)} characters to {path}"


@mcp.tool()
def list_directory(path: str = ".") -> list[dict[str, str]]:
    """List contents of a directory within the workspace.

    Args:
        path: Relative path to the directory from workspace root
    """
    dir_path = _validate_path(path)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    if not dir_path.is_dir():
        raise ValueError(f"Not a directory: {path}")

    entries = []
    for entry in sorted(dir_path.iterdir()):
        entries.append(
            {
                "name": entry.name,
                "type": "directory" if entry.is_dir() else "file",
                "size": str(entry.stat().st_size) if entry.is_file() else "",
            }
        )
    return entries


@mcp.tool()
def create_directory(path: str) -> str:
    """Create a directory within the workspace.

    Args:
        path: Relative path to the directory from workspace root
    """
    dir_path = _validate_path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return f"Created directory: {path}"


@mcp.tool()
def delete_file(path: str) -> str:
    """Delete a file within the workspace.

    Args:
        path: Relative path to the file from workspace root
    """
    file_path = _validate_path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")
    file_path.unlink()
    return f"Deleted file: {path}"


@mcp.tool()
def file_exists(path: str) -> bool:
    """Check if a file or directory exists within the workspace.

    Args:
        path: Relative path from workspace root
    """
    try:
        full_path = _validate_path(path)
        return full_path.exists()
    except ValueError:
        return False


if __name__ == "__main__":
    mcp.run()
