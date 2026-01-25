# WORKFLOW

## Principles

- **KISS** - Simplest solution wins
- **Separation of Concerns** - Backend = Agents/API, Frontend = UI
- **Clean Code** - Readable > clever

---

## STEPS

### STEP: checkpoint

TRIGGER: Before risky changes OR start of new feature
ACTION: `git add -A && git commit -m "checkpoint: 📍 before [description]"`

---

### STEP: research

TRIGGER: Unclear requirements OR new technology

ACTIONS:
```
1. CODEBASE: Does this already exist here?
   - Grep for similar functions/patterns
   - Read related files
   → If found: USE IT

2. LIBRARY: Is there a library for this?
   - mcp__context7__ for docs
   - WebSearch for options
   → If found: USE IT

3. ONLY THEN: Plan custom implementation
```

Tool priority: Codebase search > mcp__context7__ > WebSearch > mcp__perplexity__

SKIP_IF: Requirements clear AND solution approach known

---

### STEP: plan

TRIGGER: Complex tasks (multiple files OR architectural decisions)
SKIP_IF: Trivial changes (typos, single-line fixes)

Use subagents for complex scope analysis:
- Explore agents (parallel, haiku) for finding files
- Plan agent (sonnet) for implementation strategy

---

### STEP: implement

TRIGGER: After plan OR after research
ACTIONS:
1. Small, focused changes
2. One feature/fix per iteration
3. Follow stack rules from `.claude/rules/fullstack.md`

---

### STEP: verify

TRIGGER: After implement

**Backend (Python):**
```bash
cd backend

# Lint + Format
uv run ruff check --fix .
uv run ruff format .

# Type check
uvx ty check

# Test
uv run pytest
```

**Frontend (TypeScript):**
```bash
cd frontend

# Lint + Format
bunx biome check --write .

# Type check
bunx svelte-check --threshold warning

# Test
bun test
```

MAX_ITERATIONS: 3

---

### STEP: commit

TRIGGER: After verify
ACTIONS:
1. `git add -A`
2. `git commit -m "type: emoji description"`
3. Update `dev/HANDOVER.md`
4. Update `dev/PLAN.md` (check off tasks)

---

## ISSUE TRACKING

**GitHub = Single Source of Truth:** https://github.com/dweigend/kanban-orchestrator/issues

### Grundprinzip

Issues sollen Feature-Arbeit NICHT blockieren. Erfassen → Weiterarbeiten → Später fixen.

### Workflow

```
1. Problem/Idee entdeckt
2. SOFORT Issue anlegen: gh issue create --title "🔴/🟡/🔵 Titel" --label "bug|enhancement|refactoring"
3. Weiter am aktuellen Task
4. Issue in dedizierter Session fixen
```

### Issue-Typen & Labels

| Prefix | Label | Bedeutung |
|--------|-------|-----------|
| 🔴 | `bug` | Fehler, hohe Prio |
| 🟡 | `enhancement` | Feature, mittlere Prio |
| 🔵 | `enhancement` | Nice-to-have, niedrige Prio |
| 🔧 | `refactoring` | Code Quality |

### Cleanup-Sessions

Regelmäßige Sessions für:
- Bug Fixes (🔴 zuerst)
- Refactoring (🔧)
- Tech Debt

### NEVER

- ❌ Issues lokal tracken (nur GitHub)
- ❌ Issues sofort fixen wenn anderer Task läuft
- ❌ Issues ignorieren (immer erfassen!)

---

## COMMIT TYPES

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

---

## CONSTRAINTS

- NEVER mention AI/Claude in commits
- ALWAYS check codebase before writing new code
- ALWAYS test before commit
- ALWAYS update docs at session end

*Updated: 2026-01-25*
