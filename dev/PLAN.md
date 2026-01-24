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
- **Phase 9:** Bug Fixes + UI Cleanup (13 Issues closed)

---

## Nächste Phasen

### Phase 10: Subtasks & Expand/Collapse Cards (#24)

**Ziel:** Komplexe Tasks in Untertasks zerlegen

**Features:**
- Expand/Collapse Cards im Board
- Subtasks als Checklist innerhalb einer Card
- Agent zerlegt komplexe Tasks automatisch (Claude SDK Planungsmodus)
- Nur für komplexe Tasks (einfache bleiben flat)

**Implementation:**
| Komponente | Änderung |
|------------|----------|
| Task-Model | `subtasks: [{text: string, done: boolean}]` (JSON-Array) |
| TaskCard.svelte | Expandable mit Chevron |
| Agent | Planungsmodus für Task-Zerlegung |

**Kein Backend-Bloat:** Subtasks als JSON-Feld, keine separate Tabelle.

---

### Phase 11: Konzept-Session - Projektstruktur & Erweiterte Tasks

**Ziel:** Grundlagen für erweiterte Task-Konfiguration schaffen

⚠️ **KONZEPT-SESSION** - Nur Planung, keine Implementation

#### Part A: Projektstruktur & Standardpfade (#26)

**Fragen zu klären:**
1. Wo liegt das Projekt-Root?
2. Welche Standardordner gibt es? (src, docs, tests, etc.)
3. Wie werden MCP-Server pro Projekt konfiguriert?
4. Wie greift Frontend auf diese Infos zu?

**Mögliche Struktur:**
```
project/
├── .kanban/           # Orchestrator-Konfiguration
│   ├── config.yaml    # Projekt-Settings
│   ├── mcps.yaml      # Verfügbare MCPs
│   └── paths.yaml     # Standardpfade
├── src/
├── docs/
└── ...
```

#### Part B: Erweiterte Task-Definition (#25)

**Neue Felder (nach Konzept):**
| Feld | Beschreibung |
|------|--------------|
| `mcps` | MCP-Server, die der Agent nutzen darf |
| `files` | Dateien/Ordner mit Zugriff |
| `permissions` | Berechtigungen (read/write/execute) |
| `output_dict` | Erwartetes Output-Format |

**Abhängigkeit:** Braucht #26 (Projektstruktur) zuerst

#### Part C: Projekt-Management (#22)

- Backend `/api/projects` mit echten Daten füllen
- Projekt-Menü funktionsfähig machen
- Multi-Projekt Support?

---

### Phase 12: Implementation Erweiterte Tasks

**Nach Konzept-Session:**
- Backend: Task-Model erweitern
- Frontend: TaskEditor erweitern
- Schema-Endpoints aktualisieren

---

### Phase 13: Plugin Manager

- MCP Registry Integration (Glama API)
- Plugin Install/Configure UI
- Pro-Projekt MCP-Konfiguration

---

### Phase 14: Advanced Features

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

## Aktuelle Issues

| Prio | # | Issue | Phase |
|------|---|-------|-------|
| 1 | #24 | Subtasks + Expand Cards | 10 |
| 2 | #26 | Projektstruktur & Standardpfade | 11 (Konzept) |
| 3 | #25 | Erweiterte Task-Definition | 11 (Konzept) |
| 4 | #22 | Projekt-Management | 11 (Konzept) |
| 5 | #3, #16 | Settings, Autostart | Backlog |

**Abhängigkeiten:**
```
#26 (Projektstruktur) → #25 (Erweiterte Tasks)
#22 (Projekt-Management) → #9 (Projekt-Menü)
```

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

---

## Dokumentation

- `ARCHITECTURE.md` - System-Architektur + Backend/Frontend Aufteilung
- `dev/HANDOVER.md` - Session Handover
- `dev/ISSUE_TRACKER.md` - Bug Tracking + Feature Status
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme & Lösungen
- `dev/WORKFLOW.md` - Development Workflow

---

*Updated: 2026-01-24*
