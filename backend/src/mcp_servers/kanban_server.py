"""Kanban MCP Server for Claude Code integration.

This MCP server exposes Kanban board operations as tools that Claude Code can use
to create tasks and retrieve results.
"""

import os
from typing import Any

import httpx
from mcp.server import FastMCP  # type: ignore[import-untyped]

# Get API URL from environment
KANBAN_API_URL = os.environ.get("KANBAN_API_URL", "http://localhost:8000")

# Create FastMCP server
mcp = FastMCP("Kanban MCP")


class KanbanAPIError(Exception):
    """Error communicating with Kanban API."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def _handle_response(response: httpx.Response) -> dict[str, Any] | list[dict[str, Any]]:
    """Parse response JSON with error handling."""
    try:
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise KanbanAPIError(
            f"API returned {e.response.status_code}: {e.response.text}",
            status_code=e.response.status_code,
        ) from e
    except ValueError as e:
        raise KanbanAPIError(f"Invalid JSON response: {e}") from e


def _get(path: str) -> dict[str, Any]:
    """GET request returning a single object."""
    url = f"{KANBAN_API_URL}{path}"
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            result = _handle_response(response)
            if not isinstance(result, dict):
                raise KanbanAPIError(f"Expected object, got {type(result).__name__}")
            return result
    except httpx.ConnectError as e:
        raise KanbanAPIError(f"Cannot connect to Kanban API at {url}") from e
    except httpx.TimeoutException as e:
        raise KanbanAPIError(f"Request to {url} timed out") from e


def _get_list(path: str) -> list[dict[str, Any]]:
    """GET request returning a list."""
    url = f"{KANBAN_API_URL}{path}"
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            result = _handle_response(response)
            if not isinstance(result, list):
                raise KanbanAPIError(f"Expected list, got {type(result).__name__}")
            return result
    except httpx.ConnectError as e:
        raise KanbanAPIError(f"Cannot connect to Kanban API at {url}") from e
    except httpx.TimeoutException as e:
        raise KanbanAPIError(f"Request to {url} timed out") from e


def _post(path: str, json: dict[str, Any]) -> dict[str, Any]:
    """POST request returning a single object."""
    url = f"{KANBAN_API_URL}{path}"
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, json=json)
            result = _handle_response(response)
            if not isinstance(result, dict):
                raise KanbanAPIError(f"Expected object, got {type(result).__name__}")
            return result
    except httpx.ConnectError as e:
        raise KanbanAPIError(f"Cannot connect to Kanban API at {url}") from e
    except httpx.TimeoutException as e:
        raise KanbanAPIError(f"Request to {url} timed out") from e


@mcp.tool()
def create_task(title: str, description: str | None = None) -> dict[str, str]:
    """Create a new task in the Kanban board.

    Args:
        title: Task title (required)
        description: Optional task description

    Returns:
        Dict with task ID and status on success, or error message on failure.
    """
    if not title or not title.strip():
        return {"error": "Title is required and cannot be empty"}

    payload: dict[str, Any] = {"title": title.strip()}
    if description:
        payload["description"] = description.strip()

    try:
        result = _post("/api/tasks", json=payload)
        return {
            "id": result.get("id", "unknown"),
            "status": result.get("status", "unknown"),
        }
    except KanbanAPIError as e:
        return {"error": str(e)}


@mcp.tool()
def list_tasks() -> list[dict[str, Any]] | dict[str, str]:
    """List all tasks in the Kanban board with their current status.

    Returns:
        List of tasks on success, or dict with error message on failure.
    """
    try:
        tasks = _get_list("/api/tasks")
        return [
            {
                "id": t.get("id", "unknown"),
                "title": t.get("title", "untitled"),
                "status": t.get("status", "unknown"),
                "type": t.get("type", "neutral"),
                "description": t.get("description"),
            }
            for t in tasks
        ]
    except KanbanAPIError as e:
        return {"error": str(e)}


@mcp.tool()
def get_task_result(task_id: str) -> dict[str, Any]:
    """Get task details and agent execution results.

    Args:
        task_id: UUID of the task to retrieve

    Returns:
        Task details on success, or dict with error message on failure.
    """
    if not task_id or not task_id.strip():
        return {"error": "task_id is required"}

    try:
        task = _get(f"/api/tasks/{task_id.strip()}")
        return {
            "id": task.get("id", task_id),
            "title": task.get("title", "untitled"),
            "status": task.get("status", "unknown"),
            "type": task.get("type", "neutral"),
            "description": task.get("description"),
            "created_at": task.get("created_at"),
        }
    except KanbanAPIError as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()
