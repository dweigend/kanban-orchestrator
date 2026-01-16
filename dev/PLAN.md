# PLAN: Kanban Orchestrator

## Vision

AI-gestützter Workflow-Orchestrator mit Kanban-Board UI für automatisierte Recherche, Programmierung und Prototyping.

**Kernprinzip:** Kanban = Stabile Orchestration, MCPs = Austauschbare Features

---

## Abgeschlossene Phasen

### Phase 1-3: Infrastructure ✅
- Backend: FastAPI + SQLAlchemy + SSE
- Frontend: SvelteKit + bits-ui + Tailwind
- Task CRUD mit Live-Updates

### Phase 4.1: Agent MVP ✅
- Claude Agent SDK Integration
- Project/AgentRun Models
- MCP Registry + Filesystem Server
- Git Auto-Checkpoints
- SSE Agent Log Streaming

### Phase 4.2: Agent UI Integration ✅
- Run Button auf TaskCard
- AgentLog Tab in Sidebar
- NEEDS_REVIEW Spalte
- Spinner während Agent läuft

---

## Aktuelle Phase: 5 - Modulares Backend

**Ziel:** Clean Code, Separation of Concerns

### Tasks
- [ ] `mcp_servers/` → `mcp/` umbenennen
- [ ] `orchestrator.py` aufteilen (< 100 Zeilen)
- [ ] `agent_service.py` extrahieren
- [ ] `prompts.py` für Templates
- [ ] Leere Ordner löschen (`plugins/`, `tools/`)

**Referenz:** → `dev/MCP-ARCHITECTURE.md` Abschnitt 5

---

## Phase 6: Kanban als MCP Server

**Ziel:** Claude Code kann Tasks erstellen

### Tasks
- [ ] FastMCP installieren (`uv add fastmcp`)
- [ ] `mcp/kanban_server.py` erstellen
- [ ] Tools: create_task, list_tasks, get_task_result
- [ ] In Claude Code registrieren

**Referenz:** → `dev/MCP-ARCHITECTURE.md` Abschnitt 3.3

---

## Phase 7: Plugin Manager

**Ziel:** MCPs aus Registry installieren

### Tasks
- [ ] `models/plugin.py` Model
- [ ] `mcp/discovery.py` Glama API Client
- [ ] `api/routes/plugins.py` REST Endpoints
- [ ] Frontend: Plugin Manager Tab
- [ ] Search + Install + Configure UI

**Referenz:** → `dev/MCP-ARCHITECTURE.md` Abschnitt 7

---

## Phase 8: Bidirektionaler Workflow

**Ziel:** Vollständiger Flow UI↔Agent↔MCPs

### Tasks
- [ ] NEEDS_REVIEW Flow implementieren
- [ ] Agent setzt Status korrekt
- [ ] Claude Code → Kanban → Ergebnis zurück
- [ ] Polling oder Notification für Completion

**Referenz:** → `dev/MCP-ARCHITECTURE.md` Abschnitt 4

---

## Backlog

- [ ] Vite Proxy für Production CORS
- [ ] Multi-Project Support (Project Selector)
- [ ] Knowledge DBs (thematische Spezialisierung)
- [ ] Workflow Templates

---

*Updated: 2026-01-16*
