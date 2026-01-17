# MCP Architecture: Kanban Orchestrator

## 1. Vision & Ziele

### Kernproblem

Die AI-Tool-Landschaft ändert sich rasant: Neue Models, neue APIs, neue MCPs.
Ein System, das direkt an diese Tools gekoppelt ist, muss ständig angepasst werden.

### Lösung: Stabile Orchestration Layer

Das Kanban-Board ist eine **stabile Orchestrierungsschicht**, die:
- Tasks verwaltet (CRUD)
- Agents koordiniert (Claude Agent SDK)
- Externe MCPs nutzt (nicht selbst implementiert)
- Als MCP-Server exponiert ist (für Claude Code)

### Schlüsselprinzip

```
Kanban = Orchestration (stabil)
MCPs = Features (austauschbar)
```

---

## 2. Key Insights

### 2.1 Bidirektionale MCP-Integration

Das System arbeitet in BEIDE Richtungen:

**A) Kanban NUTZT MCPs (Agent SDK → externe Tools)**
- Orchestrator ruft Perplexity, OpenAlex, Filesystem etc.
- Konfiguration via registry.py
- Tools sind austauschbar ohne Code-Änderung

**B) Kanban IST ein MCP (Claude Code → Kanban)**
- Claude Code kann Tasks erstellen: "Recherche zu XY"
- Tasks werden automatisch bearbeitet
- Ergebnisse fließen zurück

### 2.2 Entkopplung durch MCP-Protokoll

```
┌──────────────┐     MCP      ┌──────────────┐     MCP      ┌──────────────┐
│ Claude Code  │◄────────────►│   Kanban     │◄────────────►│  Perplexity  │
│   (Client)   │              │(Server+Client)│             │   (Server)   │
└──────────────┘              └──────────────┘              └──────────────┘
```

Jede Komponente kann unabhängig aktualisiert werden.

### 2.3 Plugin statt Implementation

**Falsch:** Perplexity-Integration selbst implementieren
**Richtig:** Existierenden MCP-Server aus Registry installieren

Vorteile:
- Weniger Code zu maintainen
- Community-Updates automatisch
- Standardisierte Schnittstellen

### 2.4 Modulare Backend-Architektur

Klare Trennung: `routes → services → agents → mcp`
- Routes: HTTP-Endpoints
- Services: Business Logic
- Agents: Orchestrierung
- MCP: Tool-Integration

---

## 3. Architekturentscheidungen

### Decision 1: Claude Agent SDK als Orchestrator

**Kontext:** Wie führt das System Tasks aus?
**Entscheidung:** Claude Agent SDK mit bypassPermissions
**Begründung:**
- Nutzt Max-Abo (keine API-Kosten)
- Subprocess-basiert (isoliert)
- MCP-Support eingebaut

### Decision 2: Externe MCPs statt eigene Implementation

**Kontext:** Wie integrieren wir Recherche-Tools?
**Entscheidung:** MCP-Server aus Glama/Smithery Registry
**Begründung:**
- Weniger Code
- Community-maintained
- Standardisiert

### Decision 3: Kanban als MCP Server (FastMCP)

**Kontext:** Wie kommuniziert Claude Code mit Kanban?
**Entscheidung:** FastMCP-Server der FastAPI-Backend aufruft
**Begründung:**
- Wenige Zeilen Code (~50)
- Nutzt bestehende API
- Kein Duplizieren von Logic

### Decision 4: Plugin Manager mit Glama API

**Kontext:** Wie installiert der User neue MCPs?
**Entscheidung:** UI mit Glama-API-Suche, Config in SQLite
**Begründung:**
- 15,833+ Server verfügbar
- Standardisiertes Schema
- Plug & Play

---

## 4. Workflows

### Workflow 1: UI → Agent → Review → Done

```
Kanban UI                    Backend                     MCPs
    │                           │                          │
    ├─► Create Task ──────────► │                          │
    │                           │                          │
    ├─► Click "Run" ──────────► │                          │
    │                           │                          │
    │   ◄── SSE: IN_PROGRESS ── │                          │
    │                           ├─► Orchestrator ─────────►│
    │   ◄── SSE: agent_log ──── │   (Claude Agent SDK)     │
    │                           │         │                │
    │                           │         ├─► Perplexity   │
    │                           │         ├─► Filesystem   │
    │                           │         └─► ...          │
    │   ◄── SSE: NEEDS_REVIEW ─ │                          │
    │                           │                          │
    ├─► Approve ──────────────► │                          │
    │                           │                          │
    │   ◄── SSE: DONE ───────── │                          │
```

### Workflow 2: Claude Code → Kanban → Agent → Ergebnis

