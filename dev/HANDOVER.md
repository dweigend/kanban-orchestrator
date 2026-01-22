# HANDOVER

## Phase: 8 - Schema-Driven UI ✅

---

## Session 2026-01-21 (Implementation) ✅

### Was wurde gemacht

1. **Backend: Enum-Erweiterung (8.1)**
   - `EnumOption`, `TaskStatusOption`, `TaskTypeOption` Pydantic Models
   - `/api/schema/enums` liefert jetzt Metadaten (label, icon, prefix, description)
   - Tests erweitert (3 neue Tests)

2. **Backend: Settings Endpoint (8.2)**
   - Neuer `/api/settings/schema` Endpoint
   - Git Settings (auto_checkpoint, checkpoint_prefix)
   - Agent Settings (max_turns, model)
   - Tests erstellt

3. **Frontend: Schema Store**
   - Neuer `$lib/stores/schema.svelte.ts` mit Svelte 5 Runes
   - `initSchemaStore()` im Layout
   - Helper: `getStatusLabel()`, `getTypeLabel()`, `getTypeIcon()`, `getTypePrefix()`

4. **Frontend: Komponenten umgestellt**
   - `Column.svelte` → nutzt `getStatusLabel()`
   - `TaskCard.svelte` → nutzt `getTypeIcon()`, `getTypePrefix()`
   - `TaskEditor.svelte` → Labels aus Schema Store

5. **Deprecated markiert**
   - `TASK_TYPE_LABELS` in task.ts
   - `TASK_STATUS_LABELS` in task.ts

### Test-Ergebnisse

| Check | Ergebnis |
|-------|----------|
| Backend Tests | 77 passed ✅ |
| Backend Types | All checks passed ✅ |
| Frontend Types | 0 errors, 0 warnings ✅ |
| Browser Test | UI funktioniert ✅ |

### Neue Dateien

```
backend/
├── src/api/routes/settings.py      # NEU
└── tests/test_settings.py          # NEU

frontend/
└── src/lib/stores/schema.svelte.ts # NEU
```

### Geänderte Dateien

```
backend/
├── src/api/schemas.py              # EnumOption Models
├── src/api/routes/schema.py        # Enum Response erweitert
├── main.py                         # Settings Router
└── tests/test_schema.py            # Tests angepasst

frontend/
├── src/lib/types/schema.ts         # EnumOption Interfaces
├── src/lib/services/schema.ts      # Helper Functions
├── src/lib/types/task.ts           # @deprecated Annotations
├── src/routes/+layout.svelte       # initSchemaStore()
├── src/lib/components/kanban/Column.svelte
├── src/lib/components/kanban/TaskCard.svelte
└── src/lib/components/panel/TaskEditor.svelte
```

---

## API Endpoints (Neu)

### GET /api/schema/enums

```json
{
  "task_status": [
    {"value": "todo", "label": "To Do", "description": "Task nicht gestartet"},
    ...
  ],
  "task_type": [
    {"value": "research", "label": "Research", "icon": "MagnifyingGlass", "prefix": "RES"},
    ...
  ],
  "agent_run_status": [
    {"value": "pending", "label": "Pending"},
    ...
  ]
}
```

### GET /api/settings/schema

```json
{
  "git": {
    "auto_checkpoint": {"type": "boolean", "default": true, ...},
    "checkpoint_prefix": {"type": "string", "default": "checkpoint:", ...}
  },
  "agent": {
    "max_turns": {"type": "number", "default": 10, "min": 1, "max": 50, ...},
    "model": {"type": "select", "options": [...], ...}
  }
}
```

---

## Was noch offen ist

### Phase 8 Cleanup (Optional)

- [ ] Board.svelte: Columns aus Schema statt hardcoded
- [ ] Biome false-positive Warnings (Svelte Component Imports)
- [ ] TASK_TYPE_LABELS / TASK_STATUS_LABELS komplett entfernen

### Phase 9: Plugin Manager

- MCP Registry Integration (Glama API)
- Plugin Install/Configure UI

---

## Commands

```bash
# Backend
cd backend
uv run pytest -v                      # 77 Tests
uv run ruff check --fix . && uv run ruff format .
uvx ty check

# Frontend
cd frontend
bunx biome check --write .
bunx svelte-check --threshold warning

# Beide
make dev                              # Server starten
```

---

*Updated: 2026-01-22*
