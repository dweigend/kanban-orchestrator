# 🎯 Kanban Orchestrator

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

## 🚀 Quick Start

```bash
# Backend
cd backend
uv run python main.py

# Frontend (separate terminal)
cd frontend
bun dev
```

Open `http://localhost:5173`

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
├── frontend/         # SvelteKit UI
│   ├── src/lib/      # Components, services, stores
│   └── src/routes/   # Pages
└── dev/              # Workflow documentation
```

---

## 📄 License

MIT
