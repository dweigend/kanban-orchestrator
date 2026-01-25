# 🧩 Components

> Svelte 5 UI components for the Kanban board

## 📋 Contents

| Directory | Description |
|-----------|-------------|
| `form/` | Form field components (text, select, datetime) |
| `kanban/` | Board, Column, TaskCard, SubtaskTree |
| `layout/` | Header navigation |
| `panel/` | Side panels (TaskEditor, AgentLog) |
| `settings/` | Settings panel components |

## 🏗️ Architecture

```
components/
├── form/           # Reusable form fields
│   ├── FieldText.svelte
│   ├── FieldTextarea.svelte
│   ├── FieldSelect.svelte
│   ├── FieldDatetime.svelte
│   └── FieldRenderer.svelte
├── kanban/         # Board components
│   ├── Board.svelte
│   ├── Column.svelte
│   ├── TaskCard.svelte
│   └── SubtaskTree.svelte
├── layout/         # App layout
│   └── Header.svelte
├── panel/          # Detail panels
│   ├── TaskEditor.svelte
│   ├── AgentLog.svelte
│   ├── AgentList.svelte
│   ├── ProjectOverview.svelte
│   ├── FunctionPanel.svelte
│   └── SystemLog.svelte
└── settings/       # Settings UI
    └── SettingsPanel.svelte
```

## 🎯 Design Principles

1. **Single Responsibility** - One component, one purpose
2. **Props over local state** - Parent controls state
3. **Svelte 5 Runes** - `$state`, `$derived`, `$effect`
4. **Tailwind only** - No custom CSS
