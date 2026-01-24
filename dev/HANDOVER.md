# HANDOVER

## Phase: Phase 10 Ready - Subtasks & Expand/Collapse (#24) 🟢

---

## Session 2026-01-24 (Quick Wins: #3, #16)

### Was wurde gemacht

1. **#16 - Agent-Autostart** ✅ WON'T FIX
   - Entscheidung: Kein Autostart implementieren
   - Gründe: Task-Erstellung ≠ Task-Ausführung, User behält Kontrolle
   - Bei Bedarf später als optionales Setting möglich

2. **#3 - Backend Settings in UI** ✅ FIXED
   - Backend: `GET/POST /api/settings` Endpoints
   - Frontend: `settings.ts` Service + Store erweitert
   - SettingsPanel: Neue "Agent Config" Section (Model + Max Turns)
   - Speicherung: `.kanban/settings.json`
   - Tests: 78 passed

### Geänderte Dateien

```
backend/src/api/routes/settings.py      # GET/POST /api/settings
backend/tests/test_settings.py          # Neue Tests
frontend/src/lib/services/settings.ts   # NEU: API Client
frontend/src/lib/stores/settings.svelte.ts  # Backend-Settings hinzugefügt
frontend/src/lib/components/panel/SettingsPanel.svelte  # Agent Config UI
frontend/src/routes/+layout.svelte      # loadBackendSettings()
dev/ISSUE_TRACKER.md                    # #3, #16 erledigt
```

---

## Nächste Session: #24 - Subtasks + Expand/Collapse Cards

### User Story
> "Komplexe Tasks werden vom Agent in Untertasks zerlegt. Die Card kann aufgeklappt werden, um Subtasks zu sehen."

### Features
- Expand/Collapse Cards im Board
- Subtasks als Checklist innerhalb einer Card
- Agent zerlegt komplexe Tasks automatisch (Claude SDK Planungsmodus)
- Nur für komplexe Tasks (einfache bleiben flat)

### Implementation Plan

| Komponente | Änderung |
|------------|----------|
| Backend: Task-Model | `subtasks: list[dict]` (JSON-Array) |
| Backend: Task-Schema | Subtasks-Feld in Pydantic-Model |
| Frontend: TaskCard | Expandable mit Chevron + Subtask-Checklist |
| Frontend: TaskEditor | Subtasks hinzufügen/bearbeiten |
| Agent | Planungsmodus für Task-Zerlegung |

### Technisches Detail
```python
# Task-Model
subtasks: list[dict] = []  # [{text: str, done: bool}]
```

```typescript
// Frontend Interface
interface Subtask {
  text: string;
  done: boolean;
}
```

---

## Offene Issues

| Prio | # | Issue | Phase |
|------|---|-------|-------|
| 1 | **#24** | Subtasks + Expand Cards | **10** |
| 2 | #25, #26 | Erweiterte Tasks + Projektstruktur | 11 (Konzept) |
| 3 | #22 | Projekt-Management | 11 (Konzept) |

---

## Verification Commands

```bash
# Server starten
make dev

# Backend Checks
cd backend
uv run ruff check --fix . && uv run ruff format .
uvx ty check
uv run pytest

# Frontend Checks
cd frontend
bunx biome check --write .
bunx svelte-check --threshold warning
```

---

*Updated: 2026-01-24*
