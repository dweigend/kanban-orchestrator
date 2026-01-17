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

### Phase 5: Modulares Backend ✅
- `orchestrator.py` refactored (272 → 199 Zeilen)
- `services/git.py` extrahiert
- Dokumentation aktualisiert

### Phase 6: Kanban als MCP Server ✅

**Ziel:** Claude Code kann Tasks erstellen

**Erledigt:**
- [x] FastMCP installiert
- [x] Namespace-Kollision gelöst (`mcp/` → `mcp_servers/` + `mcp_client/`)
- [x] `kanban_server.py` mit 3 Tools (create_task, list_tasks, get_task_result)
- [x] `.mcp.json` für Claude Code Integration
- [x] Naming Conventions dokumentiert in ARCHITECTURE.md

**Referenz:** → `dev/MCP-ARCHITECTURE.md` Abschnitt 3.3

### Phase 7.1: Cleanup & Testing ✅

**Ziel:** Technische Schulden vor Plugin Manager beheben

**Erledigt:**
- [x] Test-Infrastruktur (pytest-asyncio, conftest.py, in-memory SQLite)
- [x] 44 Tests (Task CRUD, Project CRUD, Agent API, MCP Server)
- [x] Error Handling für `kanban_server.py` (KanbanAPIError, input validation)
- [x] Bug fix: `AgentRunResponse.started_at` optional

---

## Aktuelle Phase: 7.2 - Test-Session & Debugging 🧪

**Ziel:** System End-to-End testen und alle Bugs fixen

**Tracking:** → `dev/DEBUG-REPORT.md`

### Workflow
1. Alle Issues in DEBUG-REPORT.md dokumentieren
2. Issues einzeln abarbeiten (🔴 → 🟡 → 🟢)
3. Fixes verifizieren
4. Erst wenn alles 🟢 → weiter zu Phase 7

### Bekannte Issues
- [x] Port 8000 belegt → Makefile auto-cleanup
- [x] DB Schema veraltet → `rm backend/kanban.db`
- [ ] Weitere Issues → siehe DEBUG-REPORT.md

### Tests
- [ ] Backend API (Task/Project/Agent CRUD)
- [ ] Frontend UI (Kanban Board, Drag&Drop)
- [ ] Agent Flow (Task → Agent → Completion)
- [ ] SSE Events (Live-Updates)
- [ ] MCP Server (Claude Code Integration)

---

## Phase 7: Plugin Manager

**Ziel:** MCPs aus Registry installieren

### Tasks
- [ ] `models/plugin.py` Model
- [ ] `mcp_client/discovery.py` Glama API Client
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

### Architektur-Verbesserungen
- [ ] **Schema-Driven UI** - Backend definiert Felder dynamisch, Frontend rendert
  - **Priorität: HOCH** - Fundamental für Flexibilität
  - Backend liefert Field-Definitionen: `{type: "text"|"textarea"|"result"|"checklist", name: string, ...}`
  - Frontend hat Pool von UI-Komponenten, rendert basierend auf Schema
  - Keine harte Kopplung mehr zwischen Backend-Model und Frontend-Types
  - Ermöglicht: Unterschiedliche Task-Types, MCP-spezifische Felder, dynamische Erweiterungen
- [ ] **OpenAPI Codegen** - TypeScript-Types aus Pydantic generieren
  - Löst: ARCH-001, ARCH-002, ARCH-004 (siehe DEBUG-REPORT.md)
  - `npx openapi-typescript http://localhost:8000/openapi.json -o src/lib/types/api.ts`
- [ ] **Runtime-Validierung (Zod)** - Frontend validiert Backend-Responses
  - Löst: ARCH-003
- [ ] **Project Selector UI** - Frontend nutzt Project-API (existiert bereits im Backend)

### Infrastruktur
- [ ] Vite Proxy für Production CORS
- [ ] Knowledge DBs (thematische Spezialisierung)
- [ ] Workflow Templates

---

*Updated: 2026-01-16 (Backlog: Architektur-Verbesserungen)*
