# HANDOVER

## Session: 2026-01-16 - Architecture Planning ✅

### Was wurde gemacht

**Architektur-Planung & Dokumentation:**

1. **Neue Architektur definiert** → `dev/MCP-ARCHITECTURE.md`
   - Bidirektionale MCP-Integration
   - Kanban als stabile Orchestration Layer
   - Plugin Manager Konzept

2. **Key Decisions dokumentiert:**
   - Decision 1: Claude Agent SDK als Orchestrator
   - Decision 2: Externe MCPs statt eigene Implementation
   - Decision 3: Kanban als MCP Server (FastMCP)
   - Decision 4: Plugin Manager mit Glama API

3. **Dokumentation aufgeräumt:**
   - PLAN.md mit Phasen 5-8
   - FRONTEND-PLAN.md gelöscht (redundant)
   - ARCHITECTURE.md erweitert

### Architektur-Übersicht

```
┌──────────────┐     MCP      ┌──────────────┐     MCP      ┌──────────────┐
│ Claude Code  │◄────────────►│   Kanban     │◄────────────►│  Perplexity  │
│   (Client)   │              │(Server+Client)│             │   (Server)   │
└──────────────┘              └──────────────┘              └──────────────┘
```

**Prinzip:** Kanban = Orchestration (stabil), MCPs = Features (austauschbar)

---

## Nächste Session: Phase 5 - Modulares Backend

### Priority 1: Refactoring

```
backend/src/
├── mcp/                      # Umbenennen von mcp_servers/
│   ├── registry.py           # existiert
│   ├── kanban_server.py      # Phase 6
│   └── discovery.py          # Phase 7
├── services/
│   └── agent_service.py      # aus orchestrator.py
├── agents/
│   ├── orchestrator.py       # Slim down
│   └── prompts.py            # Templates
└── models/
    └── plugin.py             # Phase 7
```

### Priority 2: Cleanup

- [ ] `backend/src/plugins/` löschen (leer)
- [ ] `backend/src/tools/` löschen (leer)
- [ ] Mock-Daten aus Frontend entfernen

### Detaillierter Implementierungsplan

**Schritt 1: Ordner umbenennen**
```bash
cd backend/src
mv mcp_servers mcp
# Imports in orchestrator.py anpassen
```

**Schritt 2: agent_service.py extrahieren**
- Git-Operationen aus orchestrator.py → `services/git_service.py`
- Agent-Run-Management → `services/agent_service.py`
- orchestrator.py auf < 100 Zeilen reduzieren

**Schritt 3: prompts.py erstellen**
- `_build_prompt()` aus orchestrator.py → `agents/prompts.py`
- Prompt-Templates für verschiedene Task-Typen

**Schritt 4: Cleanup**
- Leere Ordner löschen
- Imports prüfen
- Type checks laufen lassen

---

## Verification Commands

```bash
# Backend
cd backend && uvx ty check
uv run ruff check --fix . && uv run ruff format .

# Frontend
cd frontend && bunx svelte-check --threshold warning
bunx biome check --write .
```

---

## Referenzen

- **Architektur-Details:** `dev/MCP-ARCHITECTURE.md`
- **Phasen-Übersicht:** `dev/PLAN.md`
- **Workflow-Dokumentation:** `dev/WORKFLOW.md`

---

*Updated: 2026-01-16*
