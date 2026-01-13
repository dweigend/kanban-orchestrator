# Git Workflow

## Philosophy

- **Atomic Commits** - One logical change per commit
- **Issue Tracking** - Note problems, fix later
- **Checkpoints** - Save stable states before risky changes

---

## Branch Strategy

```
main
 └── feature/[name]     # New features
 └── fix/[name]         # Bug fixes
 └── refactor/[name]    # Code restructuring
```

### Commands

```bash
# Create feature branch
git checkout -b feature/add-task-api

# After completion
git checkout main
git merge feature/add-task-api
git branch -d feature/add-task-api
```

---

## Commit Format

```
type: emoji description

[optional body]
```

### Types

| Type | Emoji | Use |
|------|-------|-----|
| feat | ✨ | New feature |
| fix | 🐛 | Bug fix |
| refactor | ♻️ | Restructure |
| style | 💄 | Formatting |
| docs | 📝 | Documentation |
| chore | 🔧 | Maintenance |
| test | ✅ | Tests |
| checkpoint | 📍 | Stable state |

### Examples

```bash
git commit -m "feat: ✨ add task CRUD endpoints"
git commit -m "fix: 🐛 resolve SSE connection timeout"
git commit -m "refactor: ♻️ extract agent logic to service"
git commit -m "checkpoint: 📍 before major refactor"
```

---

## Issue Tracking

**Key principle:** Don't fix problems immediately.

```
1. Discover problem during implementation
2. Create Issue or note in PLAN.md Backlog
3. Continue with current task
4. Fix issues in dedicated session
```

### Create Issue

```bash
gh issue create --title "Bug: SSE drops connection after 30s" --body "..."
```

### Or Note in PLAN.md

```markdown
## Backlog

- SSE connection drops after 30s - needs investigation
```

---

## Checkpoints

Create checkpoints before:
- Major refactors
- Risky changes
- Experimental features

```bash
git add -A && git commit -m "checkpoint: 📍 before [description]"
```

---

## Never

- ❌ Commit directly to main (use branches)
- ❌ Mention AI/Claude in commits
- ❌ Commit untested code
- ❌ Commit secrets (.env, credentials)

*Updated: 2026-01-13*
