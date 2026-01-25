# 🖼️ Layout Components

> Application layout and navigation

## 📋 Contents

| File | Description |
|------|-------------|
| `Header.svelte` | Top navigation bar |

## 🏗️ Architecture

```
┌────────────────────────────────────┐
│  Header                            │
│  [Logo] [Project] [Actions]        │
├────────────────────────────────────┤
│                                    │
│           Main Content             │
│                                    │
└────────────────────────────────────┘
```

## 🔧 Header Features

| Element | Description |
|---------|-------------|
| Logo | App branding |
| Project Selector | Switch between projects |
| New Task | Create task button |
| Settings | Open settings panel |
| Run Agent | Execute agent on selected task |

## 🔧 Usage

```svelte
<script>
  import Header from '$lib/components/layout/Header.svelte';
</script>

<Header
  project={currentProject}
  onNewTask={() => createTask()}
  onSettings={() => showSettings = true}
/>
```
