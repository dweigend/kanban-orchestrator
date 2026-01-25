# 🤖 Agents Module

> Claude Agent SDK integration for task execution and planning

## 📋 Contents

| File | Description | Lines |
|------|-------------|-------|
| `orchestrator.py` | Re-export Hub (Backward Compatibility) | ~30 |
| `types.py` | Dataclasses: `AgentLogEntry`, `AgentResult` | ~25 |
| `executor.py` | Agent Execution with Claude SDK | ~200 |
| `planner.py` | Task Decomposition & Subtask Creation | ~120 |
| `subtask_executor.py` | Sequential Subtask Execution | ~65 |

## 🏗️ Architecture

```
orchestrator.py (Re-Export Hub)
├── types.py
│   ├── AgentLogEntry
│   └── AgentResult
├── executor.py
│   ├── execute_agent_run()
│   ├── stop_agent_run()
│   └── _finalize_run(), _publish_task_update(), _publish_finished_log()
├── planner.py
│   ├── plan_task_decomposition()
│   └── _create_placeholder_subtasks(), _build_planning_prompt()
└── subtask_executor.py
    └── execute_subtasks_sequentially()
```

## 🔧 Usage

```python
# Import via orchestrator (recommended)
from src.agents.orchestrator import (
    execute_agent_run,
    plan_task_decomposition,
    execute_subtasks_sequentially,
    AgentResult,
)

# Or direct imports
from src.agents.executor import execute_agent_run
from src.agents.planner import plan_task_decomposition
```

## 📚 Functions

### execute_agent_run()
Executes a task with Claude Agent SDK.
- Creates Git checkpoint before execution
- Streams logs via SSE to frontend
- Creates Git commit on success

### plan_task_decomposition()
Decomposes a task into subtasks.
- Creates 3 subtasks (Setup/Implement/Finalize)
- Sets parent status to NEEDS_REVIEW

### execute_subtasks_sequentially()
Executes all subtasks of a parent task sequentially.
- Called after user approval
- Updates parent status at the end

## 📡 Events

The module sends the following SSE events:
- `task_updated`: On status changes
- `task_created`: On subtask creation
- `agent_log`: For live logs (including `finished` event at the end)
