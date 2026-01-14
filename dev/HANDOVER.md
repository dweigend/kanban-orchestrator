# HANDOVER

## Session: 2026-01-14 - Phase 4 Agent Integration (MVP) ✅

### Summary

Agent-System MVP implementiert! Claude Agent SDK integriert mit:
- Project/AgentRun Models für Multi-Project Support
- MCP Plugin-Architektur mit Filesystem Server
- Orchestrator Agent für Task-Ausführung
- Git Auto-Checkpoints vor jeder Task-Änderung
- SSE Agent Log Streaming zum Frontend

### Completed

- ✅ **Project Model** - Workspace-Pfad für Agent-Sandbox
- ✅ **AgentRun Model** - Tracking von Agent-Ausführungen
- ✅ **Task erweitert** - description, project_id, parent_id, NEEDS_REVIEW status
- ✅ **MCP Registry** - Modulare Tool-Registrierung
- ✅ **Filesystem MCP** - Read/Write/List innerhalb Workspace
- ✅ **Orchestrator Agent** - Claude SDK Integration mit bypassPermissions
- ✅ **Git Integration** - Auto-Checkpoint vor Tasks, Commit bei Erfolg
- ✅ **Agent API** - /api/agent/run, /stop, /runs endpoints
- ✅ **SSE agent_log** - Live-Streaming von Agent-Output
- ✅ **AgentLog Component** - Sidebar-Komponente für Log-Anzeige

### Architecture

```
Backend
├── src/models/
│   ├── project.py      # Project with workspace_path
│   ├── agent_run.py    # AgentRun tracking
│   └── task.py         # Extended with description, parent_id
├── src/mcp_servers/
│   ├── registry.py     # MCP tool registration
│   └── filesystem/     # Sandboxed file I/O
├── src/agents/
│   └── orchestrator.py # Claude Agent SDK integration
└── src/api/routes/
    ├── projects.py     # Projects CRUD
    └── agent.py        # Agent run/stop/list

Frontend
├── src/lib/types/
│   ├── task.ts         # + NEEDS_REVIEW status
│   └── agent.ts        # + AgentRun, AgentLogEntry
├── src/lib/services/
│   ├── agent.ts        # Agent API client
│   └── events.ts       # + agent_log SSE handling
└── src/lib/components/panel/
    └── AgentLog.svelte # Log display component
```

### Key Decisions

