# HANDOVER

## Phase: 8 - Schema-Driven UI 🏗️

---

## Session 2026-01-21 (Architektur & Planung) ✅

### Was wurde gemacht

1. **Architektur-Analyse:** Backend vs. Frontend Aufteilung definiert
2. **ARCHITECTURE.md erweitert:** Entscheidungslogik + Aufteilung hinzugefügt (Root-Datei)
3. **PLAN.md aktualisiert:** Phase 8 mit konkreten Tasks

### Architektur-Entscheidung

**Faustregel:** Braucht ein MCP-Client (headless) diese Information?

| JA → Backend | NEIN → Frontend |
|--------------|-----------------|
| Task/Project Daten | Font Family/Size |
| Enum Labels & Icons | CSS Farben |
| Workflow Settings | Notifications |
| Feld-Schemas | Animations |

**Dokumentiert in:** `ARCHITECTURE.md` (Root)

---

## Nächste Session: Phase 8 Implementation

### Empfohlene Reihenfolge

#### 8.1 Backend - Enum-Erweiterung (Start hier!)

**Datei:** `backend/src/api/routes/schema.py`

**Aktuell:**
```python
@router.get("/enums")
async def get_enums():
    return {
        "task_status": [s.value for s in TaskStatus],
        "task_type": [t.value for t in TaskType],
    }
```

**Ändern zu:**
```python
@router.get("/enums")
async def get_enums():
    return {
        "task_status": [
            {"value": "todo", "label": "To Do", "description": "Task nicht gestartet"},
            {"value": "in_progress", "label": "In Progress", "description": "Task wird bearbeitet"},
            {"value": "needs_review", "label": "Needs Review", "description": "Wartet auf Review"},
            {"value": "done", "label": "Done", "description": "Task abgeschlossen"},
        ],
        "task_type": [
            {"value": "research", "label": "Research", "icon": "MagnifyingGlass"},
            {"value": "dev", "label": "Development", "icon": "Code"},
            {"value": "notes", "label": "Notes", "icon": "NotePencil"},
            {"value": "neutral", "label": "General", "icon": "Circle"},
        ],
        "agent_run_status": [
            {"value": "pending", "label": "Pending"},
            {"value": "running", "label": "Running"},
            {"value": "completed", "label": "Completed"},
            {"value": "failed", "label": "Failed"},
        ],
    }
```

**Test:** `curl http://localhost:8000/api/schema/enums | jq`

#### 8.2 Backend - Settings Endpoint (Optional)

**Neue Datei:** `backend/src/api/routes/settings.py`

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/schema")
async def get_settings_schema():
    """MCP-relevante Settings Schema"""
    return {
        "git": {
            "auto_checkpoint": {
                "type": "boolean",
                "default": True,
                "label": "Auto Checkpoint",
                "description": "Erstellt automatisch Git Commits vor Agent-Runs"
            },
        },
        "agent": {
            "max_turns": {
                "type": "number",
                "default": 10,
                "min": 1,
                "max": 50,
                "label": "Max Agent Turns"
            },
        },
    }
```

**Registrieren in:** `backend/src/api/routes/__init__.py`

#### 8.3 Frontend - Schema Types erweitern

**Datei:** `frontend/src/lib/types/schema.ts`

```typescript
// NEU: Erweiterte Enum-Option
export interface EnumOption {
  value: string;
  label: string;
  description?: string;
  icon?: string;
}

export interface EnumsResponse {
  task_status: EnumOption[];
  task_type: EnumOption[];
  agent_run_status: EnumOption[];
}
```

#### 8.4 Frontend - Schema Service erweitern

**Datei:** `frontend/src/lib/services/schema.ts`

```typescript
import type { EnumsResponse } from '$lib/types/schema';

let enumsCache: EnumsResponse | null = null;

export async function fetchEnums(): Promise<EnumsResponse> {
  if (enumsCache) return enumsCache;

  const response = await fetch('/api/schema/enums');
  if (!response.ok) throw new Error('Failed to fetch enums');

  enumsCache = await response.json();
  return enumsCache;
}

