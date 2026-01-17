"""Kanban MCP Server unit tests."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.mcp_servers.kanban_server import (
    KanbanAPIError,
    _get,
    _get_list,
    _post,
    create_task,
    get_task_result,
    list_tasks,
)


class TestInputValidation:
    """Test input validation in MCP tools."""

    def test_create_task_empty_title(self) -> None:
        """create_task rejects empty title."""
        result = create_task(title="")
        assert "error" in result
        assert "required" in result["error"].lower()

    def test_create_task_whitespace_title(self) -> None:
        """create_task rejects whitespace-only title."""
        result = create_task(title="   ")
        assert "error" in result

    def test_get_task_result_empty_id(self) -> None:
        """get_task_result rejects empty task_id."""
        result = get_task_result(task_id="")
        assert "error" in result
        assert "required" in result["error"].lower()

    def test_get_task_result_whitespace_id(self) -> None:
        """get_task_result rejects whitespace-only task_id."""
        result = get_task_result(task_id="   ")
        assert "error" in result


class TestErrorHandling:
    """Test error handling for network and API errors."""

    @patch("src.mcp_servers.kanban_server.httpx.Client")
    def test_connection_error_get(self, mock_client: MagicMock) -> None:
        """_get handles connection errors gracefully."""
        mock_client.return_value.__enter__.return_value.get.side_effect = (
            httpx.ConnectError("Connection refused")
        )

        with pytest.raises(KanbanAPIError) as exc:
            _get("/api/tasks")
        assert "Cannot connect" in str(exc.value)

    @patch("src.mcp_servers.kanban_server.httpx.Client")
    def test_timeout_error_get(self, mock_client: MagicMock) -> None:
        """_get handles timeout errors gracefully."""
        mock_client.return_value.__enter__.return_value.get.side_effect = (
            httpx.TimeoutException("Timeout")
        )

        with pytest.raises(KanbanAPIError) as exc:
            _get("/api/tasks")
        assert "timed out" in str(exc.value)

    @patch("src.mcp_servers.kanban_server.httpx.Client")
    def test_connection_error_get_list(self, mock_client: MagicMock) -> None:
        """_get_list handles connection errors gracefully."""
        mock_client.return_value.__enter__.return_value.get.side_effect = (
            httpx.ConnectError("Connection refused")
        )

        with pytest.raises(KanbanAPIError) as exc:
            _get_list("/api/tasks")
        assert "Cannot connect" in str(exc.value)

    @patch("src.mcp_servers.kanban_server.httpx.Client")
    def test_connection_error_post(self, mock_client: MagicMock) -> None:
        """_post handles connection errors gracefully."""
        mock_client.return_value.__enter__.return_value.post.side_effect = (
            httpx.ConnectError("Connection refused")
        )

        with pytest.raises(KanbanAPIError) as exc:
            _post("/api/tasks", {"title": "Test"})
        assert "Cannot connect" in str(exc.value)

    @patch("src.mcp_servers.kanban_server.httpx.Client")
    def test_http_error_get(self, mock_client: MagicMock) -> None:
        """_get handles HTTP errors gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=mock_response
        )
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        with pytest.raises(KanbanAPIError) as exc:
            _get("/api/tasks/unknown")
        assert "404" in str(exc.value)


class TestToolErrorReturns:
    """Test that MCP tools return error dicts instead of raising exceptions."""

    @patch("src.mcp_servers.kanban_server._post")
    def test_create_task_api_error(self, mock_post: MagicMock) -> None:
        """create_task returns error dict on API failure."""
        mock_post.side_effect = KanbanAPIError("Connection refused")

        result = create_task(title="Test Task")
        assert "error" in result
        assert "Connection refused" in result["error"]

    @patch("src.mcp_servers.kanban_server._get_list")
    def test_list_tasks_api_error(self, mock_get_list: MagicMock) -> None:
        """list_tasks returns error dict on API failure."""
        mock_get_list.side_effect = KanbanAPIError("Connection refused")

        result = list_tasks()
        assert isinstance(result, dict)
        assert "error" in result

    @patch("src.mcp_servers.kanban_server._get")
    def test_get_task_result_api_error(self, mock_get: MagicMock) -> None:
        """get_task_result returns error dict on API failure."""
        mock_get.side_effect = KanbanAPIError("API returned 404: Not Found")

        result = get_task_result(task_id="abc-123")
        assert "error" in result
        assert "404" in result["error"]


class TestSuccessfulCalls:
    """Test successful MCP tool calls with mocked API."""

    @patch("src.mcp_servers.kanban_server._post")
    def test_create_task_success(self, mock_post: MagicMock) -> None:
        """create_task returns ID and status on success."""
        mock_post.return_value = {"id": "abc-123", "status": "todo"}

        result = create_task(title="Test Task")
        assert result == {"id": "abc-123", "status": "todo"}
        mock_post.assert_called_once_with("/api/tasks", json={"title": "Test Task"})

    @patch("src.mcp_servers.kanban_server._post")
    def test_create_task_with_description(self, mock_post: MagicMock) -> None:
        """create_task includes description when provided."""
        mock_post.return_value = {"id": "abc-123", "status": "todo"}

        result = create_task(title="Test Task", description="A description")
        assert result == {"id": "abc-123", "status": "todo"}
        mock_post.assert_called_once_with(
            "/api/tasks", json={"title": "Test Task", "description": "A description"}
        )

    @patch("src.mcp_servers.kanban_server._post")
    def test_create_task_strips_whitespace(self, mock_post: MagicMock) -> None:
        """create_task strips whitespace from title and description."""
        mock_post.return_value = {"id": "abc-123", "status": "todo"}

        create_task(title="  Test Task  ", description="  Description  ")
        mock_post.assert_called_once_with(
            "/api/tasks", json={"title": "Test Task", "description": "Description"}
        )

    @patch("src.mcp_servers.kanban_server._get_list")
    def test_list_tasks_success(self, mock_get_list: MagicMock) -> None:
        """list_tasks returns formatted task list."""
        mock_get_list.return_value = [
            {"id": "1", "title": "Task 1", "status": "todo", "description": None},
            {"id": "2", "title": "Task 2", "status": "done", "description": "Done!"},
        ]

        result = list_tasks()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["status"] == "done"

    @patch("src.mcp_servers.kanban_server._get_list")
    def test_list_tasks_empty(self, mock_get_list: MagicMock) -> None:
        """list_tasks handles empty list."""
        mock_get_list.return_value = []

        result = list_tasks()
        assert result == []

    @patch("src.mcp_servers.kanban_server._get")
    def test_get_task_result_success(self, mock_get: MagicMock) -> None:
        """get_task_result returns task details."""
        mock_get.return_value = {
            "id": "abc-123",
            "title": "Test",
            "status": "todo",
            "description": None,
            "created_at": "2026-01-16T00:00:00Z",
        }

        result = get_task_result(task_id="abc-123")
        assert result["id"] == "abc-123"
        assert result["created_at"] == "2026-01-16T00:00:00Z"

    @patch("src.mcp_servers.kanban_server._get")
    def test_get_task_result_strips_whitespace(self, mock_get: MagicMock) -> None:
        """get_task_result strips whitespace from task_id."""
        mock_get.return_value = {"id": "abc-123", "title": "Test", "status": "todo"}

        get_task_result(task_id="  abc-123  ")
        mock_get.assert_called_once_with("/api/tasks/abc-123")
