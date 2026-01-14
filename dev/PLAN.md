# PLAN: Kanban Orchestrator

## Vision

AI-gestützter Workflow-Orchestrator mit Kanban-Board UI für automatisierte Recherche, Programmierung und Prototyping.

---

## Abgeschlossene Phasen

### Phase 1-3: Infrastructure ✅
- Backend: FastAPI + SQLAlchemy + SSE
- Frontend: SvelteKit + bits-ui + Tailwind
- Task CRUD mit Live-Updates

### Phase 4.1: Agent MVP ✅
- Claude Agent SDK Integration
- Project/AgentRun Models
- MCP Registry + Filesystem Server
- Git Auto-Checkpoints
- SSE Agent Log Streaming

### Phase 5: Frontend UI ✅
- Kanban Board mit Drag & Drop
- Sidebar-First Architecture
- Task Editor in Sidebar
- Toast Notifications

---

## Aktuelle Phase: 4.2 - Agent UI Integration

### Sofort (UI Wiring)
- [ ] Run Button auf TaskCard
- [ ] AgentLog Tab in Sidebar
- [ ] NEEDS_REVIEW Spalte
- [ ] Spinner während Agent läuft

### Danach (Multi-Project)
- [ ] Project Selector im Header
- [ ] Tasks nach Project filtern
- [ ] Default Project erstellen

### Später (MCP Erweiterung)
- [ ] Perplexity MCP Server
- [ ] Workflow Templates Model + UI
- [ ] Human-in-the-Loop Flow

---

## Phase 6: Polish (Future)

- [ ] Plugin-System
- [ ] Error Handling & Logging
- [ ] Performance Optimization
- [x] ARCHITECTURE.md Dokumentation ✅

---

## Backlog

- Vite Proxy für Production CORS
- OpenAlex/BibTeX MCP Server
- Google ADK für komplexe Workflows

---

*Updated: 2026-01-14*
