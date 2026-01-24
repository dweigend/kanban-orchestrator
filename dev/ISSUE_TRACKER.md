# Issue Tracker

Lebendes Dokument zur Erfassung des Projektstatus. Wird in jeder Session aktualisiert.

---

## Status Legend

- 🟢 **Functional** - Works as expected
- 🟡 **Under Development** - Partially implemented, known limitations
- 🔴 **Buggy** - Broken or critical issues
- ⚪ **Not Tested** - Needs verification
- ✅ **Fixed** - Issue resolved
- 🚫 **Won't Fix** - Closed without implementation

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
| Drag & Drop (Reorder) | 🚫 | #14 | Won't Fix - Subtasks stattdessen |
| Task Types Visual | 🟢 | | research/dev/notes/neutral |
| Status Labels | 🟢 | | Schema-driven |
| **Subtasks/Checklists** | ✅ | #24 | FIXED - Subtasks + Expand Cards |
| **Erweiterte Task-Definition** | ⚪ | #25 | **NEU** - Geplant |

### Agent System

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Agent Runs (API) | 🟢 | | Completed runs in DB |
| Agent Logs Panel | 🟢 | #8 ✅ | Historical runs displayed |
| Run Agent Button | 🟢 | #17 ✅ | Icon direkt auf Card |
| Agent Autostart | 🚫 | #16 | Won't Fix - Expliziter Start besser |
| **Agent Task-Planung** | ✅ | #24 | FIXED - Plan/Execute Endpoints |

### Settings

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Settings UI | 🟢 | #15 ✅ | Fixed: untrack() in +layout.svelte |
| Font Family | 🟢 | #1 ✅ | Live-Änderung funktioniert |
| Font Size | 🟢 | #1 ✅ | Live-Änderung funktioniert |
| Save Button | 🟢 | | Saves to localStorage + toast |
| Persistence | 🟢 | | Settings bleiben nach Reload |
| Backend Settings | 🟢 | #3 ✅ | Connected to UI via API |

### UI Components

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Sidebar Tabs | 🟢 | | Overview/Agents/Settings |
| Hide/Show Sidebar | 🟢 | | Button funktioniert |
| Search Bar | ✅ | #4, #23 | **ENTFERNT** |
| Project Menu | 🔴 | #9, #22 | Konzeptionell überarbeiten |
| Card Icons (Run/Delete) | 🟢 | #17 ✅ | Context Menu ersetzt |
| **Expand/Collapse Cards** | ✅ | #24 | FIXED - SubtaskTree Component |

### Projektstruktur & Konfiguration

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| Projekt-Management | 🔴 | #22 | Konzept nötig |
| Standardpfade | ⚪ | #26 | **NEU** - Backend-Konfiguration |
| MCP-Zuordnung | ⚪ | #25 | **NEU** - Pro Task |
| Dateien-Zuordnung | ⚪ | #25 | **NEU** - Pro Task |
| Berechtigungen | ⚪ | #25 | **NEU** - Pro Task |
| Output Dict | ⚪ | #25 | **NEU** - Pro Task |

---

## Known Issues (Offen)

### #14 - Card Reihenfolge 🚫 WON'T FIX

**Status:** Geschlossen - durch #24 ersetzt
**Reason:** Backend-Bloat für reines UI-Feature vermeiden. Subtasks/Checklists sind sinnvoller.

---

### #22 - Projekt-Management konzeptionell überarbeiten 🔴

**Severity:** High (Eigene Session)
**Status:** Konzeptarbeit nötig

**Description:**
- Projekt-Menü funktioniert nicht
- Backend `/api/projects` existiert aber ist leer
- Konzept-Entwicklung mit User nötig

---

### #24 - Subtasks/Checklists + Expand/Collapse Cards ✅ FIXED

**Severity:** High
**Status:** Erledigt (2026-01-24)

**Implementiert:**
- ✅ Task-Model mit `parent_id` + `steps` (JSON-Array)
- ✅ `SubtaskTree.svelte` Komponente
- ✅ Expand/Collapse Cards im Board
- ✅ Tree-Struktur mit Status-Icons + Step-Counter
- ✅ Agent Plan/Execute Endpoints (`POST /api/agent/plan/{id}`, `POST /api/agent/execute/{id}`)
- ✅ Step Toggle im TaskEditor
- ✅ NEEDS_REVIEW Status mit Execute Button

---

### #25 - Erweiterte Task-Definition 🆕

**Severity:** High
**Status:** Konzeptarbeit nötig (Phase 11)
**Created:** 2026-01-24
**Depends On:** #26 (Standardpfade)

**Description:**
Tasks sollen mehr Konfiguration ermöglichen als nur Name + Beschreibung.

**Neue Felder:**
| Feld | Beschreibung |
|------|--------------|
| `mcps` | Liste von MCP-Servern, die der Agent nutzen darf |
| `files` | Dateien/Ordner, auf die der Task Zugriff hat |
| `permissions` | Berechtigungen (read/write/execute) |
| `output_dict` | Erwartetes Output-Format/Schema |

