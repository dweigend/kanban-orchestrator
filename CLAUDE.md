# Kanban Orchestrator

## Overview

**Goal:** AI-gestützter Workflow-Orchestrator mit Kanban-Board UI für automatisierte Recherche, Programmierung und Prototyping
**Stack:** Full-Stack (Python backend + SvelteKit frontend)
**Libraries:** Claude Agent SDK, FastAPI, Pydantic, Google ADK, bits-ui, Tailwind

---

## Commands

### Backend (Python)

```bash
cd backend

# Run
uv run python main.py

# Lint + Format
uv run ruff check --fix . && uv run ruff format .

# Type check
uvx ty check

# Test
uv run pytest

# All checks
uv run ruff check --fix . && uv run ruff format . && uvx ty check
```

### Frontend (TypeScript/SvelteKit)

```bash
cd frontend

# Dev server
bun dev

# Lint + Format
bunx biome check --write .

# Type check
bunx svelte-check --threshold warning

# Test
bun test

# All checks
bunx biome check --write . && bunx svelte-check --threshold warning
```

### Root

```bash
# Start both servers
make dev

# Quality check all
make check
```

---

## Project Structure

```
kanban-orchestrator/
├── backend/
│   ├── src/
│   │   ├── agents/          # Claude SDK Agent Orchestrator
│   │   ├── api/             # FastAPI Routes + Services
│   │   ├── mcp_servers/     # MCP servers WE EXPOSE (Kanban → Claude Code)
│   │   ├── mcp_client/      # MCP config for servers WE USE (Orchestrator → MCPs)
│   │   ├── models/          # SQLAlchemy Models
│   │   └── services/        # Business Logic (git, etc.)
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/  # UI Components
│   │   │   ├── services/    # API Client
│   │   │   └── types/       # TypeScript Interfaces
│   │   └── routes/          # SvelteKit Pages
│   └── package.json
├── dev/                     # Workflow Docs
├── Makefile
└── README.md
```

---

## Principles

- **KISS** - Simplest solution wins
- **Separation of Concerns** - Clear backend/frontend split
- **Type Safety** - Python type hints + TypeScript types
- **API Contract** - Define interfaces clearly
- **Modular Design** - Plugin-ready architecture

## Before Writing Code

```
1. Does this exist in codebase? → USE IT
2. Is there a library? → USE IT
3. Last resort → Write code
```

---

## Stack

### Backend
| Component | Tool |
|-----------|------|
| Package Manager | uv |
| Framework | FastAPI |
| Validation | Pydantic |
| AI Agents | Claude Agent SDK |
| Workflows | Google ADK |
| Linting | Ruff |
| Type Checking | Ty |
| Testing | Pytest |
| Database | SQLite |

### Frontend
| Component | Tool |
|-----------|------|
| Runtime | Bun |
| Framework | SvelteKit 5 |
| UI | bits-ui |
| Styling | Tailwind CSS 4 |
| Linting | Biome |

---

## Integrations

| Service | Purpose |
|---------|---------|
| Perplexity | Search & Research |
| OpenAlex | Scientific Paper Analysis |
| BibTeX | Citation Management |

---

## NEVER

- ❌ Use pip (use uv)
- ❌ Use mypy (use ty)
- ❌ Use ESLint/Prettier (use Biome)
- ❌ Use `any` in TypeScript
- ❌ Custom CSS (use Tailwind)
- ❌ Mention AI in commits

---

## Workflow

1. Use `/start` to begin sessions
2. Follow `dev/WORKFLOW.md`
3. Update `dev/HANDOVER.md` at end

*Updated: 2026-01-16*
