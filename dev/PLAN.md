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

## Aktuelle Phase: Bug Fixes + UI Cleanup 🔴

**Status:** 23 Issues dokumentiert (Stand 2026-01-22)

Siehe `dev/ISSUE_TRACKER.md` für vollständige Liste.

### ✅ Erledigt

| Issue | Beschreibung |
|-------|--------------|
| #1 | Settings persistent (localStorage) |
| #6 | Tasks im Board anzeigen |
| #7 | Plus-Buttons funktional |
| #8 | Agent Logs anzeigen |

### 🚀 Quick Wins (UI verschlanken)

| Issue | Beschreibung | Action |
|-------|--------------|--------|
| #18 | Hub/Board View Toggle | Entfernen |
| #19 | Breadcrumb "vibe-kanban/hub-view" | Entfernen |
| #20 | Project Overview Section | Entfernen |
| #21 | System Logs Section | Entfernen |

### 🔧 Bugs

| Issue | Beschreibung | Severity |
|-------|--------------|----------|
| #15 | Editor Config Freeze | HIGH |
| #14 | Card Reorder in Columns | MEDIUM |

### 🎨 UX Verbesserungen

| Issue | Beschreibung |
|-------|--------------|
| #17 | Card-Menü → Icons (Run Agent, Delete) |
| #16 | Agent-Autostart bei Task-Erstellung |

### 📋 Eigene Sessions (Konzeptarbeit)

| Issue | Beschreibung | Notes |
|-------|--------------|-------|
| #22 | Projekt-Management | Backend-Recherche + Konzept mit User |
| #23 | Search / Knowledge Base | Konzept-Abgleich mit Original |
| #9 | Projekt-Menü | Abhängig von #22 |
| #4 | Search | Abhängig von #23 |

### 🧹 Cleanup (niedrige Prio)

| Issue | Beschreibung |
|-------|--------------|
| #3 | Backend Settings in UI |
| #5 | Mock Data System Log |
| #10 | View Toggle (entfernt durch #18) |
| #11 | "View All" Button |
| #12 | User Avatar |
| #13 | Overview Mock Data |

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
- `dev/ISSUE_TRACKER.md` - Bug Tracking + Feature Status (23 Issues)
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme & Lösungen
- `dev/WORKFLOW.md` - Development Workflow

---

*Updated: 2026-01-22*
