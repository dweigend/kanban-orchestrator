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
- **Phase 8:** Schema-Driven UI (77 Tests) ✅

---

## Aktuelle Phase: Bug Fixes 🔴

**Status:** 13 Issues identifiziert in systematischer Test-Session (2026-01-22)

**Kritisches Problem:** Backend funktioniert (9 Tasks, 2 Agent Runs in DB), Frontend zeigt nichts an!

Siehe `dev/ISSUE_TRACKER.md` für vollständige Liste.

### Sprint 1: Make App Usable (CRITICAL)

| Issue | Beschreibung | Status |
|-------|--------------|--------|
| #6 | Tasks im Board anzeigen | ⬜ TODO |
| #7 | Plus-Buttons funktional | ⬜ TODO |

### Sprint 2: Core Features (HIGH)

| Issue | Beschreibung | Status |
|-------|--------------|--------|
| #8 | Agent Logs anzeigen | ⬜ TODO |
| #1 | Settings persistent (localStorage) | ⬜ TODO |
| #3 | Backend Settings in UI | ⬜ TODO |
| #9 | Project Menu funktional | ⬜ TODO |

### Sprint 3: UX Polish (MEDIUM)

| Issue | Beschreibung | Status |
|-------|--------------|--------|
| #4 | Search implementieren | ⬜ TODO |
| #10 | Hub/Board View unterscheiden | ⬜ TODO |

### Sprint 4: Cleanup (LOW)

| Issue | Beschreibung | Status |
|-------|--------------|--------|
| #5, #11, #12, #13 | Mock Data entfernen | ⬜ TODO |
| #2 | Appearance Section | ⬜ TODO |

---

## Nächste Phasen (nach Bug Fixes)

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

| Gruppe | Endpoints | Status |
|--------|-----------|--------|
| Tasks | `/api/tasks`, `/api/tasks/{id}` | ✅ Working |
| Projects | `/api/projects`, `/api/projects/{id}` | ✅ Working |
| Agent | `/api/agent/run`, `/api/agent/stop/{id}`, `/api/agent/runs` | ✅ Working |
| Schema | `/api/schema/task`, `/api/schema/project`, `/api/schema/agent-run`, `/api/schema/enums` | ✅ Working |
| Settings | `/api/settings/schema` | ✅ Working |
| Events | `/api/events` (SSE) | ⚪ Not Tested |

---

## Dokumentation

- `ARCHITECTURE.md` - System-Architektur + Backend/Frontend Aufteilung
- `dev/HANDOVER.md` - Session Handover
- `dev/ISSUE_TRACKER.md` - Bug Tracking + Feature Status
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme & Lösungen
- `dev/WORKFLOW.md` - Development Workflow

---

*Updated: 2026-01-22*
