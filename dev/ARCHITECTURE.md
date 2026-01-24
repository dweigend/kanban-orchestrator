# Architecture: Kanban Orchestrator

## System Overview

AI-gestützter Workflow-Orchestrator mit Kanban-Board UI für automatisierte Recherche, Programmierung und Prototyping.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (SvelteKit 5)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Kanban Board│  │   Header    │  │     FunctionPanel       │  │
│  │  + Columns  │  │  + Tabs     │  │  Overview | Agents |    │  │
│  │  + Cards    │  │  + Toggle   │  │  Logs | Editor | Settings│ │
│  └──────┬──────┘  └─────────────┘  └────────────┬────────────┘  │
│         │                                       │               │
│         └───────────────┬───────────────────────┘               │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Services (API, Events, Tasks, Agent, Schema)   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP + SSE
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    API Routes Layer                       │   │
│  │  /api/projects  /api/tasks  /api/agent/*  /api/events    │   │
│  │  /api/schema/*  /api/settings                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌────────────┐    ┌─────────────────┐    ┌──────────────┐      │
│  │  Services  │    │   Orchestrator  │    │   EventBus   │      │
│  │ task/proj  │    │ Claude SDK Agent│    │  SSE Pub/Sub │      │
│  └─────┬──────┘    └────────┬────────┘    └──────────────┘      │
│        │                    │                                   │
│        ▼                    ▼                                   │
│  ┌────────────┐    ┌─────────────────┐                          │
│  │  Database  │    │   MCP Servers   │                          │
│  │  SQLite    │    │   Filesystem    │                          │
│  └────────────┘    └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | SvelteKit 5 | UI Framework mit Runes |
| | bits-ui | Accessible Components |
| | Tailwind CSS 4 | Styling |
| | TypeScript | Type Safety |
| **Backend** | FastAPI | Async REST API |
| | SQLAlchemy 2.0 | Async ORM |
| | SQLite + aiosqlite | Database |
| | Claude Agent SDK | AI Agent Execution |
| **Communication** | REST API | CRUD Operations |
| | SSE | Real-time Events |
| **Tools** | uv | Python Package Manager |
| | Bun | JS Runtime + Package Manager |
| | Ruff | Python Linting |
| | Biome | TS/JS Linting |

---

## Backend Architecture

### Directory Structure

```
backend/
├── main.py                    # FastAPI Entry Point
├── pyproject.toml             # Dependencies
├── kanban.db                  # SQLite Database
└── src/
    ├── database.py            # SQLAlchemy Setup
    ├── models/                # Database Models
    │   ├── __init__.py
    │   ├── task.py            # Task Model (with steps, parent_id)
    │   ├── project.py         # Project Model
    │   └── agent_run.py       # AgentRun Model
    ├── api/
    │   ├── schemas.py         # Pydantic Schemas
    │   ├── events.py          # EventBus + SSE
    │   ├── task_service.py    # Task Business Logic
    │   ├── project_service.py # Project Business Logic
    │   └── routes/
    │       ├── projects.py    # /api/projects
    │       ├── tasks.py       # /api/tasks + /api/tasks/{id}/subtasks
    │       ├── agent.py       # /api/agent/* (run, stop, plan, execute)
    │       ├── events.py      # /api/events (SSE)
    │       ├── schema.py      # /api/schema/* (task, project, enums)
    │       └── settings.py    # /api/settings (backend config)
    ├── services/              # Shared Business Logic
    │   └── git.py             # Git checkpoint/commit operations
    ├── agents/
    │   └── orchestrator.py    # Claude Agent SDK Integration
    ├── mcp_servers/           # MCP servers WE EXPOSE (Kanban → external clients)
    │   ├── kanban_server.py   # Tools for Claude Code (create_task, list_tasks)
    │   └── filesystem/
    │       └── server.py      # File I/O Tools (sandboxed)
    └── mcp_client/            # MCP config for servers WE USE (Kanban → external MCPs)
        └── registry.py        # Registry of MCP servers the orchestrator can spawn
```

### Database Schema

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    projects     │     │      tasks      │     │   agent_runs    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │◄────┤ project_id (FK) │     │ id (PK)         │
│ name            │     │ id (PK)         │◄────┤ task_id (FK)    │
│ workspace_path  │     │ title           │     │ status          │
│ created_at      │     │ description     │     │ logs            │
└─────────────────┘     │ result          │     │ error_message   │
                        │ steps (JSON)    │     │ created_at      │
                        │ status          │     │ started_at      │
                        │ type            │     │ completed_at    │
                        │ parent_id (FK)──┼──┐  └─────────────────┘
                        │ created_at      │  │
                        └─────────────────┘  │
                                │            │
                                └────────────┘
                              (Self-Reference: Subtasks)
```

**Task Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | String(36) | UUID primary key |
| `title` | String(255) | Task title |
| `description` | Text | Optional description |
| `result` | Text | Agent execution result |
| `steps` | JSON | Array of `{text: string, done: boolean}` |
| `status` | String(20) | todo, in_progress, needs_review, done |
| `type` | String(20) | research, dev, notes, neutral |
| `parent_id` | String(36) | FK to parent task (subtasks) |
| `project_id` | String(36) | FK to project |
| `created_at` | DateTime | Creation timestamp |

**Status Enums:**

| Model | Status Values |
|-------|---------------|
| Task | `todo`, `in_progress`, `needs_review`, `done` |
| AgentRun | `pending`, `running`, `completed`, `failed`, `cancelled` |

### API Endpoints

#### Projects
```
POST   /api/projects              Create project
GET    /api/projects              List all projects
GET    /api/projects/{id}         Get project by ID
PUT    /api/projects/{id}         Update project
DELETE /api/projects/{id}         Delete project
```

#### Tasks
```
POST   /api/tasks                 Create task
GET    /api/tasks                 List all tasks
GET    /api/tasks/{id}            Get task by ID
PUT    /api/tasks/{id}            Update task
PUT    /api/tasks/{id}/steps      Update task steps
DELETE /api/tasks/{id}            Delete task
GET    /api/tasks/{id}/subtasks   Get subtasks of a parent task
```

#### Agent
```
POST   /api/agent/run             Start agent for task (202 Accepted)
POST   /api/agent/stop/{id}       Stop running agent
GET    /api/agent/runs            List agent runs (filter: task_id, status)
GET    /api/agent/runs/{id}       Get agent run details
POST   /api/agent/plan/{id}       Plan task decomposition (creates subtasks)
POST   /api/agent/execute/{id}    Execute subtasks of a planned task
```

#### Schema
```
GET    /api/schema/task           Task field schema for dynamic forms
GET    /api/schema/project        Project field schema
GET    /api/schema/agent-run      AgentRun field schema
GET    /api/schema/enums          All enum values with labels
```

#### Settings
```
GET    /api/settings              Read backend settings
POST   /api/settings              Save backend settings
GET    /api/settings/schema       Settings field schema
```

#### Events
```
GET    /api/events                SSE stream (text/event-stream)
```

### Event System (SSE)

```
┌──────────────┐     publish()    ┌──────────────┐     SSE Stream    ┌──────────────┐
│   Service    │ ───────────────► │   EventBus   │ ─────────────────► │   Frontend   │
│ (task_service│                  │              │                    │ (events.ts)  │
│  orchestrator│                  │ asyncio.Queue│                    │              │
└──────────────┘                  └──────────────┘                    └──────────────┘
```

**Event Types:**
- `task_created` - New task created
- `task_updated` - Task modified
- `task_deleted` - Task removed
- `agent_log` - Agent execution log entry
- `heartbeat` - Keep-alive (30s interval)

### Agent Orchestrator

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Execution Flow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Frontend: startAgentRun(taskId)                             │
│         │                                                       │
│         ▼                                                       │
│  2. Backend: POST /api/agent/run → 202 Accepted                 │
│         │                                                       │
│         ▼                                                       │
│  3. Background: _run_task_background()                          │
│         │                                                       │
│         ▼                                                       │
│  4. Git: Create checkpoint (📍 before task-{id})                │
│         │                                                       │
│         ▼                                                       │
│  5. Claude Agent SDK: query() with MCP tools                    │
│         │                                                       │
│         ├───► SSE: agent_log events (streaming)                 │
│         │                                                       │
│         ▼                                                       │
│  6. Success: Git commit (✨ {task.title}) + Task → DONE         │
│     Failure: Task → TODO + error_message                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### MCP Architecture

The system uses MCP (Model Context Protocol) bidirectionally:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP BIDIRECTIONAL FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DIRECTION A: Kanban USES MCPs (mcp_client/)                   │
│  ───────────────────────────────────────────                   │
│  Orchestrator → spawns MCP servers for agent tools             │
│                                                                 │
│  ┌──────────────┐      ┌─────────────────┐                     │
│  │ Orchestrator │ ───► │ Filesystem MCP  │                     │
│  │ (Claude SDK) │      │ Perplexity MCP  │ (future)            │
│  └──────────────┘      └─────────────────┘                     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DIRECTION B: Kanban IS an MCP (mcp_servers/)                  │
│  ────────────────────────────────────────────                  │
│  Claude Code → creates tasks in Kanban board                   │
│                                                                 │
│  ┌─────────────┐      ┌──────────────┐      ┌──────────┐       │
│  │ Claude Code │ ───► │ Kanban MCP   │ ───► │ REST API │       │
│  └─────────────┘      └──────────────┘      └──────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Frontend Architecture

### Directory Structure

```
frontend/
├── package.json
├── svelte.config.js
├── vite.config.ts
└── src/
    ├── app.html                # HTML Template
    ├── app.css                 # Global Styles
    ├── routes/
    │   ├── +layout.svelte      # Root Layout (loads settings)
    │   └── +page.svelte        # Main Page
    └── lib/
        ├── types/
        │   ├── task.ts         # Task interfaces + status mappings
        │   ├── agent.ts        # AgentRun interfaces
        │   └── schema.ts       # Schema field definitions
        ├── stores/
        │   ├── schema.svelte.ts   # Schema + Enums state
        │   └── settings.svelte.ts # Frontend + Backend settings
        ├── services/
        │   ├── api.ts          # Generic fetch wrapper
        │   ├── tasks.ts        # Task CRUD + steps update
        │   ├── agent.ts        # Agent execution
        │   ├── events.ts       # SSE subscription
        │   ├── schema.ts       # Schema fetching
        │   ├── settings.ts     # Backend settings API
        │   └── toast.ts        # Notifications
        └── components/
            ├── form/
            │   ├── FieldRenderer.svelte   # Schema-driven field rendering
            │   ├── FieldText.svelte       # Text input
            │   ├── FieldTextarea.svelte   # Textarea input
            │   ├── FieldSelect.svelte     # Select dropdown
            │   ├── FieldReadonly.svelte   # Read-only display
            │   ├── FieldDatetime.svelte   # Datetime display
            │   └── index.ts               # Barrel export
            ├── kanban/
            │   ├── Board.svelte       # Main board container
            │   ├── Column.svelte      # Status column
            │   ├── TaskCard.svelte    # Task card (expandable)
            │   └── SubtaskTree.svelte # Subtask tree display
            ├── layout/
            │   └── Header.svelte      # App header with tabs
            └── panel/
                ├── FunctionPanel.svelte   # Main sidebar container
                ├── ProjectOverview.svelte # Project info
                ├── AgentList.svelte       # Agent status list
                ├── AgentLog.svelte        # Agent execution logs
                ├── TaskEditor.svelte      # Task edit form
                └── SettingsPanel.svelte   # Settings (Frontend + Backend)
```

### Component Hierarchy

```
+page.svelte
├── Header.svelte
│   └── Tabs: overview | agents | settings
├── Board.svelte
│   └── Column.svelte (×4: TODO, IN_PROGRESS, NEEDS_REVIEW, DONE)
│       └── TaskCard.svelte (expandable for subtasks)
│           └── SubtaskTree.svelte (when expanded)
└── FunctionPanel.svelte
    └── Content (based on activeTab):
        ├── ProjectOverview.svelte
        ├── AgentList.svelte
        │   └── AgentLog.svelte
        ├── TaskEditor.svelte
        └── SettingsPanel.svelte
```

### State Management (Svelte 5 Runes)

```typescript
// +page.svelte
let sidebarVisible = $state(true);
let activeTab = $state<SidebarTab>('overview');
let editingTask = $state<Task | null>(null);
let tasks = $state<Task[]>([]);
let loading = $state(true);

// Derived state
let todoTasks = $derived(tasks.filter(t => t.status === 'TODO'));
let activeTasks = $derived(tasks.filter(t => t.status === 'IN_PROGRESS'));
```

### Type Definitions

**Task Types:**
```typescript
type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'NEEDS_REVIEW' | 'DONE';
type TaskType = 'research' | 'dev' | 'notes' | 'neutral';

interface Step {
  text: string;
  done: boolean;
}

interface Task {
  id: string;
  title: string;
  description?: string;
  result?: string;
  steps?: Step[];
  status: TaskStatus;
  type: TaskType;
  project_id?: string;
  parent_id?: string;
  created_at: string;
}
```

**Agent Types:**
```typescript
type AgentRunStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

interface AgentRun {
  id: string;
  task_id: string;
  status: AgentRunStatus;
  logs: string | null;
  error_message: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}
```

### Services Layer

| Service | Purpose | API Base |
|---------|---------|----------|
| `api.ts` | Generic fetch wrapper with error handling | `http://localhost:8000` |
| `tasks.ts` | Task CRUD + steps update | `/api/tasks` |
| `agent.ts` | Agent run management | `/api/agent/*` |
| `events.ts` | SSE subscription | `/api/events` |
| `schema.ts` | Schema + enums fetching | `/api/schema/*` |
| `settings.ts` | Backend settings | `/api/settings` |
| `toast.ts` | Toast notifications | svelte-sonner |

### SSE Event Handling

```typescript
// events.ts
export function subscribeToEvents(callback: (event: SSEEvent) => void) {
  const eventSource = new EventSource(`${API_BASE}/api/events`);

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    callback(data);
  };

  return () => eventSource.close();
}

// Usage in +page.svelte
onMount(() => {
  const cleanup = subscribeToEvents((event) => {
    switch (event.type) {
      case 'task_created':
        tasks = [...tasks, mapBackendToTask(event.data)];
        break;
      case 'task_updated':
        tasks = tasks.map(t => t.id === event.data.id
          ? mapBackendToTask(event.data) : t);
        break;
      case 'task_deleted':
        tasks = tasks.filter(t => t.id !== event.data.id);
        break;
      case 'agent_log':
        // Handle agent log event
        break;
    }
  });

  return cleanup;
});
```

---

## Data Flow

### CRUD Operations

```
┌──────────────┐     HTTP Request     ┌──────────────┐     SQL Query     ┌──────────────┐
│   Frontend   │ ──────────────────► │   FastAPI    │ ────────────────► │   SQLite     │
│  Component   │                      │   Route      │                   │   Database   │
└──────────────┘                      └──────────────┘                   └──────────────┘
       ▲                                     │
       │                                     │
       │            JSON Response            │
       └─────────────────────────────────────┘
```

### Real-time Updates

```
┌──────────────┐     Event Publish    ┌──────────────┐      SSE         ┌──────────────┐
│   Service    │ ──────────────────► │   EventBus   │ ────────────────► │   Frontend   │
│ (task_service│                      │              │                   │ (events.ts)  │
│  orchestrator)                      │              │                   │              │
└──────────────┘                      └──────────────┘                   └──────────────┘
                                                                               │
                                                                               ▼
                                                                        State Update
                                                                        + UI Re-render
```

---

## Component Status

### Backend

| Component | Status | Notes |
|-----------|--------|-------|
| Models (Task, Project, AgentRun) | ✅ Complete | Full CRUD + steps/parent_id |
| Database (SQLAlchemy async) | ✅ Complete | SQLite + aiosqlite |
| API Routes (CRUD) | ✅ Complete | Projects, Tasks, Agent, Events |
| API Routes (Schema) | ✅ Complete | Dynamic form schemas |
| API Routes (Settings) | ✅ Complete | Backend config via API |
| Services | ✅ Complete | Event publishing integrated |
| EventBus (SSE) | ✅ Complete | All event types supported |
| Orchestrator | ✅ Complete | Plan + Execute support |
| MCP Filesystem | ✅ MVP | Sandboxed file operations |

### Frontend

| Component | Status | Notes |
|-----------|--------|-------|
| Types (Task, Agent, Schema) | ✅ Complete | Full type coverage |
| Stores (Schema, Settings) | ✅ Complete | Svelte 5 runes |
| Services (API, Events, Schema) | ✅ Complete | All endpoints covered |
| Board.svelte | ✅ Complete | Drag & drop working |
| Column.svelte | ✅ Complete | Status grouping |
| TaskCard.svelte | ✅ Complete | Expandable with subtasks |
| SubtaskTree.svelte | ✅ Complete | Tree with status icons |
| Header.svelte | ✅ Complete | Tabs, toggle |
| FunctionPanel.svelte | ✅ Complete | Tab routing |
| TaskEditor.svelte | ✅ Complete | Schema-driven, steps toggle |
| AgentList.svelte | ✅ Complete | Historical runs |
| AgentLog.svelte | ✅ Complete | SSE integration |
| ProjectOverview.svelte | ✅ MVP | Basic info |
| SettingsPanel.svelte | ✅ Complete | Frontend + Backend settings |
| Form Components | ✅ Complete | Schema-driven rendering |

---

## Key Design Decisions

### 1. Schema-Driven Forms

Forms are rendered dynamically based on backend schema definitions. This ensures consistency between backend validation and frontend forms.

### 2. Claude Agent SDK with bypassPermissions

The orchestrator runs with `bypassPermissions=true` (YOLO mode) within the sandboxed workspace. This allows automated file operations without user confirmation.

**Security:** All MCP tools are restricted to the project's `workspace_path`.

### 3. Subtask Architecture

Tasks can have:
- **Steps** (JSON array): Checklist items within a single task
- **Subtasks** (parent_id FK): Child tasks created by agent planning

The agent `plan` endpoint decomposes complex tasks into subtasks, which can then be executed individually.

### 4. Git Auto-Checkpoints

Before each agent run, a git checkpoint is created. On success, changes are committed. This provides rollback capability and audit trail.

### 5. SSE for Real-time Updates

Instead of WebSockets, we use Server-Sent Events (SSE) for simplicity. The EventBus pattern decouples producers from consumers.

### 6. Frontend/Backend Status Mapping

Task statuses use different cases (Frontend: `'TODO'`, Backend: `'todo'`). Mapping functions in `types/task.ts` handle conversion.

### 7. Backend Settings via API

Backend configuration (agent model, max turns, git settings) is exposed via `/api/settings` and stored in `.kanban/settings.json`. This allows the frontend to configure agent behavior.

---

## MCP Architecture Vision

Das System folgt dem Prinzip: **Kanban = Orchestration (stabil), MCPs = Features (austauschbar)**

### Bidirektionale Integration

```
┌──────────────┐     MCP      ┌──────────────┐     MCP      ┌──────────────┐
│ Claude Code  │◄────────────►│   Kanban     │◄────────────►│  Perplexity  │
│   (Client)   │              │(Server+Client)│             │   (Server)   │
└──────────────┘              └──────────────┘              └──────────────┘
```

**A) Kanban NUTZT MCPs** - Orchestrator ruft externe Tools
**B) Kanban IST ein MCP** - Claude Code kann Tasks erstellen

---

*Last updated: 2026-01-24*
