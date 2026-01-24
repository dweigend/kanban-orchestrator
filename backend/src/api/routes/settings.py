"""Settings API endpoints for MCP-relevant configuration schema."""

import json
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/settings", tags=["settings"])

# Settings file location
SETTINGS_FILE = Path(".kanban/settings.json")


class GitSettings(BaseModel):
    """Git-related settings."""

    auto_checkpoint: bool = True
    checkpoint_prefix: str = "checkpoint:"


class AgentSettings(BaseModel):
    """Agent-related settings."""

    max_turns: int = 10
    model: str = "claude-sonnet-4-20250514"


class BackendSettings(BaseModel):
    """All backend settings."""

    git: GitSettings = GitSettings()
    agent: AgentSettings = AgentSettings()


def _load_settings() -> BackendSettings:
    """Load settings from file or return defaults."""
    if SETTINGS_FILE.exists():
        try:
            data = json.loads(SETTINGS_FILE.read_text())
            return BackendSettings(**data)
        except (json.JSONDecodeError, ValueError):
            pass
    return BackendSettings()


def _save_settings(settings: BackendSettings) -> None:
    """Save settings to file."""
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(settings.model_dump_json(indent=2))


@router.get("")
def get_settings() -> BackendSettings:
    """Get current backend settings."""
    return _load_settings()


@router.post("")
def save_settings(settings: BackendSettings) -> BackendSettings:
    """Save backend settings."""
    _save_settings(settings)
    return settings


@router.get("/schema")
def get_settings_schema() -> dict:
    """Returns MCP-relevant settings schema.

    These settings affect how agents interact with the system.
    UI-only preferences (colors, fonts) are NOT included here.
    """
    return {
        "git": {
            "auto_checkpoint": {
                "type": "boolean",
                "default": True,
                "label": "Auto Checkpoint",
                "description": "Erstellt automatisch Git Commits vor Agent-Runs",
            },
            "checkpoint_prefix": {
                "type": "string",
                "default": "checkpoint:",
                "label": "Checkpoint Prefix",
                "description": "Prefix für automatische Checkpoint-Commits",
            },
        },
        "agent": {
            "max_turns": {
                "type": "number",
                "default": 10,
                "min": 1,
                "max": 50,
                "label": "Max Agent Turns",
                "description": "Maximale Anzahl an Agent-Iterationen pro Run",
            },
            "model": {
                "type": "select",
                "default": "claude-sonnet-4-20250514",
                "options": [
                    "claude-sonnet-4-20250514",
                    "claude-opus-4-20250514",
                ],
                "label": "Agent Model",
                "description": "Claude Model für Agent-Runs",
            },
        },
    }