**Voraussetzungen:**
- Projektstruktur muss definiert sein (#22)
- Standardpfade müssen im Backend hinterlegt sein (#26)
- Frontend braucht Zugriff auf verfügbare MCPs/Dateien

**Benötigt Konzept-Session:**
- Wie werden MCPs registriert?
- Wie werden Dateipfade relativ zum Projekt aufgelöst?
- Wie funktioniert das Berechtigungssystem?

---

### #26 - Projektstruktur & Standardpfade 🆕

**Severity:** High
**Status:** Konzeptarbeit nötig (Phase 11)
**Created:** 2026-01-24
**Blocks:** #25

**Description:**
Backend braucht Konfiguration für Projektstruktur und Standardpfade.

**Fragen zu klären:**
- Wo liegt das Projekt-Root?
- Welche Standardordner gibt es? (src, docs, tests, etc.)
- Wie werden MCP-Server pro Projekt konfiguriert?
- Wie greift Frontend auf diese Infos zu?

**Mögliche Struktur:**
```
project/
├── .kanban/           # Orchestrator-Konfiguration
│   ├── config.yaml    # Projekt-Settings
│   ├── mcps.yaml      # Verfügbare MCPs
│   └── paths.yaml     # Standardpfade
├── src/
├── docs/
└── ...
```

---

### #3 - Frontend-Backend Settings Gap ✅ FIXED

**Severity:** Low
**Status:** Erledigt (2026-01-24)

**Lösung:**
- Backend: `GET/POST /api/settings` für Git + Agent Config
- Frontend: Settings Store + SettingsPanel mit Agent Config Section
- Speicherung: `.kanban/settings.json`

---

### #16 - Kein Agent-Autostart bei Task-Erstellung 🚫 WON'T FIX

**Severity:** Low
**Status:** Geschlossen (UX-Entscheidung)

**Entscheidung:** Kein Autostart implementieren.

**Gründe:**
1. Task-Erstellung ≠ Task-Ausführung (semantisch getrennt)
2. User behält Kontrolle über Agent-Start
3. Konsistent mit Edit → Save Workflow
4. Bei Bedarf später als optionales Setting möglich

---

## Erledigte Issues ✅

| # | Issue | Fix | Session |
|---|-------|-----|---------|
| #1 | Settings Not Persistent | localStorage + CSS Custom Properties | 2026-01-22 |
| #4 | Search Not Implemented | SearchBar komplett entfernt | 2026-01-23 |
| #6 | Tasks Not Visible | Schema status mapping | 2026-01-22 |
| #7 | Plus-Buttons | handleAddTask() + onAddTask prop | 2026-01-22 |
| #8 | Agent Logs "No activity" | Historical runs angezeigt | 2026-01-22 |
| #14 | Card Reorder | **WON'T FIX** - #24 stattdessen | 2026-01-24 |
| #15 | Settings Freeze | untrack() in +layout.svelte | 2026-01-23 |
| #17 | Card-Menü redundant | Icons auf Card | 2026-01-23 |
| #18 | Hub/Board View Toggle | Entfernt | 2026-01-23 |
| #19 | Breadcrumb | Entfernt | 2026-01-23 |
| #20 | Project Overview Section | Entfernt | 2026-01-23 |
| #21 | System Logs Section | Entfernt | 2026-01-23 |
| #23 | Search/Knowledge Base | SearchBar entfernt | 2026-01-23 |
| #16 | Agent-Autostart | **WON'T FIX** - Expliziter Start besser | 2026-01-24 |
| #3 | Backend Settings in UI | API + SettingsPanel verbunden | 2026-01-24 |
| #24 | Subtasks + Expand Cards | SubtaskTree + Plan/Execute | 2026-01-24 |

---

## Priority Matrix

### ✅ Erledigt (16 Issues)
#1, #3, #4, #6, #7, #8, #14, #15, #16, #17, #18, #19, #20, #21, #23, #24

### 🔧 Offen (3 Issues)

| Prio | # | Issue | Severity | Phase |
|------|---|-------|----------|-------|
| 1 | #26 | Projektstruktur & Standardpfade | HIGH | 11 |
| 2 | #25 | Erweiterte Task-Definition | HIGH | 11 |
| 3 | #22 | Projekt-Management (Konzept) | HIGH | 11 |

### 📋 Abhängigkeiten
```
#26 (Projektstruktur) → #25 (Erweiterte Tasks)
#22 (Projekt-Management) → #9 (Projekt-Menü)
```

---

## Summary

| Category | Count |
|----------|-------|
| ✅ Fixed/Closed | 16 |
| 🔴 Open (High) | 3 |
| 🟡 Open (Low) | 0 |
| **Total Issues** | **19** |

---

*Last Updated: 2026-01-24*
