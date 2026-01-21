"""Settings API endpoint tests."""

from httpx import AsyncClient


async def test_get_settings_schema(client: AsyncClient) -> None:
    """GET /api/settings/schema returns MCP-relevant settings."""
    response = await client.get("/api/settings/schema")
    assert response.status_code == 200

    data = response.json()

    # Main setting groups are present
    assert "git" in data
    assert "agent" in data


async def test_settings_schema_git_options(client: AsyncClient) -> None:
    """Git settings have expected structure."""
    response = await client.get("/api/settings/schema")
    data = response.json()

    git = data["git"]

    # Auto checkpoint setting
    assert "auto_checkpoint" in git
    assert git["auto_checkpoint"]["type"] == "boolean"
    assert git["auto_checkpoint"]["default"] is True
    assert "label" in git["auto_checkpoint"]
    assert "description" in git["auto_checkpoint"]

    # Checkpoint prefix setting
    assert "checkpoint_prefix" in git
    assert git["checkpoint_prefix"]["type"] == "string"
    assert git["checkpoint_prefix"]["default"] == "checkpoint:"


async def test_settings_schema_agent_options(client: AsyncClient) -> None:
    """Agent settings have expected structure."""
    response = await client.get("/api/settings/schema")
    data = response.json()

    agent = data["agent"]

    # Max turns setting
    assert "max_turns" in agent
    assert agent["max_turns"]["type"] == "number"
    assert agent["max_turns"]["default"] == 10
    assert agent["max_turns"]["min"] == 1
    assert agent["max_turns"]["max"] == 50
    assert "label" in agent["max_turns"]

    # Model setting
    assert "model" in agent
    assert agent["model"]["type"] == "select"
    assert "options" in agent["model"]
    assert len(agent["model"]["options"]) > 0
    assert "claude-sonnet-4-20250514" in agent["model"]["options"]