```
Claude Code                 Kanban MCP Server           Backend
    │                           │                          │
    ├─► "Recherche XY" ────────►│                          │
    │                           │                          │
    │   create_task(            │                          │
    │     title="Recherche XY", ├─► POST /api/tasks ──────►│
    │     auto_run=true         │                          │
    │   )                       │   ◄── task_id ────────── │
    │                           │                          │
    │   ◄── {task_id, status} ──│                          │
    │                           │                          │
    │   ... wartet ...          │   ... Agent arbeitet ... │
    │                           │                          │
    ├─► get_task_result(id) ───►│                          │
    │                           ├─► GET /api/tasks/{id} ──►│
    │                           │   ◄── task + result ──── │
    │   ◄── Recherche-Ergebnis ─│                          │
```

---

## 5. Modulare Backend-Struktur

### Aktueller Stand (Phase 7.3 ✅)

```
backend/src/
├── api/
│   ├── routes/
│   │   ├── tasks.py          # Task CRUD
│   │   ├── projects.py       # Project CRUD
│   │   ├── agent.py          # Agent runs
│   │   ├── events.py         # SSE
│   │   └── schema.py         # Schema-Endpoints ✅ NEU
│   ├── schemas.py            # Pydantic (inkl. FieldType, SchemaField, EntitySchema)
│   ├── task_service.py       # Task Business Logic
│   └── project_service.py    # Project Business Logic
│
├── services/
│   └── git.py                # Git checkpoint/commit operations
│
├── agents/
│   └── orchestrator.py       # Claude Agent SDK (~200 Zeilen)
│
├── mcp_servers/              # Kanban als MCP Server
│   └── server.py             # FastMCP
│
├── mcp_client/               # MCP Client Config
│   └── registry.py           # Config für externe MCPs
│
├── models/
│   ├── task.py
│   ├── project.py
│   └── agent_run.py
│
└── database.py
```

### Schema-API (Phase 7.3)

Die Schema-Endpoints ermöglichen dynamisches Frontend-Rendering:

```
GET /api/schema/task         → Field-Definitionen für Task-Formulare
GET /api/schema/project      → Field-Definitionen für Project-Formulare
GET /api/schema/agent-run    → Field-Definitionen für AgentRun-Anzeige
GET /api/schema/enums        → Alle Enum-Werte (task_status, task_type, agent_run_status)
```

### Geplante Erweiterungen (Phase 8-9)

```
backend/src/
├── api/routes/
│   └── plugins.py            # Plugin Manager API (Phase 9)
│
├── services/
│   └── plugin_service.py     # Install/Uninstall (Phase 9)
│
├── mcp_client/
│   └── discovery.py          # Glama/Smithery API (Phase 9)
│
└── models/
    └── plugin.py             # Installierte Plugins (Phase 9)
```

---

## 6. MCP-Server Kategorien

| Kategorie | Server | Zweck |
|-----------|--------|-------|
| **Recherche** | Perplexity | Web Search mit AI-Summary |
|             | OpenAlex | Academic Paper Search |
|             | Crossref | DOI/Citation Lookup |
|             | Wikipedia | Encyclopedia |
| **Knowledge** | Joplin | Personal Notes |
|              | Custom DBs | Thematische Spezialisierung |
| **Coding** | Context7 | Library Docs |
|           | GitHub | Repository Operations |
| **Filesystem** | MCP Filesystem | Local Files |

---

## 7. Plugin Manager Konzept

### Datenmodell

```python
class Plugin(Base):
    id: str              # "perplexity"
    name: str            # "Perplexity Search"
    source: str          # "glama" | "smithery" | "local"
    source_id: str       # ID im Registry
    command: str         # "uvx mcp-perplexity"
    env_schema: JSON     # Required env vars
    env_values: JSON     # User's API keys (encrypted)
    enabled: bool
    installed_at: datetime
```

### UI Flow

```
Plugin Manager Tab
    │
    ├─► Search (Glama API)
    │       └─► Results: [Perplexity, OpenAlex, ...]
    │
    ├─► Click "Install"
    │       └─► Modal: Enter API Key
    │           └─► Save to DB
    │
    └─► Installed Plugins List
            ├─► Toggle Enable/Disable
            └─► Configure (API Keys)
```

---

## 8. Quellen

- [Glama MCP Registry](https://glama.ai/mcp/servers) - 15,833+ Server
- [Smithery](https://smithery.ai/) - CLI Installation
- [FastMCP Docs](https://gofastmcp.com/)
- [Claude Agent SDK MCP](https://platform.claude.com/docs/en/agent-sdk/mcp)
- [VibeKanban Extension Points](https://github.com/dweigend/vibe-kanban)

---

*Updated: 2026-01-17*
