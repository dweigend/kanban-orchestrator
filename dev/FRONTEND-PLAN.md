# Frontend Plan: Kanban Orchestrator UI

## Design-Regeln

### Sidebar-First Architecture

**ALLE Funktionen in der Sidebar (FunctionPanel)!**

| Bereich | Erlaubt | Verboten |
|---------|---------|----------|
| **Hauptfenster** | Kanban Board | Dialoge, Formulare |
| **Sidebar** | Editor, Settings, Logs | - |
| **Popups** | - | ❌ Keine modalen Dialoge |

---

## Implementierte Komponenten ✅

### Layout
- ✅ Header mit Icon-Buttons für Sidebar-Tabs
- ✅ Resizable Sidebar (FunctionPanel)
- ✅ Controlled Component Pattern (activeTab in Page)

### Kanban Board
- ✅ Board.svelte - Container mit Columns
- ✅ Column.svelte - Drop Target für Drag & Drop
- ✅ TaskCard.svelte - Draggable, Click → Editor

### Sidebar Panels
- ✅ FunctionPanel.svelte - Tab-Container
- ✅ TaskEditor.svelte - Create/Edit Tasks
- ✅ SettingsPanel.svelte - App Settings
- ✅ AgentLog.svelte - Agent Output Stream (NEU, noch nicht eingebunden)
- ✅ ProjectOverview.svelte
- ✅ AgentList.svelte
- ✅ SystemLog.svelte

### Services
- ✅ api.ts - Fetch wrapper
- ✅ tasks.ts - Task CRUD
- ✅ events.ts - SSE subscription (+agent_log)
- ✅ agent.ts - Agent API (NEU)
- ✅ toast.ts - Notifications

---

## File Structure (Aktuell)

```
frontend/src/
├── lib/
│   ├── components/
│   │   ├── layout/
│   │   │   └── Header.svelte
│   │   ├── kanban/
│   │   │   ├── Board.svelte
│   │   │   ├── Column.svelte
│   │   │   └── TaskCard.svelte
│   │   └── panel/
│   │       ├── FunctionPanel.svelte
│   │       ├── TaskEditor.svelte
│   │       ├── SettingsPanel.svelte
│   │       ├── AgentLog.svelte      # NEU
│   │       ├── ProjectOverview.svelte
│   │       ├── AgentList.svelte
│   │       ├── SystemLog.svelte
│   │       └── SearchBar.svelte
│   ├── services/
│   │   ├── api.ts
│   │   ├── tasks.ts
│   │   ├── events.ts
│   │   ├── agent.ts                 # NEU
│   │   └── toast.ts
│   └── types/
│       ├── task.ts                  # +NEEDS_REVIEW
│       └── agent.ts                 # +AgentRun, AgentLogEntry
├── routes/
│   ├── +layout.svelte
│   └── +page.svelte
└── app.css
```

---

## Nächste Schritte (Phase 4.2)

### 1. AgentLog in Sidebar einbinden
```svelte
<!-- FunctionPanel.svelte -->
{#if activeTab === 'agent'}
  <AgentLog logs={agentLogs} isRunning={isAgentRunning} />
{/if}
```

### 2. Run Button auf TaskCard
```svelte
<!-- TaskCard.svelte - im Dropdown -->
<DropdownMenu.Item onclick={() => onRunAgent?.(task)}>
  Run Agent
</DropdownMenu.Item>
```

### 3. NEEDS_REVIEW Spalte
```typescript
// +page.svelte
const columns: TaskStatus[] = ['TODO', 'IN_PROGRESS', 'NEEDS_REVIEW', 'DONE'];
```

### 4. Spinner auf Card
```svelte
<!-- TaskCard.svelte -->
{#if task.status === 'IN_PROGRESS'}
  <span class="animate-spin">⟳</span>
{/if}
```

---

## Design Tokens

```css
/* app.css - bereits implementiert */
--bg-base: #0a0a0a;
--bg-elevated: #141414;
--border-default: #3f3f46;
--text-primary: #fafafa;
--text-muted: #71717a;
--accent-primary: #a78bfa;

/* Task Type Colors */
--task-research: #3b82f6;
--task-dev: #f97316;
--task-notes: #eab308;
--task-neutral: #525250;
```

---

*Updated: 2026-01-14*
