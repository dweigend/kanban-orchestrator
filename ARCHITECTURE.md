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
│  │              Services (API, Events, Tasks, Agent)           ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP + SSE
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    API Routes Layer                       │   │
│  │  /api/projects  /api/tasks  /api/agent/*  /api/events    │   │
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
    │   ├── task.py            # Task Model
    │   ├── project.py         # Project Model
    │   └── agent_run.py       # AgentRun Model
    ├── api/
    │   ├── schemas.py         # Pydantic Schemas
    │   ├── events.py          # EventBus + SSE
    │   ├── task_service.py    # Task Business Logic
    │   ├── project_service.py # Project Business Logic
    │   └── routes/
    │       ├── projects.py    # /api/projects
    │       ├── tasks.py       # /api/tasks
    │       ├── agent.py       # /api/agent/*
    │       └── events.py      # /api/events (SSE)
    ├── agents/
    │   └── orchestrator.py    # Claude Agent SDK Integration
    └── mcp_servers/
        ├── registry.py        # MCP Server Registry
        └── filesystem/
            └── server.py      # File I/O Tools
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
└─────────────────┘     │ status          │     │ error_message   │
                        │ parent_id (FK)──┼──┐  │ started_at      │
                        │ created_at      │  │  │ completed_at    │
                        └─────────────────┘  │  └─────────────────┘
                                │            │
                                └────────────┘
                              (Self-Reference: Subtasks)
```

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
DELETE /api/tasks/{id}            Delete task
```

#### Agent
```
POST   /api/agent/run             Start agent for task (202 Accepted)
POST   /api/agent/stop/{id}       Stop running agent
GET    /api/agent/runs            List agent runs (filter: task_id, status)
GET    /api/agent/runs/{id}       Get agent run details
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

### MCP Server System

```
mcp_servers/
├── registry.py        # Central configuration
└── filesystem/
    └── server.py      # Sandboxed file operations
```

**Available Tools (Filesystem MCP):**

| Tool | Description |
|------|-------------|
| `read_file(path)` | Read file content |
| `write_file(path, content)` | Write to file |
| `list_directory(path)` | List directory contents |
| `create_directory(path)` | Create directory |
| `delete_file(path)` | Delete file |
| `file_exists(path)` | Check file existence |

All operations are sandboxed within the project's `workspace_path`.

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
    │   ├── +layout.svelte      # Root Layout
    │   └── +page.svelte        # Main Page
    └── lib/
        ├── types/
        │   ├── task.ts         # Task interfaces + mappings
        │   └── agent.ts        # Agent interfaces
        ├── services/
        │   ├── api.ts          # Generic fetch wrapper
        │   ├── tasks.ts        # Task CRUD
        │   ├── agent.ts        # Agent execution
        │   ├── events.ts       # SSE subscription
        │   └── toast.ts        # Notifications
        └── components/
            ├── kanban/
            │   ├── Board.svelte    # Main board container
            │   ├── Column.svelte   # Status column
            │   └── TaskCard.svelte # Task card
            ├── layout/
            │   └── Header.svelte   # App header
            └── panel/
                ├── FunctionPanel.svelte   # Main sidebar container
                ├── ProjectOverview.svelte # Project info
                ├── AgentList.svelte       # Agent status list
                ├── AgentLog.svelte        # Agent execution logs
                ├── SystemLog.svelte       # System logs
                ├── TaskEditor.svelte      # Task edit form
                ├── SearchBar.svelte       # Search input
                └── SettingsPanel.svelte   # Settings
```

### Component Hierarchy

```
+page.svelte
├── Header.svelte
│   └── Tabs: overview | agents | settings
├── Board.svelte
│   └── Column.svelte (×4: TODO, IN_PROGRESS, NEEDS_REVIEW, DONE)
│       └── TaskCard.svelte (for each task)
└── FunctionPanel.svelte
    ├── SearchBar.svelte
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
let viewMode = $state('hub-view');
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

interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  type: TaskType;
  projectId?: string;
  parentId?: string;
  createdAt: Date;
}
```

**Agent Types:**
```typescript
type AgentStatus = 'idle' | 'running' | 'completed' | 'failed';
type AgentType = 'orchestrator' | 'coder' | 'researcher' | 'architect';

interface AgentRun {
  id: string;
  taskId: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  errorMessage?: string;
  startedAt: Date;
  completedAt?: Date;
}
```

### Services Layer

| Service | Purpose | API Base |
|---------|---------|----------|
| `api.ts` | Generic fetch wrapper with error handling | `http://localhost:8000` |
| `tasks.ts` | Task CRUD operations | `/api/tasks` |
| `agent.ts` | Agent run management | `/api/agent/*` |
| `events.ts` | SSE subscription | `/api/events` |
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
| Models (Task, Project, AgentRun) | ✅ Complete | Full CRUD support |
| Database (SQLAlchemy async) | ✅ Complete | SQLite + aiosqlite |
| API Routes | ✅ Complete | Projects, Tasks, Agent, Events |
| Services | ✅ Complete | Event publishing integrated |
| EventBus (SSE) | ✅ Complete | All event types supported |
| Orchestrator | ✅ MVP | Claude Agent SDK working |
| MCP Filesystem | ✅ MVP | Sandboxed file operations |
| MCP Perplexity | 🔲 Planned | Web search integration |
| MCP OpenAlex | 🔲 Planned | Scientific paper search |
| MCP BibTeX | 🔲 Planned | Citation management |

### Frontend

| Component | Status | Notes |
|-----------|--------|-------|
| Types (Task, Agent) | ✅ Complete | Full type coverage |
| Services (API, Events) | ✅ Complete | All endpoints covered |
| Board.svelte | ✅ Complete | Drag & drop working |
| Column.svelte | ✅ Complete | Status grouping |
| TaskCard.svelte | ✅ Complete | Draggable cards |
| Header.svelte | ✅ Complete | Tabs, toggle |
| FunctionPanel.svelte | ✅ Complete | Tab routing |
| TaskEditor.svelte | ✅ Complete | Create/edit tasks |
| AgentList.svelte | ✅ MVP | Mock data (needs backend) |
| AgentLog.svelte | ✅ MVP | SSE integration |
| ProjectOverview.svelte | ✅ MVP | Basic info |
| Run Button on TaskCard | 🔲 Planned | UI integration |
| Project Selector | 🔲 Planned | Multi-project support |

---

## Key Design Decisions

### 1. Claude Agent SDK with bypassPermissions

The orchestrator runs with `bypassPermissions=true` (YOLO mode) within the sandboxed workspace. This allows automated file operations without user confirmation.

**Security:** All MCP tools are restricted to the project's `workspace_path`.

### 2. MCP Server Registry Pattern

MCP servers are modular and registered in `mcp_servers/registry.py`. New capabilities (Perplexity, OpenAlex) can be added without modifying the orchestrator.

### 3. Git Auto-Checkpoints

Before each agent run, a git checkpoint is created. On success, changes are committed. This provides rollback capability and audit trail.

### 4. SSE for Real-time Updates

Instead of WebSockets, we use Server-Sent Events (SSE) for simplicity. The EventBus pattern decouples producers from consumers.

### 5. Frontend/Backend Status Mapping

Task statuses use different cases (Frontend: `'TODO'`, Backend: `'todo'`). Mapping functions in `types/task.ts` handle conversion.

---

## Future Architecture

### Planned Extensions

```
┌─────────────────────────────────────────────────────────────────┐
│                      MCP Server Ecosystem                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Filesystem │  │  Perplexity │  │   OpenAlex  │             │
│  │  (Current)  │  │  (Planned)  │  │  (Planned)  │             │
│  │             │  │             │  │             │             │
│  │ read_file   │  │ web_search  │  │ search_papers│            │
│  │ write_file  │  │ deep_research│ │ get_citations│            │
│  │ list_dir    │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   BibTeX    │  │   GitHub    │  │  Database   │             │
│  │  (Planned)  │  │  (Future)   │  │  (Future)   │             │
│  │             │  │             │  │             │             │
│  │ manage_refs │  │ create_pr   │  │ sql_query   │             │
│  │ format_cite │  │ review_code │  │ migrations  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow Templates

Future: Predefined task chains with automatic agent orchestration.

```
Research Workflow:
  1. Perplexity: Web search for topic
  2. OpenAlex: Find academic papers
  3. BibTeX: Generate citations
  4. Filesystem: Write summary document
```

---

*Last updated: 2026-01-14*
