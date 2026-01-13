# Full-Stack Development Rules

## Decision Tree (ALWAYS FOLLOW!)

```
1. Does this already exist in the codebase? → USE IT
2. Is there a library for this? → USE IT
3. Only as LAST RESORT → Write custom code
```

---

## Python Backend

### Principles

- **KISS** - Simplest solution wins
- **Early Returns** - Validate first, exit early, no deep nesting
- **Functions < 20 lines** - Break down complex logic
- **Explicit types** - Always use type hints
- **Pydantic Models** - For all data validation

### Commands

```bash
cd backend

# Run
uv run python main.py

# Lint + Format
uv run ruff check --fix . && uv run ruff format .

# Type Check
uvx ty check

# Test
uv run pytest
```

### Patterns

```python
# ✅ Early returns + type hints
def process_task(task_id: str) -> Task | None:
    if not task_id:
        return None
    task = get_task(task_id)
    if not task:
        return None
    return transform_task(task)

# ✅ FastAPI + Pydantic
@app.post("/api/tasks", response_model=Task)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
) -> Task:
    return await task_service.create(db, task)

# ✅ Claude Agent SDK Pattern
async def run_agent(prompt: str) -> str:
    response = await client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

### Never (Python)

- ❌ Use `pip` (always `uv`)
- ❌ Use `mypy` (use `ty`)
- ❌ Skip type hints
- ❌ Deep nesting (>2 levels)

---

## TypeScript Frontend

### Principles

- **KISS** - Simplest solution wins
- **Early Returns** - Validate first, exit early
- **Functions < 20 lines** - Break down complex logic
- **Explicit types** - No `any`, always interfaces
- **bits-ui** - For UI components

### Commands

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
```

### Svelte 5 Runes

```typescript
// ✅ State management
const tasks = $state<Task[]>([]);
const activeCount = $derived(tasks.filter(t => t.status === 'active').length);

$effect(() => {
  console.log(`Active tasks: ${activeCount}`);
});

// ✅ Props
interface Props {
  task: Task;
  onUpdate: (task: Task) => void;
}
let { task, onUpdate }: Props = $props();
```

### Separation of Concerns

```
src/
├── lib/
│   ├── components/     # UI components (presentation)
│   ├── stores/         # State management
│   ├── services/       # API calls
│   ├── utils/          # Pure utility functions
│   └── types/          # TypeScript interfaces
├── routes/             # Pages (routing only)
```

### Never (TypeScript)

- ❌ Use `any` type
- ❌ Write components > 200 lines
- ❌ Write functions > 20 lines
- ❌ Custom CSS (use Tailwind)
- ❌ ESLint/Prettier (use Biome)

---

## API Communication

### FastAPI → SvelteKit

```python
# Backend: SSE for streaming agent updates
@app.get("/api/tasks/{id}/stream")
async def stream_task(id: str):
    async def event_generator():
        async for event in agent.run_stream(id):
            yield f"data: {json.dumps(event)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

```typescript
// Frontend: Consume SSE
const eventSource = new EventSource(`/api/tasks/${id}/stream`);
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateTaskStatus(data);
};
```

---

## Quality Gates

Before every commit:

```bash
# Backend
cd backend && uv run ruff check --fix . && uv run ruff format . && uvx ty check

# Frontend
cd frontend && bunx biome check --write . && bunx svelte-check --threshold warning
```

*Updated: 2026-01-13*
