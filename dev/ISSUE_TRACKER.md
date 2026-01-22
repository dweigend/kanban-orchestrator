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
| Tasks im Board anzeigen | 🟢 | #6 | ✅ Fixed: Schema status mapping (lowercase → UPPERCASE) |
| Edit Task | ⚪ | | Nicht getestet (Tasks nicht sichtbar) |
| Delete Task | ⚪ | | Nicht getestet (Tasks nicht sichtbar) |
| Drag & Drop (Column) | 🟢 | | Tasks zwischen Spalten verschieben funktioniert |
| Drag & Drop (Reorder) | 🔴 | #14 | Cards können nicht innerhalb einer Spalte sortiert werden |
| Plus-Buttons (Column) | 🟢 | #7 | ✅ Fixed: handleAddTask() + onAddTask prop |
| Task Types Visual | ⚪ | | research/dev/notes/neutral |
| Status Labels | 🟢 | | Schema-driven, funktioniert |

### Agent System

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Agent Runs (API) | 🟢 | | 2 completed runs in DB |
| Agent Logs Panel | 🟢 | #8 | ✅ Fixed: Historical runs now displayed |
| Run Agent Button | 🟢 | | Funktioniert |
| Agent Autostart | 🟡 | #16 | Kein Autostart bei Task-Erstellung (UX-Frage) |
| Agent Logs Streaming | ⚪ | | SSE nicht getestet |
| Task Result Display | ⚪ | | Nicht getestet |

### Settings

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Settings UI | 🔴 | #15 | Hängt sich nach erster Änderung auf |
| Font Family | 🟢 | #1 | ✅ localStorage + CSS Custom Properties |
| Font Size | 🟢 | #1 | ✅ localStorage + CSS Custom Properties |
| Editor Config Live | 🔴 | #15 | Erste Änderung funktioniert, danach freeze |
| Save Button | 🟢 | #1 | ✅ Saves to localStorage + toast |
| Persistence | 🟢 | #1 | ✅ Settings bleiben nach Reload |
| Backend Settings | 🔴 | #3 | Not connected to UI |

### UI Components

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Sidebar Tabs | 🟢 | | Overview/Agents/Settings wechseln |
| Hide/Show Sidebar | 🟢 | | Button funktioniert |
| Search Bar | 🔴 | #4, #23 | Konzeptionell unklar, nicht implementiert |
| Hub/Board View Toggle | 🟢 | #18 | **ENTFERNEN** - nur 1 View nötig |
| Breadcrumb "vibe-kanban/hub-view" | 🟢 | #19 | **ENTFERNEN** - unnütz |
| Project Menu | 🔴 | #9, #22 | Konzeptionell überarbeiten (eigene Session) |
| Project Overview Section | 🟢 | #20 | **ENTFERNEN** - Mock Data, nicht MVP |
| System Logs Section | 🟢 | #21 | **ENTFERNEN** - Mock Data, nicht MVP |
| Card Context Menu | 🟡 | #17 | Redundant → Icons direkt auf Card |
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

### #14 - Card Reihenfolge nicht änderbar 🔴

**Severity:** Medium
**File:** `frontend/src/lib/components/kanban/Board.svelte`, `Column.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Cards lassen sich zwischen Spalten verschieben (Drag & Drop funktioniert)
- Cards können NICHT innerhalb einer Spalte umsortiert werden
- Reihenfolge bleibt immer gleich (vermutlich nach created_at)

**Root Cause:** Kein `position`/`order` Feld im Task-Model, keine Reorder-Logik im Frontend

**Steps to Reproduce:**
1. Erstelle mehrere Tasks in "To Do"
2. Versuche Task 3 über Task 1 zu ziehen
3. Task springt zurück an ursprüngliche Position

---

### #15 - Editor Config Freeze nach erster Änderung 🔴

**Severity:** High
**File:** `frontend/src/lib/stores/settings.svelte.ts`, `SettingsPanel.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Erste Änderung an Font Family oder Font Size funktioniert
- Danach hängt sich die Settings-UI auf
- Weitere Slider/Dropdown-Interaktionen werden nicht mehr verarbeitet

**Root Cause:** Vermutlich unendliche $effect Loop durch gegenseitige reaktive Updates

**Steps to Reproduce:**
1. Settings öffnen
2. Font Size von 14px auf 18px ändern → funktioniert
3. Font Size erneut ändern (z.B. 20px) → UI reagiert nicht mehr

---

### #16 - Kein Agent-Autostart bei Task-Erstellung 🟡

**Severity:** Medium
**Verified:** ✅ 2026-01-22

**Description:**
- Task anlegen → Agent startet nicht automatisch
- User muss manuell "Run Agent" klicken

**Frage:** Soll Agent automatisch starten bei Task-Erstellung? (UX-Entscheidung)

---

### #17 - Card-Menü redundant / UX-Überarbeitung 🟡

