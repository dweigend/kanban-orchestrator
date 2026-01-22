# Issue Tracker

Lebendes Dokument zur Erfassung des Projektstatus. Wird in jeder Session aktualisiert.

---

## Status Legend

- 🟢 **Functional** - Works as expected
- 🟡 **Under Development** - Partially implemented, known limitations
- 🔴 **Buggy** - Broken or critical issues
- ⚪ **Not Tested** - Needs verification

---

## Features

### Task Management

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Create Task (API) | 🟢 | | POST /api/tasks → 201 |
| Create Task (UI) | 🟢 | | TaskEditor funktioniert |
| Tasks im Board anzeigen | 🔴 | #6 | Board zeigt "No tasks" trotz 9 Tasks in DB |
| Edit Task | ⚪ | | Nicht getestet (Tasks nicht sichtbar) |
| Delete Task | ⚪ | | Nicht getestet (Tasks nicht sichtbar) |
| Drag & Drop | ⚪ | | Nicht getestet (Tasks nicht sichtbar) |
| Plus-Buttons (Column) | 🔴 | #7 | Keine onClick Handler |
| Task Types Visual | ⚪ | | research/dev/notes/neutral |
| Status Labels | 🟢 | | Schema-driven, funktioniert |

### Agent System

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Agent Runs (API) | 🟢 | | 2 completed runs in DB |
| Agent Logs Panel | 🔴 | #8 | Zeigt "No agent activity" |
| Run Agent Button | ⚪ | | Nicht getestet (Tasks nicht sichtbar) |
| Agent Logs Streaming | ⚪ | | SSE nicht getestet |
| Task Result Display | ⚪ | | Nicht getestet |

### Settings

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Settings UI | 🟢 | | Dropdowns, Sliders, Switches funktionieren |
| Font Family | 🔴 | #1 | UI only, not persisted |
| Font Size | 🔴 | #1 | UI only, not persisted |
| Line Numbers | 🔴 | #1 | UI only, not persisted |
| Word Wrap | 🔴 | #1 | UI only, not persisted |
| Save Button | 🔴 | #1 | Only console.log |
| Persistence | 🔴 | #1 | No localStorage/backend |
| Appearance/Theme | 🟡 | #2 | "Coming soon" placeholder |
| Backend Settings | 🔴 | #3 | Not connected to UI |

### UI Components

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Sidebar Tabs | 🟢 | | Overview/Agents/Settings wechseln |
| Hide/Show Sidebar | 🟢 | | Button funktioniert |
| Search Bar | 🔴 | #4 | Nur console.log |
| Hub/Board View Toggle | 🔴 | #10 | Nur URL ändert sich, UI identisch |
| Project Menu | 🔴 | #9 | Open/New/Import ohne Funktion |
| "View All" Button | 🔴 | #11 | Keine Aktion |
| User Avatar "DW" | 🟡 | #12 | Nur StaticText, kein User-System |

### Backend Communication

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| GET /api/tasks | 🟢 | | 9 Tasks in DB |
| POST /api/tasks | 🟢 | | 201 Created |
| GET /api/schema/enums | 🟢 | | Labels korrekt |
| GET /api/agent/runs | 🟢 | | 2 Runs returned |
| GET /api/projects | 🟢 | | Leer aber funktional |
| SSE Events | ⚪ | | Nicht vollständig getestet |
| Task Store Update | 🔴 | #6 | Frontend lädt Tasks nicht |

---

## Known Issues

### #1 - Settings Not Persistent 🔴

**Severity:** High
**File:** `frontend/src/lib/components/panel/SettingsPanel.svelte:31-42`
**Verified:** ✅ 2026-01-22

**Description:**
`handleSave()` function only logs to console. No actual persistence.

**Steps to Reproduce:**
1. Open Settings tab
2. Change any setting (e.g., Word Wrap)
3. Click "Save"
4. Console shows: `Settings saved: JSHandle@object`
5. Refresh page
6. Settings are reset to defaults

**Expected:** Settings persist across sessions
**Actual:** Settings lost on page reload

---

### #2 - Appearance Section Placeholder 🟡

**Severity:** Low
**File:** `frontend/src/lib/components/panel/SettingsPanel.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
Appearance section shows "Theme and visual settings coming soon..." - no actual controls.

---

### #3 - Frontend-Backend Settings Gap 🔴

**Severity:** High
**Verified:** ✅ 2026-01-22

**Description:**
- Frontend has UI for: Font, Notifications, Analytics
- Backend serves only: Git config, Agent config (`/api/settings/schema`)
- No connection between them

**Impact:** Backend settings (max_turns, model, auto_checkpoint) cannot be configured from UI.

---

### #4 - Search Not Implemented 🔴

**Severity:** Medium
**File:** `frontend/src/routes/+page.svelte:227`
**Verified:** ✅ 2026-01-22

**Description:**
`handleSearch()` only logs to console: `Search: test search`
No actual search functionality.

---

### #5 - Mock Data in System Log 🟡

**Severity:** Low
**Files:**
- `frontend/src/routes/+page.svelte:31-54` - Hardcoded mock agents
- `frontend/src/routes/+page.svelte:57-77` - Hardcoded system logs
**Verified:** ✅ 2026-01-22

**Description:**
System Log shows hardcoded mock data:
- "Python Interpreter connected successfully"
- "Web Search: Tailwind CSS high contrast"
- "PostgreSQL: Connection timeout (5432)"
- "Waiting for changes..."

---

### #6 - Tasks Not Visible in Board 🔴

**Severity:** CRITICAL
**Files:**
- `frontend/src/routes/+page.svelte`
- `frontend/src/lib/components/kanban/Board.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Task erstellen → Toast "Task created" erscheint
- Board zeigt weiterhin "No tasks" in allen Columns
- Backend hat 9 Tasks in DB (`curl http://localhost:8000/api/tasks`)
- Network Tab zeigt POST 201 success

