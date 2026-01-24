# Issue Tracker

Lebendes Dokument zur Erfassung des Projektstatus. Wird in jeder Session aktualisiert.

---

## Status Legend

- 🟢 **Functional** - Works as expected
- 🟡 **Under Development** - Partially implemented, known limitations
- 🔴 **Buggy** - Broken or critical issues
- ⚪ **Not Tested** - Needs verification
- ✅ **Fixed** - Issue resolved

---

## Features

### Task Management

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Create Task (API) | 🟢 | | POST /api/tasks → 201 |
| Create Task (UI) | 🟢 | | TaskEditor funktioniert |
| Tasks im Board anzeigen | 🟢 | #6 ✅ | Fixed: Schema status mapping |
| Edit Task | 🟢 | | Click auf Card öffnet Editor |
| Delete Task | 🟢 | #17 ✅ | Delete Icon auf Card |
| Drag & Drop (Column) | 🟢 | | Tasks zwischen Spalten verschieben |
| Drag & Drop (Reorder) | 🔴 | #14 | Cards nicht innerhalb Spalte sortierbar |
| Task Types Visual | 🟢 | | research/dev/notes/neutral |
| Status Labels | 🟢 | | Schema-driven |

### Agent System

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Agent Runs (API) | 🟢 | | Completed runs in DB |
| Agent Logs Panel | 🟢 | #8 ✅ | Historical runs displayed |
| Run Agent Button | 🟢 | #17 ✅ | Icon direkt auf Card |
| Agent Autostart | 🟡 | #16 | Kein Autostart (UX-Frage) |
| Agent Logs Streaming | ⚪ | | SSE nicht getestet |

### Settings

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Settings UI | 🟢 | #15 ✅ | Fixed: untrack() in +layout.svelte |
| Font Family | 🟢 | #1 ✅ | Live-Änderung funktioniert |
| Font Size | 🟢 | #1 ✅ | Live-Änderung funktioniert |
| Save Button | 🟢 | | Saves to localStorage + toast |
| Persistence | 🟢 | | Settings bleiben nach Reload |
| Backend Settings | 🔴 | #3 | Not connected to UI |

### UI Components

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Sidebar Tabs | 🟢 | | Overview/Agents/Settings |
| Hide/Show Sidebar | 🟢 | | Button funktioniert |
| Search Bar | ✅ | #4, #23 | **ENTFERNT** |
| Hub/Board View Toggle | ✅ | #18 | **ENTFERNT** |
| Breadcrumb | ✅ | #19 | **ENTFERNT** |
| Project Menu | 🔴 | #9, #22 | Konzeptionell überarbeiten |
| Project Overview Section | ✅ | #20 | **ENTFERNT** |
| System Logs Section | ✅ | #21 | **ENTFERNT** |
| Card Icons (Run/Delete) | 🟢 | #17 ✅ | Context Menu ersetzt |
| User Avatar "DW" | 🟡 | #12 | Nur StaticText |
| Plus-Buttons (Columns) | ✅ | | **ENTFERNT** (New Task via Header) |

### Backend Communication

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| GET /api/tasks | 🟢 | | Tasks in DB |
| POST /api/tasks | 🟢 | | 201 Created |
| GET /api/schema/enums | 🟢 | | Labels korrekt |
| GET /api/agent/runs | 🟢 | | Runs returned |
| GET /api/projects | 🟢 | | Leer aber funktional |
| SSE Events | ⚪ | | Nicht vollständig getestet |

---

## Known Issues (Offen)

### #3 - Frontend-Backend Settings Gap 🔴

**Severity:** Low
**Status:** Offen

**Description:**
- Frontend: Font, Notifications, Analytics (localStorage)
- Backend: Git config, Agent config (`/api/settings/schema`)
- Keine Verbindung zwischen UI und Backend-Settings

---

### #14 - Card Reihenfolge nicht änderbar 🔴

**Severity:** High
**Status:** Offen
**Verified:** ✅ 2026-01-23

**Description:**
- Cards lassen sich zwischen Spalten verschieben (Status-Änderung funktioniert)
- Cards können NICHT innerhalb einer Spalte umsortiert werden
- Reihenfolge bleibt immer gleich (sortiert nach `created_at`)
- User erwartet: Drag & Drop zum Priorisieren innerhalb einer Spalte

**User Story:**
> "Ich möchte die Reihenfolge der Karten im Kanban-Board per Drag & Drop ändern können."

**Root Cause:**
- Kein `position`/`order` Feld im Task-Model (Backend)
- Keine Reorder-Logik im Frontend (nur Status-Update bei Drop)

