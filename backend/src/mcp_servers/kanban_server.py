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


def _get(path: str) -> dict[str, Any]:
    """GET request returning a single object."""
    url = f"{KANBAN_API_URL}{path}"
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def _get_list(path: str) -> list[dict[str, Any]]:
    """GET request returning a list."""
    url = f"{KANBAN_API_URL}{path}"
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def _post(path: str, json: dict[str, Any]) -> dict[str, Any]:
    """POST request returning a single object."""
    url = f"{KANBAN_API_URL}{path}"
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json=json)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def create_task(title: str, description: str | None = None) -> dict[str, str]:
    """Create a new task in the Kanban board.

    Args:
        title: Task title (required)
        description: Optional task description
    """
    payload: dict[str, Any] = {"title": title}
    if description:
        payload["description"] = description

    result = _post("/api/tasks", json=payload)
    return {"id": result["id"], "status": result["status"]}


@mcp.tool()
def list_tasks() -> list[dict[str, Any]]:
    """List all tasks in the Kanban board with their current status."""
    tasks = _get_list("/api/tasks")
    return [
        {
            "id": t["id"],
            "title": t["title"],
            "status": t["status"],
            "description": t.get("description"),
        }
        for t in tasks
    ]


@mcp.tool()
def get_task_result(task_id: str) -> dict[str, Any]:
    """Get task details and agent execution results.

    Args:
        task_id: UUID of the task to retrieve
    """
    task = _get(f"/api/tasks/{task_id}")
    return {
        "id": task["id"],
        "title": task["title"],
        "status": task["status"],
        "description": task.get("description"),
        "created_at": task["created_at"],
    }


if __name__ == "__main__":
    mcp.run()
