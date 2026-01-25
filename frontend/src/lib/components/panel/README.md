# 📊 Panel Components

> Side panels for task editing and agent logs

## 📋 Contents

| File | Description |
|------|-------------|
| `TaskEditor.svelte` | Task detail editor |
| `AgentLog.svelte` | Real-time agent output |
| `AgentList.svelte` | Agent run history |
| `ProjectOverview.svelte` | Project stats |
| `FunctionPanel.svelte` | Function execution panel |
| `SystemLog.svelte` | System log viewer |

## 🏗️ Architecture

```
┌─────────────┬───────────────┐
│             │               │
│   Board     │    Panel      │
│             │               │
│             │ TaskEditor or │
│             │ AgentLog      │
│             │               │
└─────────────┴───────────────┘
```

## 🔧 TaskEditor

Displays task details with dynamic form fields:
- Title, description, status, priority
- Agent execution controls
- Subtask management

```svelte
<TaskEditor
  task={selectedTask}
  schema={taskSchema}
  onupdate={(task) => saveTask(task)}
/>
```

## 🔧 AgentLog

Real-time streaming of agent execution:
- Text output
- Tool calls and results
- Error messages
- Completion status

```svelte
<AgentLog taskId={selectedTask.id} />
```

## 🎯 Panel Switching

Panels are mutually exclusive - only one shows at a time:
- Click task → TaskEditor
- Run agent → AgentLog
- Click project → ProjectOverview
