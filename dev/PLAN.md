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
- **Phase 11C:** MCP Registry (YAML-Config, Environment-Auflösung) ✅
- **Phase 11.5A:** OpenAlex MCP Integration ✅

---

## Aktuelle Phase

### Phase 11.5B: Trilium MCP Integration 🔲 NEXT

**Ziel:** Trilium Notes als Knowledge-Speicher für Orchestrator-Output

| Task | Beschreibung |
|------|--------------|
| 1 | Trilium Server auf Server einrichten |
| 2 | ETAPI Token generieren |
| 3 | Trilium MCP in `mcps.yaml` hinzufügen |
| 4 | E2E Test: Research → Trilium |

**Voraussetzung:** Trilium Server läuft und ETAPI ist aktiviert.

---

### Phase 11.5C: Templates 🔲

**Ziel:** Markdown-Templates für strukturierten Agent-Output

**Design:** Siehe `dev/DESIGN-TASK-DELEGATION.md`

---

## Nächste Phasen

### Phase 11D: Templates (ehemals 11.5C)

**Ziel:** Markdown-Templates für Agent-Output-Struktur

| Task | Beschreibung |
|------|--------------|
| 1 | `backend/templates/` Ordner erstellen |
| 2 | Templates: `quick.md`, `deep.md`, `paper.md`, `idea.md` |
| 3 | Template-Loader in `backend/src/agents/templates.py` |
| 4 | Template-Injection in Agent-Prompt |

**Templates:**
- `quick.md` - Schnelle Recherche (TL;DR + Key Points)
- `deep.md` - Umfassende Recherche (Summary, Findings, Sources)
- `paper.md` - Wissenschaftliche Paper-Analyse (Abstract, Methods, Results)
- `idea.md` - Ideen-Exploration (Problem, Related Concepts, Next Steps)

**Dateien:**
- `backend/templates/*.md` (NEU)
- `backend/src/agents/templates.py` (NEU)

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

### Phase 12: Zotero Integration

**Ziel:** Bibliography-Management für wissenschaftliche Recherche

| Task | Beschreibung |
|------|--------------|
| 1 | Zotero + Better BibTeX Plugin installieren |
| 2 | Zotero MCP konfigurieren (`54yyyu/zotero-mcp`) |
| 3 | `mcps.yaml` erweitern |
| 4 | BibTeX-Export in Templates integrieren |

**Features:**
- Semantic Vector Search
- BibTeX Export
- PDF Annotations
- Full-Text Access

---

### Phase 13: Plugin Manager (Optional)

- MCP Registry UI (statt nur YAML)
- Plugin Install/Configure UI
- Glama API Integration

---

### Phase 14: Agent Skills / Workflows (Backlog)

**Ziel:** Vordefinierte Workflows für häufige Tasks

| Workflow | MCPs | Beschreibung |
|----------|------|--------------|
| `topic-research` | perplexity, openalex, trilium | Web + Paper Recherche → Strukturierte Note |
| `literature-review` | openalex, trilium | Paper-Suche → User-Auswahl → Synthese + BibTeX |
| `prototype` | filesystem, github | Code schreiben → Git Commit → Docs |
| `content-pipeline` | perplexity, trilium, filesystem | Research → Draft → Review → Export |

**Sandbox-Konzept:** Jeder Task schreibt Zwischenergebnisse in `output/{task_id}/`

---

### Phase 15: Advanced Features (Backlog)

- NEEDS_REVIEW Flow verbessern (2-Step Workflows)
- Automatische Ablage (Monitoring → Trilium Inbox)
- Task Dependencies
- Bulk Operations
- Chaos → Ordnung Pipeline (lokale Dateien → richtige Ablage)
- Audio-Transkription → Reports

---

## Issues

**→ Alle Issues auf GitHub:** https://github.com/dweigend/kanban-orchestrator/issues

### Phase 11.5: Cleanup & Stabilisierung (Zwischenphase)

| Prio | # | Issue | Status |
|------|---|-------|--------|
| 1 | #9 | 🔴 Agent Log Panel Bug | 🔲 Open |
| 2 | #17 | 🔧 SettingsPanel.svelte aufteilen | 🔲 Open |
| 3 | #13 | 🔧 orchestrator.py aufteilen | 🔲 Open |
| 4 | #2 | 🛡️ Error Handling kanban_server | 🔲 Open |

### Offene Feature-Issues

| # | Issue | Phase |
|---|-------|-------|
| #8 | 🔴 Projekt-Management konzeptionieren | Backlog (12+) |
| #10 | 🟡 Task-Summary im Board | 11D |
| #11 | 🔵 Klickbare Pfade + Default Editor | 11F |
| #12 | 🔵 Overview Tab ohne Funktion | 11F |

### Offene Refactoring-Issues

| # | Issue | Phase |
|---|-------|-------|
| #14 | 🔧 Services Layer konsolidieren | Backlog |
| #15 | 🔧 MCP Server HTTP-Client vereinheitlichen | Backlog |
| #16 | 🔧 Event-Serialisierung zentralisieren | Backlog |
| #18 | 🔧 +page.svelte State extrahieren | 11F |
| #19 | 🔧 Header.svelte Button-Komponente | 11F |
| #20 | 🔧 AgentLog.svelte aufteilen | 11F |
| #21 | 🔧 TaskEditor Sections extrahieren | 11F |

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
- `dev/DESIGN-MCP-WORKFLOWS.md` - MCP Discovery + Workflow Konzept (NEU)
- `dev/HANDOVER.md` - Session Handover
- `dev/TROUBLESHOOTING.md` - Bekannte Probleme & Lösungen
- `dev/WORKFLOW.md` - Development Workflow
- **GitHub Issues** - https://github.com/dweigend/kanban-orchestrator/issues

---

## MCP Inventory

| MCP | Status | Use Case |
|-----|--------|----------|
| `filesystem` | ✅ Aktiv | Sandboxed File I/O |
| `github_simple` | ✅ Aktiv | GitHub Read-Only |
| `perplexity` | ✅ Aktiv | Web Search |
| `openalex` | ✅ Aktiv | Academic Paper Search |
| `trilium` | 🔜 Phase 11.5B | Notes speichern |
| `zotero` | 📅 Phase 12 | Bibliography, PDFs |

---

*Updated: 2026-01-25*
