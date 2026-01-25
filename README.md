# 🎯 Kanban Orchestrator

> ⚠️ **Work in Progress** — This project is under active development. APIs and features may change.

**AI Agent Orchestration Layer with Kanban UI**

A personal project for orchestrating AI coding agents through a simple Kanban board interface. Built on the Claude Code SDK.

---

## 💡 Why This Exists

AI tools evolve rapidly. New models, new capabilities, new APIs — constantly changing. But the **orchestration layer** stays stable.

This project focuses on:
- **Task management** over individual tool capabilities
- **Simple workflows** over complex multi-agent systems
- **Practical orchestration** for research and prototyping

Inspired by [VibeKanban](https://vibekanban.com) — learned from [experimenting with it](https://github.com/dweigend/vibe-kanban) that simpler is better.

---

## 🔧 Tech Stack

| Layer | Stack |
|-------|-------|
| **Backend** | Python, FastAPI, SQLite, Claude Agent SDK |
| **Frontend** | SvelteKit 5, bits-ui, Tailwind CSS |
| **Communication** | REST API + SSE (real-time updates) |

---

## 📋 Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python)
- [Bun](https://bun.sh/) (TypeScript)

---

## 🚀 Quick Start

1. **Configure Backend**
   ```bash
   cd backend
   cp .kanban/mcps.yaml.example .kanban/mcps.yaml
   cp .kanban/settings.json.example .kanban/settings.json
   # Edit mcps.yaml to configure MCP servers
   ```

2. **Start Backend**
   ```bash
   uv run python main.py
   ```

3. **Start Frontend** (separate terminal)
   ```bash
   cd frontend
   bun install
   bun dev
   ```

4. Open `http://localhost:5173`

---

## 🗺️ Roadmap

- [ ] **Research Agent** — Distribute complex research across multiple tasks
- [ ] **Task Database** — Store repeating tasks and instructions
- [ ] **Context System** — Better context management for agents
- [ ] **Multi-Model Support** — OpenAI, Gemini, and other providers

---

## 📁 Structure

```
kanban-orchestrator/
├── backend/          # FastAPI + Claude SDK
│   ├── src/agents/   # Agent implementations
│   ├── src/api/      # REST endpoints
│   └── src/models/   # Pydantic models
└── frontend/         # SvelteKit UI
    ├── src/lib/      # Components, services, stores
    └── src/routes/   # Pages
```

---

## 🤝 Contributing

Issues and PRs welcome! See [GitHub Issues](https://github.com/dweigend/kanban-orchestrator/issues).

---

## 📄 License

MIT
