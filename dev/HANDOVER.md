# HANDOVER

## Phase: 7.3 - Cleanup 🧹

---

## Session 2026-01-17 (Backend A) ✅

### A.1 - Cleanup

1. **AgentRun `created_at`** - Konsistenz mit Task/Project
2. **Logging in Routes** - Warning-Logs vor HTTPExceptions
3. **Tests erweitert** - 72 Tests total (vorher 56)
   - `test_agent.py` - Skip behoben, 4 neue Tests
   - `test_git.py` - 8 neue Tests (NEU)
   - `test_events.py` - 8 neue Tests (NEU)

### A.2 - Schema-Endpoints

**Neue API:**

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /api/schema/task` | Field-Definitionen für Task-Formulare |
| `GET /api/schema/project` | Field-Definitionen für Project-Formulare |
| `GET /api/schema/agent-run` | Field-Definitionen für AgentRun-Anzeige |
| `GET /api/schema/enums` | Alle Enum-Werte |

**Neue Pydantic-Types:**
- `FieldType` - UI-Rendering-Hints (text, textarea, select, readonly, datetime)
- `SchemaField` - Field-Definition mit name, type, required, description, options
- `EntitySchema` - Liste von SchemaFields

**Erweiterbarkeit:** GitHub Issue #7 dokumentiert zukünftige FieldTypes.

---

## Architektur: Backend = Source of Truth ✅

### Implementiert

Das Schema-System ermöglicht dynamisches Frontend-Rendering:

```
Backend (Pydantic)              Frontend (Svelte)
─────────────────              ─────────────────
GET /api/schema/task     →     Liest Schema
  fields: [                    Rendert dynamisch
    {name: "title",              <TextInput />
     type: "text",               <TextArea />
     required: true},            <Select options={...} />
    {name: "status",
     type: "select",
     options: [...]}
  ]
```

### Vorteile

- Eine Quelle der Wahrheit (Single Source of Truth)
- Neue Felder im Backend → Frontend zeigt sie automatisch
- Enum-Werte nicht mehr hardcoded im Frontend
- LLMs können Backend-Schemas direkt nutzen

---

## Backend-Struktur (aktuell)

```
backend/src/
├── api/
│   ├── routes/
│   │   ├── tasks.py          # Task CRUD
│   │   ├── projects.py       # Project CRUD
│   │   ├── agent.py          # Agent runs
│   │   ├── events.py         # SSE
│   │   └── schema.py         # Schema-Endpoints ✅ NEU
│   ├── schemas.py            # Pydantic (inkl. FieldType, SchemaField)
│   ├── task_service.py
│   └── project_service.py
│
├── services/
│   └── git.py                # Git checkpoint/commit
│
├── agents/
│   └── orchestrator.py       # Claude Agent SDK
│
├── mcp_servers/              # Kanban als MCP
│   └── server.py
│
├── models/
│   ├── task.py
│   ├── project.py
│   └── agent_run.py
│
└── database.py
```

---

## Nächste Session: B (Frontend)

**Checklist:**
- [ ] Unused Imports entfernen (Biome Warnings)
- [ ] Schema-API nutzen für dynamisches Rendering
- [ ] TypeScript Types synchronisieren (oder entfernen)
- [ ] A11y Warnings fixen

---

## Commands

```bash
# Backend
cd backend
uv run pytest -v              # 72 Tests
uv run ruff check --fix .     # Lint
uvx ty check                  # Type check

# Frontend
cd frontend
bunx biome check --write .    # Lint + Format
bunx svelte-check             # Type check

# Beide
make dev                      # Server starten
make check                    # Quality Gates
```

---

## API-Übersicht

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/tasks` | GET, POST | Task CRUD |
| `/api/tasks/{id}` | GET, PUT, DELETE | Single Task |
| `/api/projects` | GET, POST | Project CRUD |
| `/api/projects/{id}` | GET, PUT, DELETE | Single Project |
| `/api/agent/run` | POST | Agent starten |
| `/api/agent/stop/{id}` | POST | Agent stoppen |
| `/api/agent/runs` | GET | Runs auflisten |
| `/api/schema/task` | GET | Task-Schema |
| `/api/schema/project` | GET | Project-Schema |
| `/api/schema/agent-run` | GET | AgentRun-Schema |
| `/api/schema/enums` | GET | Alle Enums |
| `/api/events` | GET (SSE) | Real-time Updates |

---

*Updated: 2026-01-17*
