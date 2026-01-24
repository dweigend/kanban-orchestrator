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
- **Phase 7.3 Session B:** Frontend Schema-Integration (TaskEditor)
- **Phase 8:** Schema-Driven UI (77 Tests)
- **Phase 9:** Bug Fixes + UI Cleanup (12 Issues fixed)

---

## Aktuelle Phase: Stabilisierung 🟢

**Status:** 12 von 16 Issues erledigt (Stand 2026-01-23)

Siehe `dev/ISSUE_TRACKER.md` für vollständige Liste.

### ✅ Erledigt (12 Issues)

| Issue | Beschreibung |
|-------|--------------|
| #1 | Settings persistent (localStorage) |
| #4, #23 | Search entfernt (Konzept unklar) |
| #6 | Tasks im Board anzeigen |
| #7 | Plus-Buttons funktional |
| #8 | Agent Logs anzeigen |
| #15 | Settings Freeze (untrack() fix) |
| #17 | Card-Menü → Icons |
| #18-21 | UI Cleanup (Quick Wins) |

### 🔧 Offen (4 Issues)

| Prio | # | Issue | Severity |
|------|---|-------|----------|
| 1 | #14 | Card Reorder in Columns | MEDIUM |
| 2 | #22 | Projekt-Management (Konzept) | HIGH |
| 3 | #3 | Backend Settings in UI | LOW |
| 4 | #16 | Agent-Autostart (UX) | LOW |

---

## Nächste Phasen

### Phase 10: Card Reorder (#14)

- `position`/`order` Feld im Task-Model
- Drag & Drop innerhalb Spalte
- Backend: PATCH für position update

### Phase 11: Projekt-Management (#22)

- Backend-Recherche: Wie werden Projekte gespeichert?
- Konzept-Entwicklung mit User
- Projekt-Menü funktionsfähig machen

### Phase 12: Plugin Manager

- MCP Registry Integration (Glama API)
- Plugin Install/Configure UI

### Phase 13: Advanced Features

- NEEDS_REVIEW Flow
- Knowledge DBs Integration
- Multi-Project Support

---

## Backlog

- Task Dependencies
- Bulk Operations
- Export/Import
- Keyboard Shortcuts
- Mobile Responsive
- Backend Settings in UI (#3)
- Agent-Autostart Option (#16)

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

*Updated: 2026-01-23*
