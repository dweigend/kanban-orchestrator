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

---

## Aktuelle Phase: 7.3 - Cleanup 🧹

### Session A: Backend ✅

- [x] Pydantic Schemas vervollständigen
- [x] Error Handling standardisieren (Logging)
- [x] Tests ergänzen (72 total)
- [x] Schema-Endpoints implementieren

### Session B: Frontend (nächste)

- [ ] Unused Imports entfernen
- [ ] Schema-API nutzen für dynamisches Rendering
- [ ] TypeScript Typen synchronisieren
- [ ] A11y Warnings fixen

---

## Nächste Phasen

### Phase 8: Schema-Driven UI

- Frontend nutzt `/api/schema/*` Endpoints
- Dynamische Form-Generierung
- OpenAPI Codegen evaluieren

### Phase 9: Plugin Manager

- MCP Registry Integration (Glama API)
- Plugin Install/Configure UI

---

## Backlog

- NEEDS_REVIEW Flow
- Project Selector UI
- Knowledge DBs

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

*Updated: 2026-01-17*