**Required Changes:**

1. **Backend:**
   - Task-Model: `position: int` Feld hinzufügen
   - Migration: Default position = created_at timestamp oder auto-increment
   - PATCH `/api/tasks/{id}`: position update
   - GET `/api/tasks`: Sortierung nach `status` dann `position`

2. **Frontend:**
   - `Column.svelte`: Reorder innerhalb Spalte erkennen
   - `Board.svelte`: Position-Update API call
   - Optimistic UI update für flüssiges UX

**Acceptance Criteria:**
- [ ] Cards können per Drag & Drop innerhalb einer Spalte sortiert werden
- [ ] Neue Reihenfolge bleibt nach Page Reload erhalten
- [ ] Drag zwischen Spalten funktioniert weiterhin (Status-Änderung)

---

### #16 - Kein Agent-Autostart bei Task-Erstellung 🟡

**Severity:** Low
**Status:** UX-Entscheidung offen

**Description:**
- Task anlegen → Agent startet nicht automatisch
- User muss manuell "Run Agent" klicken

---

### #22 - Projekt-Management konzeptionell überarbeiten 🔴

**Severity:** High (Eigene Session)
**Status:** Konzeptarbeit nötig

**Description:**
- Projekt-Menü funktioniert nicht
- Backend `/api/projects` existiert aber ist leer
- Konzept-Entwicklung mit User nötig

---

## Erledigte Issues ✅

| # | Issue | Fix | Session |
|---|-------|-----|---------|
| #1 | Settings Not Persistent | localStorage + CSS Custom Properties | 2026-01-22 |
| #4 | Search Not Implemented | SearchBar komplett entfernt | 2026-01-23 |
| #6 | Tasks Not Visible | Schema status mapping (lowercase → UPPERCASE) | 2026-01-22 |
| #7 | Plus-Buttons | handleAddTask() + onAddTask prop | 2026-01-22 |
| #8 | Agent Logs "No activity" | Historical runs jetzt angezeigt | 2026-01-22 |
| #15 | Settings Freeze | untrack() in +layout.svelte | 2026-01-23 |
| #17 | Card-Menü redundant | Icons direkt auf Card (Run Agent, Delete) | 2026-01-23 |
| #18 | Hub/Board View Toggle | Entfernt | 2026-01-23 |
| #19 | Breadcrumb | Entfernt | 2026-01-23 |
| #20 | Project Overview Section | Entfernt | 2026-01-23 |
| #21 | System Logs Section | Entfernt | 2026-01-23 |
| #23 | Search/Knowledge Base | SearchBar entfernt (Konzept unklar) | 2026-01-23 |

---

## Priority Matrix

### ✅ Erledigt (12 Issues)
#1, #4, #6, #7, #8, #15, #17, #18, #19, #20, #21, #23

### 🔧 Offen (4 Issues)

| Prio | # | Issue | Severity |
|------|---|-------|----------|
| 1 | #14 | Card Reorder in Columns | HIGH |
| 2 | #22 | Projekt-Management (Konzept) | HIGH |
| 3 | #3 | Backend Settings in UI | LOW |
| 4 | #16 | Agent-Autostart (UX) | LOW |

### 📋 Abhängig von #22
- #9 - Projekt-Menü

---

## Session Log

### 2026-01-23 - Settings Fix + UI Cleanup

**Fixes:**
- ✅ #15 - Settings Freeze (untrack() fix)
- ✅ #4, #23 - SearchBar entfernt
- ✅ Plus-Buttons aus Spalten entfernt

**Technical Details:**
- Root Cause #15: `$effect` in `+layout.svelte` wurde bei jeder State-Änderung re-triggered
- Fix: `untrack()` um die Initialisierung
- bits-ui Pattern: Lokaler State + onValueChange Handler

### 2026-01-22 - Systematic Browser Testing

**Method:** Chrome DevTools MCP + curl API tests

**Tests Performed:**
- ✅ Task Create Flow (UI + API)
- ✅ Task Display in Board
- ✅ Plus-Buttons in Columns
- ✅ Settings Panel
- ✅ Agents Panel
- ✅ All UI Components

**Key Finding:**
Backend funktioniert. Frontend-Bugs hauptsächlich in Reaktivität und State-Management.

---

## Summary

| Category | Count |
|----------|-------|
| ✅ Fixed | 12 |
| 🔴 Open (High/Medium) | 2 |
| 🟡 Open (Low/UX) | 2 |
| **Total Issues** | **16** |

---

*Last Updated: 2026-01-23*
