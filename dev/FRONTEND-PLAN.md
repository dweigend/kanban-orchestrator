# Frontend Plan: Kanban Orchestrator UI

## ⚠️ Design-Regeln

### Sidebar-First Architecture

**ALLE Funktionen werden in die Sidebar (Function Panel) integriert!**

| Bereich | Erlaubt | Verboten |
|---------|---------|----------|
| **Hauptfenster** | Hub-View, Kanban-View | Dialoge, Formulare, Editoren |
| **Sidebar** | Settings, Task-Editor, Details, Logs | - |
| **Popups** | - | ❌ Keine modalen Dialoge für Funktionen |

**Begründung:**
- Konsistente UX ohne Kontext-Wechsel
- Fokus bleibt auf Kanban-Board
- Mobile-friendly (Sidebar kann versteckt werden)

### Interaktions-Patterns

```
Task erstellen    → Sidebar: TaskEditor Panel
Task bearbeiten   → Sidebar: TaskEditor Panel (prefilled)
Task löschen      → Inline-Confirmation im Card
Task Details      → Sidebar: TaskDetail Panel
Settings          → Sidebar: Settings Panel (Accordion)
```

---

## Design System (aus Mockups)

### Style: "Brutalist System"
- High-contrast UI für data-dense applications
- Strictly angular geometry, 1px borders
- Direct manipulation controls

### Layout Grid
- **Columns**: 12
- **Margin**: 24px fluid
- **Gutter**: 16px fixed
- **Border**: 1px solid zinc-700

### Typography
- **Font**: JetBrains Mono
- **Base Size**: 14px
- **Headings**: Uppercase tracking (letter-spacing: 0.1em)

### Color Palette

```css
/* Background */
--bg-base: #0a0a0a;
--bg-elevated: #141414;
--bg-surface: #1a1a1a;

/* Borders */
--border-default: #3f3f46;      /* zinc-700 */
--border-focus: #a78bfa;        /* violet-400 */
--border-error: #ef4444;        /* red-500 */

/* Text */
--text-primary: #fafafa;        /* zinc-50 */
--text-secondary: #a1a1aa;      /* zinc-400 */
--text-muted: #71717a;          /* zinc-500 */

/* Task Type Colors */
--task-research: #3b82f6;       /* blue-500 */
--task-dev: #f97316;            /* orange-500 */
--task-notes: #eab308;          /* yellow-500 */
--task-neutral: #525250;        /* zinc-600 */

/* Status */
--status-active: #22c55e;       /* green-500 */
--status-idle: #71717a;         /* zinc-500 */
--status-error: #ef4444;        /* red-500 */
--status-busy: #f97316;         /* orange-500 */

/* Accent */
--accent-primary: #a78bfa;      /* violet-400 */
```

---

## Component Structure

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Header (fixed)                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Logo │ Breadcrumb │ View Toggle │        Actions │ Settings ││
│  └─────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────┬─────────────────────────────┐│
│  │                               │                             ││
│  │   Kanban Board (main)         │   Function Panel (sidebar)  ││
│  │                               │                             ││
│  │   ┌─────┬─────┬─────┐        │   ┌─────────────────────┐   ││
│  │   │ TODO│IN   │DONE │        │   │ Search              │   ││
│  │   │     │PROG │     │        │   ├─────────────────────┤   ││
│  │   ├─────┼─────┼─────┤        │   │ Overview            │   ││
│  │   │Card │Card │Card │        │   ├─────────────────────┤   ││
│  │   │Card │Card │     │        │   │ Active Agents       │   ││
│  │   │Card │     │     │        │   ├─────────────────────┤   ││
│  │   └─────┴─────┴─────┘        │   │ System Log          │   ││
│  │                               │   └─────────────────────┘   ││
│  └───────────────────────────────┴─────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## bits-ui Component Mapping

