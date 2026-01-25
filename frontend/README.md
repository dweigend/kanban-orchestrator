# 🎨 Frontend

> SvelteKit 5 + bits-ui Kanban Board UI

## 📋 Quick Start

```bash
# Install dependencies
bun install

# Run dev server
bun dev
```

Open `http://localhost:5173`

## 📁 Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── components/   # UI Components
│   │   ├── services/     # API Client
│   │   ├── stores/       # State Management
│   │   ├── types/        # TypeScript Interfaces
│   │   └── utils/        # Utility Functions
│   └── routes/           # SvelteKit Pages
├── static/               # Static assets
└── package.json          # Dependencies
```

## 🔧 Commands

```bash
# Development
bun dev

# Lint + Format
bunx biome check --write .

# Type Check
bunx svelte-check --threshold warning

# Test
bun test

# All checks
bunx biome check --write . && bunx svelte-check --threshold warning
```

## 🧩 Key Components

| Component | Description |
|-----------|-------------|
| `KanbanBoard` | Main board with columns |
| `TaskCard` | Draggable task cards |
| `TaskEditor` | Task detail editor |
| `AgentLog` | Real-time agent output |
| `SettingsPanel` | App configuration |

## 📚 Tech Stack

- **Runtime**: Bun
- **Framework**: SvelteKit 5
- **UI**: bits-ui
- **Styling**: Tailwind CSS 4
- **Linting**: Biome