// Helper für schnellen Lookup
export function getEnumLabel(
  enums: EnumsResponse,
  enumType: keyof EnumsResponse,
  value: string
): string {
  const option = enums[enumType].find(o => o.value === value);
  return option?.label ?? value;
}
```

#### 8.5 Frontend - Hardcoded Constants entfernen

**Datei:** `frontend/src/lib/types/task.ts`

```typescript
// ENTFERNEN:
export const TASK_TYPE_LABELS: Record<TaskType, string> = { ... };
export const TASK_STATUS_LABELS: Record<TaskStatus, string> = { ... };

// BEHALTEN (nur Farben, da CSS):
export const TASK_TYPE_COLORS: Record<TaskType, string> = { ... };
```

#### 8.6 Frontend - Komponenten anpassen

**TaskCard.svelte:** Labels aus Schema statt hardcoded

```svelte
<script lang="ts">
  import { fetchEnums, getEnumLabel } from '$lib/services/schema';

  const enums = $state<EnumsResponse | null>(null);

  $effect(() => {
    fetchEnums().then(e => enums = e);
  });

  const typeLabel = $derived(
    enums ? getEnumLabel(enums, 'task_type', task.type) : task.type
  );
</script>

<span>{typeLabel}</span>
```

**Column.svelte:** Header aus Schema

**AgentList.svelte:** Status-Labels aus Schema

---

## Betroffene Dateien (Übersicht)

### Backend

| Datei | Aktion |
|-------|--------|
| `src/api/routes/schema.py` | Enum-Response erweitern |
| `src/api/routes/settings.py` | NEU erstellen |
| `src/api/routes/__init__.py` | Settings Router registrieren |
| `tests/test_schema.py` | Tests anpassen |

### Frontend

| Datei | Aktion |
|-------|--------|
| `src/lib/types/schema.ts` | EnumOption Interface |
| `src/lib/services/schema.ts` | fetchEnums() |
| `src/lib/types/task.ts` | Labels entfernen |
| `src/lib/types/agent.ts` | Labels entfernen |
| `src/lib/components/kanban/TaskCard.svelte` | Schema nutzen |
| `src/lib/components/kanban/Column.svelte` | Schema nutzen |
| `src/lib/components/panel/AgentList.svelte` | Schema nutzen |
| `src/lib/components/panel/SettingsPanel.svelte` | Backend/UI trennen |

---

## Aktueller Stand

### Was funktioniert ✅

- Backend: 72 Tests passing
- Frontend: 0 Errors, 0 Warnings
- TaskEditor: Bereits schema-driven
- FieldRenderer: Generisch und wiederverwendbar
- MCP Server: Funktioniert headless

### Was noch hardcoded ist ❌

| Komponente | Hardcoded | Sollte aus Schema |
|------------|-----------|-------------------|
| TaskCard | Type Labels | ✓ |
| TaskCard | Type Icons | ✓ |
| TaskCard | Dropdown-Menü | Optional |
| Column | Status Labels | ✓ |
| AgentList | Status Labels | ✓ |
| SettingsPanel | Alle Settings | Nur MCP-relevante |

---

## Commands

```bash
# Backend
cd backend
uv run pytest -v              # Tests (72 passing)
uv run ruff check --fix .     # Lint
uvx ty check                  # Type check

# Frontend
cd frontend
bunx biome check --write .    # Lint + Format
bunx svelte-check             # Type check (0 errors)

# Beide
make dev                      # Server starten
make check                    # Quality Gates
```

---

## ⚠️ Bekannte Issues

1. **Biome False Positives** - Svelte Component Imports als "unused" gemeldet
2. **A11y Warning** - Form fields ohne id/name (minor)

---

## Referenzen

- `ARCHITECTURE.md` - System-Architektur + Backend/Frontend Aufteilung
- `dev/PLAN.md` - Phase 8 Tasks
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme
- `.claude/plans/ancient-brewing-mochi.md` - Detaillierter Implementierungsplan

---

*Updated: 2026-01-21*
