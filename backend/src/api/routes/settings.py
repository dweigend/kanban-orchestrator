"""Settings API endpoints for MCP-relevant configuration schema."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/settings", tags=["settings"])


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