**Severity:** Medium
**File:** `frontend/src/lib/components/kanban/TaskCard.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Aktuelles Menü: Edit, Open, Run Agent, Delete
- "Edit" und "Open" sind identisch (öffnen beide TaskEditor)
- **Vorschlag:** Menü entfernen, stattdessen Icons direkt auf Card:
  - ▶️ Run Agent
  - 🗑️ Delete
  - Click auf Card → Edit

---

### #18 - Hub View / Board View Toggle entfernen 🟢

**Severity:** Low (Quick Win)
**File:** `frontend/src/lib/components/layout/Header.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Toggle zwischen "Hub View" und "Board View"
- Beide Views zeigen identische UI
- Nur ein Kanban Board View wird benötigt
- **Action:** Toggle komplett entfernen

---

### #19 - Breadcrumb "vibe-kanban / hub-view" entfernen 🟢

**Severity:** Low (Quick Win)
**File:** `frontend/src/lib/components/layout/Header.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- Neben Logo: "vibe-kanban / hub-view" Text
- Unnütz, kein Mehrwert
- **Action:** Entfernen

---

### #20 - Projekt-Overview Section entfernen 🟢

**Severity:** Low (Quick Win)
**File:** `frontend/src/lib/components/panel/FunctionPanel.svelte`, `OverviewPanel.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- "OVERVIEW" mit "vibe-kanban" Dropdown
- Expandiert zu Mock-Daten (Status, Tags)
- Nicht implementiert, für MVP nicht relevant
- **Action:** Section entfernen, Sidebar verschlanken

---

### #21 - System Logs Section entfernen 🟢

**Severity:** Low (Quick Win)
**File:** `frontend/src/lib/components/panel/FunctionPanel.svelte`
**Verified:** ✅ 2026-01-22

**Description:**
- "SYSTEM LOG" mit Mock-Daten
- "Python Interpreter connected", "PostgreSQL timeout" etc.
- Nicht mit Backend verbunden
- **Action:** Section entfernen, Sidebar verschlanken

---

### #22 - Projekt-Management konzeptionell überarbeiten 🔴

**Severity:** High (Eigene Session)
**Verified:** ✅ 2026-01-22

**Description:**
- Projekt-Menü funktioniert nicht (Open/New/Import)
- Unklar wie Projekte gemanagt werden sollen
- Backend `/api/projects` existiert aber ist leer
- **Benötigt:**
  1. Backend-Recherche: Wie werden Projekte gespeichert?
  2. Konzept-Entwicklung mit User
  3. Vermutlich eigene Session

**Fragen:**
- Was ist ein "Projekt" im Kontext des Orchestrators?
- Wie verhält sich Projekt zu Git-Repo?
- Multi-Projekt oder Single-Projekt?

---

### #23 - Search / Knowledge Base konzeptionell klären 🔴

**Severity:** High (Eigene Session)
**Verified:** ✅ 2026-01-22

**Description:**
- "Search knowledge base..." Placeholder im Input
- Keine Implementierung (nur console.log)
- **Konzeptionelle Fragen:**
  - Was IST die Knowledge Base?
  - Wo wird sie eingerichtet?
  - Ist das Teil des Kanban-Orchestrators oder separates System?
  - Gehört Search überhaupt in dieses Tool?

**Vermutung:** Knowledge Base und Kanban Board sind zwei unterschiedliche Dinge. Evtl. Überbleibsel aus erster Planung.

**Benötigt:** Systematische Analyse aller offenen Features gegen Original-Konzept

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
| 🔴 HIGH | 6 |
| 🟡 MEDIUM | 4 |
| 🟢 LOW (Quick Wins) | 4 |
| 🟡 LOW (Cleanup) | 4 |
| **Total** | **23** |

---

## Priority Matrix

### ✅ Erledigt
- ~~#6 - Tasks im Board anzeigen~~ ✅
- ~~#7 - Plus-Buttons funktional~~ ✅
- ~~#8 - Agent Logs anzeigen~~ ✅
- ~~#1 - Settings persistent~~ ✅

### 🚀 Quick Wins (sofort umsetzbar)
- **#18** - Hub/Board View Toggle entfernen
- **#19** - Breadcrumb "vibe-kanban / hub-view" entfernen
- **#20** - Projekt-Overview Section entfernen
- **#21** - System Logs Section entfernen

### 🔧 Bugs (Prio 1)
- **#15** - Editor Config Freeze
- **#14** - Card Reihenfolge nicht änderbar

### 🎨 UX Verbesserungen (Prio 2)
- **#17** - Card-Menü → Icons
- **#16** - Agent-Autostart (UX-Entscheidung)

### 📋 Eigene Sessions (Konzeptarbeit)
- **#22** - Projekt-Management (Backend + Konzept)
- **#23** - Search / Knowledge Base (Konzept-Abgleich)
- **#9** - Projekt-Menü (abhängig von #22)
- **#4** - Search (abhängig von #23)

### 🧹 Cleanup (niedrige Prio)
- #3, #5, #10, #11, #12, #13 - Mock Data / Backend Settings

---

*Last Updated: 2026-01-22*