1. **Claude Agent SDK subprocess** - Nutzt Claude Max Abo, keine extra API-Kosten
2. **MCP in src/mcp_servers/** - Eigener Ordner statt `src/mcp` (Konflikt mit mcp package)
3. **NEEDS_REVIEW Status** - Vorbereitet für Human-in-the-Loop
4. **Git Auto-Checkpoints** - Sicherheit vor Agent-Änderungen
5. **bypassPermissions Mode** - YOLO-Mode für Agent innerhalb Workspace

### Open for Phase 4.2

- [ ] NEEDS_REVIEW Spalte im Kanban Board
- [ ] Run Button auf TaskCard
- [ ] AgentLog in Sidebar integrieren
- [ ] Perplexity MCP Server
- [ ] Workflow Templates in DB
- [ ] Multi-Project UI (Project Selector)

### Verification

```bash
# Backend
cd backend && uvx ty check  # All checks passed
uv run ruff check --fix . && uv run ruff format .  # Clean

# Frontend
cd frontend && bunx svelte-check --threshold warning  # 0 errors, 3 warnings
bunx biome check --write .  # Fixed
```

---

## Session: 2026-01-14 - Phase 5.8 UI Completion ✅

### Summary

Phase 5 komplett abgeschlossen! UI ist nun voll funktionsfähig:
- ✅ TaskCard Click → öffnet Editor in Sidebar
- ✅ Dropdown Edit/Delete funktional
- ✅ Drag & Drop zwischen Spalten
- ✅ Toast Notifications für Feedback

### Completed

- ✅ **Toast System** - svelte-sonner installiert + integriert
- ✅ **Handler Wiring** - Board erhält jetzt Edit/Delete/Drop Props
- ✅ **TaskCard Click** - Klick öffnet Editor mit Task-Daten
- ✅ **Drag & Drop** - Native HTML5, visuelles Feedback bei Drag/Drop

### Architecture Update

```
TaskCard (draggable)
  └── ondragstart → setData(taskId)
  └── onclick → handleEditTask(task)

Column (drop target)
  └── ondragover/drop → handleTaskDrop(taskId, newStatus)

+page.svelte (state management)
  └── handleEditTask() → editingTask + activeTab
  └── handleTaskDrop() → API call + Toast
  └── Toast notifications für alle Aktionen
```

### Key Files Changed

```
frontend/src/lib/services/toast.ts          # NEW: Toast helper
frontend/src/routes/+layout.svelte          # + Toaster component
frontend/src/routes/+page.svelte            # + handlers, - inline error
frontend/src/lib/components/kanban/
├── TaskCard.svelte                         # + draggable, + click
├── Column.svelte                           # + drop target
└── Board.svelte                            # + onTaskDrop prop
```

### Verification

Alle Tests bestanden:
- `bunx svelte-check --threshold warning` → 0 errors, 3 warnings (a11y)
- Task erstellen/bearbeiten/löschen → Success Toast
- Task draggen → Status Update + Toast
- Klick auf TaskCard → Editor öffnet

---

## Session: 2026-01-14 - Phase 5.7 API Integration

### Summary

Frontend mit Backend verbunden. Task CRUD + SSE Live-Updates funktionieren.

### Completed

- ✅ Types erweitert: `BackendTaskStatus`, Status-Mapper, `mapBackendToTask()`
- ✅ API Client: `services/api.ts` (fetch wrapper + ApiError)
- ✅ Task Service: `services/tasks.ts` (CRUD operations)
- ✅ SSE Service: `services/events.ts` (subscribeToEvents)
- ✅ Form Validation: `validateForm()` in TaskEditor
- ✅ Page Integration: `+page.svelte` mit API-Calls + SSE
- ✅ CORS Fix: `allow_origin_regex` für alle localhost-Ports
- ✅ Bug Fix: Duplicate Key Error (SSE-only für Create)

### Architecture

```
Frontend (SvelteKit)          Backend (FastAPI)
─────────────────────         ─────────────────
+page.svelte                  /api/tasks (CRUD)
  └── $effect() ──────────────► GET /api/tasks
  └── handleTaskSave() ───────► POST/PUT /api/tasks
  └── handleTaskDelete() ─────► DELETE /api/tasks
  └── subscribeToEvents() ◄───► GET /api/events (SSE)

services/
  ├── api.ts      → fetch wrapper
  ├── tasks.ts    → CRUD operations
  └── events.ts   → SSE subscription

types/task.ts
  ├── TaskStatus (uppercase: TODO, IN_PROGRESS, DONE)
  ├── BackendTaskStatus (lowercase: todo, in_progress, done)
  └── mapBackendToTask(), mapTaskToCreatePayload()
```

### Key Decisions

1. **SSE für Create** - Kein lokales Hinzufügen, SSE fügt Task hinzu → vermeidet Duplikate
2. **CORS Regex** - `allow_origin_regex=r"http://localhost:\d+"` für Dev
3. **Status Mapping** - Frontend uppercase, Backend lowercase mit Mapper-Functions
4. **Local-only Fields** - `type`, `description` nur im Frontend (Backend speichert sie nicht)

### Open Issues

- [ ] TaskCard Click → Edit in Sidebar
- [ ] Drag & Drop für Status-Änderung
- [ ] Backend: `type`, `description` Felder hinzufügen

### Next Session

1. **TaskCard Integration** - Click öffnet Editor mit Task-Daten
2. **Drag & Drop** - Tasks zwischen Spalten verschieben
3. **Backend erweitern** - `type`, `description` zu Task Model

### Files Changed

```
frontend/src/lib/
├── types/task.ts           # + BackendTaskStatus, Mapper
├── services/
│   ├── api.ts              # NEW: fetch wrapper
│   ├── tasks.ts            # NEW: CRUD
│   └── events.ts           # NEW: SSE
├── components/panel/
│   ├── TaskEditor.svelte   # + validateForm()
│   └── FunctionPanel.svelte # + onTaskDelete prop
└── routes/+page.svelte     # Refactored for API

backend/
└── main.py                 # CORS regex fix
```

### Blockers

- Keine

---

## Session: 2026-01-13 (Abend 2) - UX Refactor: Einheitliche Menüstruktur

### Summary

Doppelte Menü-Struktur eliminiert. Alle Navigation jetzt im Header, Sidebar zeigt nur Inhalt.

### Completed

- ✅ Header: Sidebar-Tabs als Icon-Buttons (📊 🤖 ⚙️ ➕)
- ✅ Header: Sidebar-Toggle Button (◧)
- ✅ Sidebar: Tab-Leiste komplett entfernt
- ✅ Sidebar: Nur noch Inhalt (Overview/Agents/Settings/TaskEditor)
- ✅ Sidebar: Resizable via Drag am linken Rand
- ✅ TaskEditor: X-Button entfernt (Cancel = anderer Tab)
- ✅ Controlled Component Pattern: activeTab State in Page

---

*Previous sessions archived...*