**Root Cause:** Frontend lädt Tasks nicht bei Page Load / aktualisiert Board nicht nach Create

**Steps to Reproduce:**
1. Open app at http://localhost:5173/
2. Click "New Task"
3. Fill in title, click "Create Task"
4. Toast "Task created" appears
5. Board still shows "No tasks" everywhere

---

### #7 - Plus-Buttons Without Function 🔴

**Severity:** CRITICAL
**File:** `frontend/src/lib/components/kanban/Column.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Klick auf "+" bei To Do, In Progress, Needs Review, Done → nichts passiert
- Buttons existieren (aria-label "Add task to To Do")
- Kein onClick Handler oder Handler tut nichts

**Steps to Reproduce:**
1. Click "+" button next to any column header
2. Nothing happens

---

### #8 - Agent Logs Show "No agent activity" 🔴

**Severity:** High
**File:** `frontend/src/lib/components/panel/AgentsPanel.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Agents Panel zeigt "No agent activity"
- Backend hat 2 completed Agent Runs
- `curl http://localhost:8000/api/agent/runs` returns 2 runs

**Root Cause:** Frontend fetcht Agent Runs nicht

---

### #9 - Project Menu Without Function 🔴

**Severity:** High
**File:** `frontend/src/routes/+page.svelte` (Header)
**Verified:** ✅ 2026-01-22

**Description:**
- Project Dropdown öffnet sich
- "Open Recent", "New Project", "Import" sind klickbar
- Klick → Menu schließt sich, keine Aktion

---

### #10 - Hub View = Board View Identical 🔴

**Severity:** Medium
**File:** `frontend/src/routes/+page.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Toggle zwischen Hub View / Board View
- Nur URL ändert sich (`hub-view` → `board-view`)
- UI ist 100% identisch

---

### #11 - "View All" Button Without Function 🟡

**Severity:** Low
**Verified:** ✅ 2026-01-22

**Description:**
- "View All" Button im System Log
- Klick → nichts passiert

---

### #12 - User Avatar "DW" Without Function 🟡

**Severity:** Low
**Verified:** ✅ 2026-01-22

**Description:**
- "DW" ist nur StaticText, kein Button
- Kein User-System implementiert

---

### #13 - Overview Section Mock Data 🟡

**Severity:** Low
**Verified:** ✅ 2026-01-22

**Description:**
- "vibe-kanban" expandiert zu Mock-Daten
- Status: "V3 Redesign", Target: "High Contrast"
- Tags: React, Tailwind, MCP (hardcoded)

---

## Session Log

### 2026-01-22 - Systematic Browser Testing

**Method:** Chrome DevTools MCP + curl API tests

**Tests Performed:**
- ✅ Task Create Flow (UI + API)
- ✅ Task Display in Board
- ✅ Plus-Buttons in Columns
- ✅ Settings Panel (all sections)
- ✅ Settings Persistence (Save + Reload)
- ✅ Agents Panel
- ✅ Project Menu
- ✅ Search Field
- ✅ Hub/Board View Toggle
- ✅ Overview Section
- ✅ System Log
- ✅ Hide/Show Sidebar
- ✅ User Avatar
- ✅ Backend API Endpoints

**Key Finding:**
Backend funktioniert einwandfrei (9 Tasks, 2 Agent Runs in DB).
Frontend lädt/zeigt die Daten nicht an.

**Summary:**
| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 2 |
| 🔴 HIGH | 4 |
| 🟡 MEDIUM | 3 |
| 🟡 LOW | 4 |
| **Total** | **13** |

---

## Priority Matrix

### Sprint 1: Make App Usable
1. #6 - Tasks im Board anzeigen (CRITICAL)
2. #7 - Plus-Buttons funktional (CRITICAL)

### Sprint 2: Core Features
3. #8 - Agent Logs anzeigen (HIGH)
4. #1 + #3 - Settings persistent machen (HIGH)

### Sprint 3: UX Polish
5. #9 - Project Menu (HIGH)
6. #4 - Search (MEDIUM)
7. #10 - View Toggle (MEDIUM)

### Sprint 4: Cleanup
8. #5, #11, #12, #13 - Mock Data entfernen/kennzeichnen (LOW)

---

*Last Updated: 2026-01-22*
