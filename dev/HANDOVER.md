# HANDOVER

## Session: 2026-01-14 - Phase 4 Agent Integration (MVP) ✅

### Was wurde gebaut

Agent-System MVP mit Claude Agent SDK:

```
Backend                              Frontend
────────                             ────────
src/models/                          src/lib/
├── project.py     # Workspace       ├── types/agent.ts    # AgentRun types
├── agent_run.py   # Run tracking    ├── services/agent.ts # API client
└── task.py        # +description    └── components/panel/
                   # +parent_id          └── AgentLog.svelte
src/mcp_servers/
├── registry.py    # Tool registry   src/lib/services/
└── filesystem/    # File I/O        └── events.ts  # +agent_log SSE
    └── server.py
                                     src/lib/types/
src/agents/                          └── task.ts    # +NEEDS_REVIEW
└── orchestrator.py # Claude SDK

src/api/routes/
├── projects.py    # CRUD
└── agent.py       # run/stop/list
```

### Implementierte Features

- ✅ **Project Model** - Workspace-Pfad für Agent-Sandbox
- ✅ **AgentRun Model** - Status: pending/running/completed/failed
- ✅ **Task erweitert** - description, project_id, parent_id, NEEDS_REVIEW
- ✅ **MCP Registry** - Modulare Tool-Registrierung in `src/mcp_servers/`
- ✅ **Filesystem MCP** - read_file, write_file, list_directory (sandboxed)
- ✅ **Orchestrator** - Claude Agent SDK mit bypassPermissions
- ✅ **Git Integration** - Auto-Checkpoint vor Task, Commit bei Erfolg
- ✅ **SSE agent_log** - Live-Streaming von Agent-Output
- ✅ **AgentLog Component** - Sidebar-Komponente (noch nicht eingebunden)

### Key Decisions

1. **Claude Agent SDK subprocess** - Nutzt Max Abo, keine API-Kosten
2. **MCP in `src/mcp_servers/`** - Nicht `src/mcp` (Konflikt mit mcp package)
3. **bypassPermissions Mode** - YOLO innerhalb Workspace
4. **Git Auto-Checkpoints** - Sicherheit vor Agent-Änderungen

### API Endpoints (neu)

```
POST /api/projects          # Create project
GET  /api/projects          # List all
GET  /api/projects/{id}     # Get one
PUT  /api/projects/{id}     # Update
DELETE /api/projects/{id}   # Delete

POST /api/agent/run         # Start agent for task
POST /api/agent/stop/{id}   # Stop running agent
GET  /api/agent/runs        # List runs (filter: task_id, status)
GET  /api/agent/runs/{id}   # Get run details
```

---

## Nächste Session: Phase 4.2

### Priority 1: UI Integration

```
[ ] Run Button auf TaskCard
[ ] AgentLog Tab in Sidebar einbinden
[ ] NEEDS_REVIEW Spalte im Board
[ ] Spinner auf Card während Agent läuft
```

### Priority 2: Multi-Project

```
[ ] Project Selector im Header
[ ] Tasks nach Project filtern
[ ] Default Project bei App-Start
```

### Priority 3: Weitere MCP Server

```
[ ] Perplexity MCP (Web Search)
[ ] Workflow Templates in DB
```

### ✅ ARCHITECTURE.md erstellt

Umfassende Systemdokumentation mit:
- Datenfluss-Diagramme (ASCII)
- Komponenten-Übersicht (Backend + Frontend)
- API-Referenz
- Status-Tabellen (implementiert vs. geplant)
- Design Decisions

---

## Verification Commands

```bash
# Backend
cd backend && uvx ty check
uv run ruff check --fix . && uv run ruff format .

# Frontend
cd frontend && bunx svelte-check --threshold warning
bunx biome check --write .
```

---

*Updated: 2026-01-14*
