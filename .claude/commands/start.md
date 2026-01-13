---
description: Start a new development session
---

# Session Start: Kanban Orchestrator

## 1. Read Context

Read these files to understand current state:

```
dev/HANDOVER.md    # Last session summary
dev/PLAN.md        # Current phase & tasks
CLAUDE.md          # Project config & commands
```

## 2. Check Status

```bash
# Git status
git status

# Backend health
cd backend && uvx ty check

# Frontend health
cd frontend && bunx svelte-check --threshold warning
```

## 3. Review Plan

Check `dev/PLAN.md` for:
- Current phase
- Open tasks
- Backlog items

## 4. Ask User

"Womit sollen wir heute weitermachen?"

Options:
- Continue with current task from PLAN.md
- Start new task from backlog
- Fix an issue
- Other

## 5. Create Checkpoint

Before starting work:

```bash
git add -A && git commit -m "checkpoint: 📍 before [today's focus]"
```

## 6. Begin Work

Follow `dev/WORKFLOW.md` for implementation steps.

---

*Remember: Update `dev/HANDOVER.md` at session end!*
