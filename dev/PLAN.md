# PLAN: Kanban Orchestrator

## Vision

AI-gestützter Workflow-Orchestrator mit Kanban-Board UI für automatisierte Recherche, Programmierung und Prototyping.

---

## Phases

### Phase 0: Setup ✅
- [x] Projekt-Struktur analysieren
- [x] Architektur-Entscheidungen treffen
- [x] `.claude/` Setup generieren
- [x] `dev/` Workflow-Docs generieren

### Phase 1: Basis-Infrastruktur ✅
- [x] Frontend: ESLint → Biome Migration
- [x] Frontend: bits-ui installieren
- [x] Backend: Modulare Ordnerstruktur (`src/agents/`, `src/api/`, etc.)
- [x] Backend: FastAPI + Pydantic hinzufügen
- [x] Root: Makefile für `make dev`

### Phase 2: Konzept & Plan
- [ ] Mockups-Ordner erstellen (`docs/mockups/`)
- [ ] Agent-Architektur dokumentieren
- [ ] API-Kontrakt definieren (OpenAPI Spec)
- [ ] Datenmodell: Task, Workflow, Agent-Run
- [ ] Plugin-System Konzept

### Phase 3: Backend Core ✅
- [x] FastAPI App Setup mit CORS
- [x] SQLite + SQLAlchemy Models (async)
- [x] Task CRUD Endpoints
- [x] SSE für Live-Updates (EventBus)

### Phase 4: Agent Integration
- [ ] Orchestrator Agent (Claude SDK)
- [ ] Researcher Agent (Perplexity Integration)
- [ ] MCP Tools: OpenAlex, BibTeX
- [ ] Google ADK für komplexe Workflows

### Phase 5: Frontend Core
- [ ] Kanban-Board Layout
- [ ] Task-Cards mit Drag & Drop
- [ ] Workflow-Orchestrator Panel
- [ ] Agent-Status Live-View (SSE)

### Phase 6: Polish & Plugins
- [ ] Plugin-System Implementation
- [ ] Error Handling & Logging
- [ ] Performance Optimization
- [ ] Documentation

---

## Current Focus

**Phase:** 4 oder 5 (Agent Integration oder Frontend)
**Next Task:** User-Entscheidung - Backend Agents oder Frontend UI?

---

## Backlog

*Probleme und Ideas für spätere Sessions:*

- (noch leer)

---

*Updated: 2026-01-13 (Phase 3 complete)*
