# 📝 Types

> TypeScript interfaces and type definitions

## 📋 Contents

| File | Description |
|------|-------------|
| `task.ts` | Task, TaskStatus, Priority interfaces |
| `agent.ts` | AgentRun, AgentLogEntry interfaces |
| `schema.ts` | TaskSchema, Section, Field interfaces |

## 🏗️ Key Types

### Task (`task.ts`)

```typescript
interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: Priority;
  parent_id: string | null;
  subtasks: Task[];
  created_at: string;
  updated_at: string;
}

type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE' | 'NEEDS_REVIEW' | 'BLOCKED';
type Priority = 'LOW' | 'MEDIUM' | 'HIGH';
```

### Agent (`agent.ts`)

```typescript
interface AgentRun {
  id: string;
  task_id: string;
  status: 'running' | 'completed' | 'failed';
  model: string;
  started_at: string;
  finished_at: string | null;
}

interface AgentLogEntry {
  type: 'text' | 'tool_use' | 'tool_result' | 'error';
  content: string;
  timestamp: string;
}
```

### Schema (`schema.ts`)

```typescript
interface TaskSchema {
  sections: Section[];
}

interface Section {
  name: string;
  fields: Field[];
}

interface Field {
  name: string;
  type: FieldType;
  label: string;
  required: boolean;
}
```
