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

### Phase 5: Frontend Core (in progress)
- [x] Kanban-Board Layout
- [x] Task-Cards mit DropdownMenu
- [x] Function Panel (Sidebar)
- [x] Settings Dialog (wird refactored)
- [ ] Drag & Drop für Task-Verschiebung
- [ ] Agent-Status Live-View (SSE)

### Phase 5.5: Sidebar Refactor ✅
- [x] **Design-Regel:** Sidebar-First Architecture
- [x] Settings Dialog → Sidebar Panel refactoren
- [x] Task CRUD in Sidebar integrieren (TaskEditor)
- [x] Function Panel mit Tabs redesignen

### Phase 5.6: UX Refactor ✅
- [x] Einheitliche Menüstruktur (alles im Header)
- [x] Sidebar-Tabs als Icon-Buttons im Header
- [x] Sidebar nur Inhalt, keine eigene Navigation
- [x] Resizable Sidebar
- [x] Controlled Component Pattern

### Phase 5.7: API Integration (next)
- [ ] Task CRUD mit Backend verbinden
- [ ] SSE für Live-Updates
- [ ] TaskCard Click → Edit in Sidebar
- [ ] Drag & Drop für Task-Verschiebung

### Phase 6: Polish & Plugins
- [ ] Plugin-System Implementation
- [ ] Error Handling & Logging
- [ ] Performance Optimization
- [ ] Documentation

---

## Current Focus

**Phase:** 5.7 (API Integration)
**Next Task:** Task CRUD mit Backend verbinden

---

## Backlog

- `TaskEditor.svelte:65-77` → `validateForm()` implementieren

---

*Updated: 2026-01-13 (Phase 5.6 UX Refactor completed)*
