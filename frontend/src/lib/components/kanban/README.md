# 📋 Kanban Components

> Board, columns, and task cards

## 📋 Contents

| File | Description |
|------|-------------|
| `Board.svelte` | Main kanban board container |
| `Column.svelte` | Status column (TODO, IN_PROGRESS, etc.) |
| `TaskCard.svelte` | Draggable task card |
| `SubtaskTree.svelte` | Nested subtask display |

## 🏗️ Architecture

```
Board (container)
├── Column (TODO)
│   ├── TaskCard
│   │   └── SubtaskTree
│   └── TaskCard
├── Column (IN_PROGRESS)
│   └── TaskCard
└── Column (DONE)
    └── TaskCard
```

## 🔧 Usage

```svelte
<script>
  import Board from '$lib/components/kanban/Board.svelte';

  let tasks = $state<Task[]>([]);
</script>

<Board
  {tasks}
  onselect={(task) => selectedTask = task}
  ondrop={(task, status) => updateStatus(task, status)}
/>
```

## 🎯 Features

- **Drag & Drop** - Move tasks between columns
- **Subtask Hierarchy** - Nested task display
- **Status Colors** - Visual status indicators
- **Click to Edit** - Opens TaskEditor panel
