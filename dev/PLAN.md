# PLAN: Kanban Orchestrator

## Vision

AI-Workflow-Orchestrator mit Kanban-Board UI.

**Prinzip:** Backend = Source of Truth, Frontend rendert dynamisch

**Neues Konzept (Phase 11):** Task-Delegations-System - Asynchrone Task-Verarbeitung aus verschiedenen Quellen (MCP, UI, API) mit Everything-via-MCP Architektur.

---

## Abgeschlossen ✅

- **Phase 1-3:** Infrastructure (FastAPI, SvelteKit, CRUD, SSE)
- **Phase 4:** Agent MVP (Claude SDK, MCP, Git Checkpoints)
- **Phase 5:** Modulares Backend
- **Phase 6:** Kanban als MCP Server
- **Phase 7.1:** Tests (44 passed)
- **Phase 7.2:** E2E Testing & Bugfixes
- **Phase 7.3 Session A:** Backend Cleanup + Schema-Endpoints (72 Tests)
- **Phase 7.3 Session B:** Frontend Schema-Integration (TaskEditor)
- **Phase 8:** Schema-Driven UI (77 Tests)
- **Phase 9:** Bug Fixes + UI Cleanup (13 Issues closed)
- **Phase 10:** Subtasks & Expand/Collapse Cards (#24) ✅
- **Phase 11A:** Task-Delegations-System Konzept ✅
- **Phase 11B:** Backend Task-Model Erweiterung (78 Tests) ✅

---

## Aktuelle Phase

### Phase 11C-F: Task-Delegations-System Implementation 🔲 NEXT

**Design:** Siehe `dev/DESIGN-TASK-DELEGATION.md`

---

## Nächste Phasen

### Phase 11C: MCP Registry

**Ziel:** Dynamische MCP-Konfiguration aus YAML-Datei

| Task | Beschreibung |
|------|--------------|
| 1 | `.kanban/mcps.yaml` Format definieren |
| 2 | YAML-Parser für MCP-Registry |
| 3 | `get_mcp_config()` liest aus YAML statt hardcoded |
| 4 | Validierung: nur enabled MCPs erlaubt |
| 5 | Environment-Variable Auflösung (`${SANDBOX_DIR}`) |

**Dateien:**
- `.kanban/mcps.yaml` (NEU)
- `backend/src/mcp_client/registry.py`

---

### Phase 11D: Templates

**Ziel:** Markdown-Templates für Agent-Output-Struktur

| Task | Beschreibung |
|------|--------------|
| 1 | `templates/` Ordner erstellen |
| 2 | `research.md`, `dev.md`, `notes.md` Templates |
| 3 | Template-Loader im Orchestrator |
| 4 | Template-Injection in Agent-Prompt |

**Dateien:**
- `templates/research.md` (NEU)
- `templates/dev.md` (NEU)
- `templates/notes.md` (NEU)
- `backend/src/agents/orchestrator.py`

---

### Phase 11E: Kanban MCP API Update

**Ziel:** Erweiterte API für Task-Erstellung via MCP

| Task | Beschreibung |
|------|--------------|
| 1 | `create_task()` mit optionalen Feldern erweitern |
| 2 | `get_task_options()` für Schema-Discovery implementieren |
| 3 | Validierung gegen MCP-Registry |
| 4 | Sofortige Response mit sandbox_dir Info |

**Dateien:**
- `backend/src/mcp_servers/kanban_server.py`

---

### Phase 11F: Frontend Anpassungen

**Ziel:** UI für neue Task-Felder

| Task | Beschreibung |
|------|--------------|
| 1 | TaskEditor: Neue Felder (target_path, read_paths, allowed_mcps, template) |
| 2 | Schema-Endpoint Integration für MCP-Liste |
| 3 | Optional-Fields UI (Collapsible "Advanced Settings") |
| 4 | Source-Badge auf TaskCard ("MCP", "UI") |

**Dateien:**
- `frontend/src/lib/components/panel/TaskEditor.svelte`
- `frontend/src/lib/types/task.ts`

---

### Phase 12: Trilium Integration

**Ziel:** Trilium Notes als Output-Target

| Task | Beschreibung |
|------|--------------|
| 1 | Trilium MCP recherchieren/einbinden |
| 2 | In MCP-Registry aktivieren |
| 3 | Als Output-Target in UI verfügbar machen |

---

### Phase 13: Plugin Manager (Optional)

- MCP Registry UI (statt nur YAML)
- Plugin Install/Configure UI
- Glama API Integration

---

### Phase 14: Advanced Features (Backlog)

- NEEDS_REVIEW Flow verbessern
- Knowledge DBs Integration
- Task Dependencies
- Bulk Operations
- Export/Import

---

## Aktuelle Issues

| Prio | # | Issue | Phase | Status |
|------|---|-------|-------|--------|
| - | #26 | Projektstruktur & Standardpfade | 11A | ✅ Konzept: Sandbox → Target |
| - | #25 | Erweiterte Task-Definition | 11B | 🔲 Implementation steht aus |
| - | #22 | Projekt-Management | Backlog | 🔲 Nach Phase 11 |

---

## API-Endpoints

| Gruppe | Endpoints | Status |
|--------|-----------|--------|
| Tasks | `/api/tasks`, `/api/tasks/{id}` | ✅ Working |
| Projects | `/api/projects`, `/api/projects/{id}` | ✅ Working (leer) |
| Agent | `/api/agent/run`, `/api/agent/stop/{id}`, `/api/agent/runs` | ✅ Working |
| Schema | `/api/schema/task`, `/api/schema/project`, `/api/schema/agent-run`, `/api/schema/enums` | ✅ Working |
| Settings | `/api/settings/schema` | ✅ Working |
| Events | `/api/events` (SSE) | ⚪ Not Tested |

**Geplante Endpoints (Phase 11E):**
- `GET /api/schema/task-create` - Optionen für Task-Erstellung (MCPs, Templates)

---

## Dokumentation

- `dev/ARCHITECTURE.md` - System-Architektur + Phase 11 Konzept
- `dev/DESIGN-TASK-DELEGATION.md` - Vollständiges Design Phase 11
- `dev/HANDOVER.md` - Session Handover
- `dev/ISSUE_TRACKER.md` - Bug Tracking + Feature Status
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme & Lösungen
- `dev/WORKFLOW.md` - Development Workflow

---

*Updated: 2026-01-24*
