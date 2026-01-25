# Agents Module

Claude Agent SDK integration für Task-Ausführung und -Planung.

## Module

| Datei | Beschreibung | Zeilen |
|-------|--------------|--------|
| `orchestrator.py` | Re-Export Hub (Backward Compatibility) | ~30 |
| `types.py` | Dataclasses: `AgentLogEntry`, `AgentResult` | ~25 |
| `executor.py` | Agent Execution mit Claude SDK | ~200 |
| `planner.py` | Task Decomposition & Subtask-Erstellung | ~120 |
| `subtask_executor.py` | Sequentielle Subtask-Ausführung | ~65 |

## Architektur

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

## Verwendung

```python
# Import über orchestrator (empfohlen)
from src.agents.orchestrator import (
    execute_agent_run,
    plan_task_decomposition,
    execute_subtasks_sequentially,
    AgentResult,
)

# Oder direkte Imports
from src.agents.executor import execute_agent_run
from src.agents.planner import plan_task_decomposition
```

## Funktionen

### execute_agent_run()
Führt einen Task mit Claude Agent SDK aus.
- Erstellt Git Checkpoint vor Ausführung
- Streamt Logs via SSE an Frontend
- Erstellt Git Commit bei Erfolg

### plan_task_decomposition()
Zerlegt einen Task in Subtasks.
- Erstellt 3 Subtasks (Setup/Implement/Finalize)
- Setzt Parent-Status auf NEEDS_REVIEW

### execute_subtasks_sequentially()
Führt alle Subtasks eines Parent-Tasks sequentiell aus.
- Wird nach User-Approval aufgerufen
- Aktualisiert Parent-Status am Ende

## Events

Das Modul sendet folgende SSE Events:
- `task_updated`: Bei Status-Änderungen
- `task_created`: Bei Subtask-Erstellung
- `agent_log`: Für Live-Logs (inkl. `finished` Event am Ende)