| UI Element | bits-ui Component | Notes |
|------------|------------------|-------|
| Header Menu | `Menubar` | View options, Actions |
| View Toggle | `Tabs` | hub-view / board-view |
| Task Card | `Card` (custom) | With color-coded border |
| Card Actions | `DropdownMenu` | Edit, Delete, etc. |
| Settings Panel | `Tabs` + `Accordion` | ⚠️ In Sidebar, NICHT als Dialog |
| Settings Sections | `Accordion` | Appearance, Editor, Git, etc. |
| Form Inputs | `Label`, `Select`, `Checkbox`, `Switch` | |
| Font Size Slider | `Slider` | 14px default |
| Scrollable Areas | `ScrollArea` | Agent list, System log |
| Tooltips | `Tooltip` | On icons, status indicators |
| Separators | `Separator` | Between sections |
| Buttons | `Button` | Primary (violet), Secondary (outline), Destructive (red) |

---

## File Structure

```
frontend/src/
├── lib/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.svelte
│   │   │   ├── Sidebar.svelte
│   │   │   └── MainContent.svelte
│   │   ├── kanban/
│   │   │   ├── Board.svelte
│   │   │   ├── Column.svelte
│   │   │   └── TaskCard.svelte
│   │   ├── panel/
│   │   │   ├── FunctionPanel.svelte
│   │   │   ├── SearchBar.svelte
│   │   │   ├── ProjectOverview.svelte
│   │   │   ├── AgentList.svelte
│   │   │   └── SystemLog.svelte
│   │   ├── settings/
│   │   │   ├── SettingsDialog.svelte
│   │   │   └── sections/
│   │   │       ├── AppearanceSection.svelte
│   │   │       ├── EditorSection.svelte
│   │   │       ├── GitSection.svelte
│   │   │       ├── NotificationsSection.svelte
│   │   │       └── PrivacySection.svelte
│   │   └── ui/
│   │       └── (bits-ui wrapper components if needed)
│   ├── stores/
│   │   ├── tasks.svelte.ts
│   │   ├── agents.svelte.ts
│   │   └── settings.svelte.ts
│   ├── services/
│   │   ├── api.ts
│   │   └── sse.ts
│   └── types/
│       ├── task.ts
│       └── agent.ts
├── routes/
│   ├── +layout.svelte
│   ├── +page.svelte
│   └── settings/
│       └── +page.svelte
└── app.css                    # ← Central CSS (Design Tokens)
```

---

## Implementation Phases

### Phase 1: Foundation
1. ✅ Design tokens in `app.css`
2. ✅ Base layout structure
3. ✅ Header component with Menubar

### Phase 2: Kanban Board
1. Board component with 3 columns
2. TaskCard component with color-coded types
3. Basic drag & drop (später)

### Phase 3: Function Panel
1. Sidebar layout
2. Search bar
3. Project overview accordion
4. Agent list with status
5. System log (ScrollArea)

### Phase 4: Settings
1. Settings Dialog
2. Accordion sections
3. Form controls (Select, Switch, Slider, Checkbox)

### Phase 5: Live Updates
1. SSE client service
2. Task state sync
3. Agent status updates

---

## Key bits-ui Patterns

### Button Variants

```svelte
<!-- Primary (violet) -->
<Button.Root class="bg-violet-500 hover:bg-violet-600 text-white">
  CONFIRM ACTION
</Button.Root>

<!-- Secondary (outline) -->
<Button.Root class="border border-zinc-700 hover:bg-zinc-800">
  VIEW DETAILS
</Button.Root>

<!-- Destructive (red) -->
<Button.Root class="bg-red-500/20 text-red-400 hover:bg-red-500/30">
  DELETE
</Button.Root>

<!-- Icon only -->
<Button.Root class="size-10 border border-zinc-700">
  <GearIcon />
</Button.Root>
```

### Task Card Structure

```svelte
<div class="border-l-4 border-l-[var(--task-color)] border border-zinc-700 bg-zinc-900 p-4">
  <div class="flex justify-between">
    <span class="text-xs text-zinc-500">#{task.id}</span>
    <DropdownMenu.Root><!-- actions --></DropdownMenu.Root>
  </div>
  <h3 class="text-sm font-medium mt-2">{task.title}</h3>
</div>
```

---

*Created: 2026-01-13*
*Updated: 2026-01-13 (Sidebar-First Architecture Rule)*
