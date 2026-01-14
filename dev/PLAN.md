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
- [x] Mockups-Ordner erstellen (`dev/ui/`)
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

### Phase 5: Frontend Core ✅
- [x] Kanban-Board Layout
- [x] Task-Cards mit DropdownMenu
- [x] Function Panel (Sidebar)
- [x] Settings Panel
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

### Phase 5.7: API Integration ✅
- [x] Task CRUD mit Backend verbinden
- [x] SSE für Live-Updates
- [x] Form Validation (TaskEditor)
- [ ] TaskCard Click → Edit in Sidebar
- [ ] Drag & Drop für Task-Verschiebung

### Phase 5.8: UI Completion ✅
- [x] TaskCard Click → öffnet Editor
- [x] TaskCard Dropdown → Edit/Delete funktional
- [x] Drag & Drop zwischen Spalten
- [x] Toast Notifications (svelte-sonner)

### Phase 6: Polish & Plugins
- [ ] Plugin-System Implementation
- [ ] Error Handling & Logging
- [ ] Performance Optimization
- [ ] Documentation

---

## Current Focus

**Phase:** 6 (Polish & Plugins)
**Next Task:** Plugin-System Implementation oder Agent Integration

---

## Backlog

- Backend: `type`, `description` Felder zu Task Model hinzufügen
- Vite Proxy für Production CORS Setup

---

*Updated: 2026-01-14 (Phase 5.7 API Integration completed)*
