# 📚 Frontend Library

> Shared components, services, stores, and utilities

## 📋 Contents

| Directory | Description |
|-----------|-------------|
| `components/` | UI Components (Svelte 5) |
| `services/` | API Client & Event Handling |
| `stores/` | State Management (Svelte 5 Runes) |
| `types/` | TypeScript Interfaces |
| `assets/` | Static Assets |

## 🏗️ Architecture

```
lib/
├── components/
│   ├── form/       # Form field components
│   ├── kanban/     # Board, Column, TaskCard
│   ├── layout/     # Header
│   ├── panel/      # Side panels (Editor, Log)
│   └── settings/   # Settings components
├── services/
│   ├── api.ts      # Base API client
│   ├── tasks.ts    # Task API
│   ├── agent.ts    # Agent API
│   ├── events.ts   # SSE handling
│   └── settings.ts # Settings API
├── stores/
│   ├── schema.svelte.ts   # Dynamic schema store
│   └── settings.svelte.ts # Settings store
└── types/
    ├── task.ts     # Task interfaces
    ├── agent.ts    # Agent interfaces
    └── schema.ts   # Schema interfaces
```

## 🔧 Import Pattern

```typescript
// Components
import Board from '$lib/components/kanban/Board.svelte';
import TaskEditor from '$lib/components/panel/TaskEditor.svelte';

// Services
import { taskApi } from '$lib/services/tasks';
import { eventService } from '$lib/services/events';

// Stores
import { schemaStore } from '$lib/stores/schema.svelte';

// Types
import type { Task, TaskStatus } from '$lib/types/task';
```
