# PLAN: Kanban Orchestrator

## Vision

AI-Workflow-Orchestrator mit Kanban-Board UI.

**Prinzip:** Backend = Source of Truth, Frontend rendert dynamisch

**Architektur:** Siehe `ARCHITECTURE.md` (Root) für Backend/Frontend Aufteilung

---

## Abgeschlossen ✅

- **Phase 1-3:** Infrastructure (FastAPI, SvelteKit, CRUD, SSE)
- **Phase 4:** Agent MVP (Claude SDK, MCP, Git Checkpoints)
- **Phase 5:** Modulares Backend
- **Phase 6:** Kanban als MCP Server
- **Phase 7.1:** Tests (44 passed)
- **Phase 7.2:** E2E Testing & Bugfixes
- **Phase 7.3 Session A:** Backend Cleanup + Schema-Endpoints (72 Tests)
- **Phase 7.3 Session B:** Frontend Schema-Integration (TaskEditor) ✅

---

## Aktuelle Phase: 8 - Schema-Driven UI 🏗️

**Ziel:** Frontend bezieht alle MCP-relevanten Daten vom Backend. UI-Präferenzen bleiben lokal.

### 8.1 Backend - Enum-Erweiterung

- [ ] `/api/schema/enums` erweitern mit Metadaten
  - Labels: `"To Do"` statt nur `"todo"`
  - Icons: `"MagnifyingGlass"` für Research
  - Descriptions: Tooltips

### 8.2 Backend - Settings Endpoint

- [ ] `/api/settings/schema` - MCP-relevante Settings
  - Git: Auto-Checkpoint, Prefix
  - Agent: Model, Max Turns

### 8.3 Frontend - Schema-Service

- [ ] `fetchEnums()` für erweiterte Enums
- [ ] Caching der Schema-Responses
- [ ] TypeScript Interfaces anpassen

### 8.4 Frontend - Hardcoded Constants entfernen

- [ ] `types/task.ts` - TASK_TYPE_LABELS, TASK_STATUS_LABELS → Schema
- [ ] `types/agent.ts` - Agent-Labels → Schema

### 8.5 Frontend - Komponenten umstellen

| Komponente | Status | Änderung |
|------------|--------|----------|
| `TaskEditor.svelte` | ✅ | Bereits schema-driven |
| `TaskCard.svelte` | ❌ | Labels + Icons aus Schema |
| `Column.svelte` | ❌ | Header-Labels aus Schema |
| `ProjectOverview.svelte` | ❌ | Schema nutzen |
| `AgentList.svelte` | ❌ | Status-Labels aus Schema |
| `SettingsPanel.svelte` | ❌ | Backend/UI Settings trennen |

### 8.6 Cleanup

- [ ] Biome false-positive Warnings
- [ ] Form field id/name A11y

---

## Nächste Phasen

### Phase 9: Plugin Manager

- MCP Registry Integration (Glama API)
- Plugin Install/Configure UI

### Phase 10: Advanced Features

- NEEDS_REVIEW Flow
- Knowledge DBs Integration
- Multi-Project Support

---

## Backlog

- Project Selector UI
- Task Dependencies
- Bulk Operations
- Export/Import
- Keyboard Shortcuts
- Mobile Responsive

---

## API-Endpoints

| Gruppe | Endpoints |
|--------|-----------|
| Tasks | `/api/tasks`, `/api/tasks/{id}` |
| Projects | `/api/projects`, `/api/projects/{id}` |
| Agent | `/api/agent/run`, `/api/agent/stop/{id}`, `/api/agent/runs` |
| Schema | `/api/schema/task`, `/api/schema/project`, `/api/schema/agent-run`, `/api/schema/enums` |
| Settings | `/api/settings/schema` (TODO) |
| Events | `/api/events` (SSE) |

---

## Dokumentation

- `ARCHITECTURE.md` - System-Architektur + Backend/Frontend Aufteilung
- `dev/HANDOVER.md` - Session Handover
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme & Lösungen
- `dev/WORKFLOW.md` - Development Workflow

---

*Updated: 2026-01-21*
