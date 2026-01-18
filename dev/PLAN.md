# PLAN: Kanban Orchestrator

## Vision

AI-Workflow-Orchestrator mit Kanban-Board UI.

**Prinzip:** Backend = Source of Truth, Frontend rendert dynamisch

---

## Abgeschlossen ✅

- **Phase 1-3:** Infrastructure (FastAPI, SvelteKit, CRUD, SSE)
- **Phase 4:** Agent MVP (Claude SDK, MCP, Git Checkpoints)
- **Phase 5:** Modulares Backend
- **Phase 6:** Kanban als MCP Server
- **Phase 7.1:** Tests (44 passed)
- **Phase 7.2:** E2E Testing & Bugfixes
- **Phase 7.3 Session A:** Backend Cleanup + Schema-Endpoints (72 Tests)
- **Phase 7.3 Session B:** Frontend Schema-Integration + Bug Fix ✅

---

## Aktuelle Phase: 8 - Frontend Improvements 🎨

### Quick Wins

- [ ] Biome false-positive Warnings beheben
- [ ] Form field id/name Attribut (A11y)
- [ ] Loading States für API Calls

### Features

- [ ] ProjectEditor mit Schema-Integration
- [ ] Agent Log Panel - mehr Details, besseres UI
- [ ] Board View - Drag & Drop optimieren
- [ ] Error Handling - User-friendly Messages

### Nice to Have

- [ ] Dark Mode / Theme System
- [ ] Keyboard Shortcuts
- [ ] Mobile Responsive

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

---

## API-Endpoints

| Gruppe | Endpoints |
|--------|-----------|
| Tasks | `/api/tasks`, `/api/tasks/{id}` |
| Projects | `/api/projects`, `/api/projects/{id}` |
| Agent | `/api/agent/run`, `/api/agent/stop/{id}`, `/api/agent/runs` |
| Schema | `/api/schema/task`, `/api/schema/project`, `/api/schema/agent-run`, `/api/schema/enums` |
| Events | `/api/events` (SSE) |

---

## Dokumentation

- `dev/HANDOVER.md` - Session Handover
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme & Lösungen
- `dev/WORKFLOW.md` - Development Workflow

---

*Updated: 2026-01-18*
