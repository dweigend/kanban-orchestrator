# 🔗 Services

> API client and event handling

## 📋 Contents

| File | Description |
|------|-------------|
| `api.ts` | Base API client with fetch wrapper |
| `tasks.ts` | Task CRUD operations |
| `agent.ts` | Agent execution API |
| `events.ts` | SSE event handling |
| `settings.ts` | Settings API |
| `schema.ts` | Dynamic schema fetching |
| `toast.ts` | Toast notifications |

## 🏗️ Architecture

```
services/
├── api.ts        # Base: API_URL, fetch wrapper
├── tasks.ts      # taskApi.list(), create(), update(), delete()
├── agent.ts      # agentApi.run(), plan(), stop()
├── events.ts     # eventService.connect(), subscribe()
├── settings.ts   # settingsApi.load(), save()
├── schema.ts     # schemaApi.get()
└── toast.ts      # toast.success(), error()
```

## 🔧 Usage

```typescript
import { taskApi } from '$lib/services/tasks';
import { agentApi } from '$lib/services/agent';
import { eventService } from '$lib/services/events';

// Task operations
const tasks = await taskApi.list();
await taskApi.create({ title: 'New Task' });

// Agent execution
await agentApi.run(taskId);

// SSE events
eventService.subscribe('task_updated', (event) => {
  console.log('Task updated:', event.task);
});
```

## 📡 Event Types

| Event | Payload |
|-------|---------|
| `task_created` | `{ task: Task }` |
| `task_updated` | `{ task: Task }` |
| `task_deleted` | `{ task_id: string }` |
| `agent_log` | `{ task_id, type, content }` |
