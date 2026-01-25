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
| Agent Logs Panel | 🔴 | #8, #30 | Zeigt keine Runs an |
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
| Overview Tab | 🔴 | #29 | Keine Funktion - entfernen oder sinnvoll nutzen |
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

### #25 - Erweiterte Task-Definition ✅ KONZEPT

**Severity:** High
**Status:** Konzept abgeschlossen (2026-01-24)
**Created:** 2026-01-24
**Design:** `dev/DESIGN-TASK-DELEGATION.md`

**Lösung (Phase 11A - Konzept):**

Tasks bekommen neue optionale Felder für erweiterte Konfiguration:

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `sandbox_dir` | String (auto) | Isolierter Arbeitsordner: `output/{task_id}/` |
| `target_path` | String? | Finale Destination nach Completion |
| `read_paths` | JSON | Erlaubte Lese-Pfade für Agent |
| `allowed_mcps` | JSON | Erlaubte MCPs (Default aus Registry) |
| `template` | String? | Template-Name oder Inline-MD |
| `source` | String | Herkunft: `ui`, `mcp`, `api` |

**Workflow:**
1. Agent arbeitet immer in `sandbox_dir` (isoliert)
2. Bei Task-Completion: wenn `target_path` gesetzt → Dateien werden kopiert
3. Kein `target_path` → Ergebnis bleibt in `output/{task_id}/`

**Nächster Schritt:** Phase 11B - Backend Implementation

---

### #26 - Projektstruktur & Standardpfade ✅ KONZEPT

**Severity:** High
**Status:** Konzept abgeschlossen (2026-01-24)
**Created:** 2026-01-24
**Design:** `dev/DESIGN-TASK-DELEGATION.md`

**Lösung (Phase 11A - Konzept):**

Statt komplexer Projektstruktur → **Task-basierter Ansatz**:
- Jeder Task definiert seinen eigenen Kontext (read_paths, MCPs)
- Kein festes "Projekt-Root" - Tasks sind unabhängig
- MCP Registry in `.kanban/mcps.yaml` für verfügbare MCPs

**MCP Registry:**
```yaml
mcps:
  filesystem:
    enabled: true
    command: "python"
    args: ["-m", "src.mcp_servers.filesystem.server"]
  perplexity:
    enabled: true
    command: "npx"
    args: ["-y", "@anthropic/perplexity-mcp"]

defaults:
  allowed_mcps: ["filesystem", "perplexity"]
  template: "research"
```

**Templates:**
```
templates/
├── research.md   # Standard-Recherche
├── dev.md        # Development-Tasks
└── notes.md      # Einfache Notizen
```

**Nächster Schritt:** Phase 11C - MCP Registry Implementation

---

### #27 - Klickbare Pfade + Default Editor 🔵 NEW

**Severity:** Low
**Status:** Offen
**Created:** 2026-01-25

**Description:**
Sandbox- und Target-Pfade im TaskEditor sollen klickbar sein, um den Ordner direkt im Editor zu öffnen.

**Requirements:**
1. Settings: Default Editor konfigurierbar (User präferiert: **Zed**)
2. TaskEditor: Pfade als klickbare Links
3. Backend: Endpoint zum Öffnen von Pfaden im Editor (`POST /api/open-in-editor`)
4. Unterstützte Editoren: `zed`, `code`, `cursor`, `sublime`

**Command-Patterns:**
```bash
zed <path>          # Zed
code <path>         # VS Code
cursor <path>       # Cursor
subl <path>         # Sublime Text
```

**Phase:** 11F (Frontend Anpassungen)

---

### #28 - Task-Summary im Board 🟡 KONZEPT NÖTIG

**Severity:** Medium
**Status:** Offen - Konzeptarbeit nötig
**Created:** 2026-01-25

**Description:**
Tasks sollen eine strukturierte Zusammenfassung des Agent-Ergebnisses im Kanban-Board anzeigen, ohne dass man die komplette Datei öffnen muss.

**Use Case:**
- Agent arbeitet an Task → erstellt Dateien in Sandbox
- Zusätzlich: Agent erstellt eine **Summary** (strukturiert)
- Summary wird im TaskEditor/Board angezeigt

**Mögliche Summary-Felder:**
- Status: Erfolgreich / Teilweise / Fehlgeschlagen
- Erledigte Schritte (Checklist)
- Kernerkenntnisse (Bullet Points)
- Generierte Dateien (Liste mit Größe)
- Nächste Schritte / Offene Punkte

**Konzept-Fragen:**
1. Format: JSON-Schema oder Markdown mit Frontmatter?
2. Wo speichern: In DB (`task.summary`) oder als `summary.json` in Sandbox?
3. Wie generieren: Agent-Prompt-Template oder Post-Processing?
4. UI: Collapsible Section im TaskEditor oder eigenes Panel?

**Abhängigkeiten:**
- Phase 11D (Templates) - Summary-Template definieren
- Agent-Prompt muss Summary-Format kennen

**Phase:** Konzept → dann 11F oder eigene Phase

---

### #29 - Overview Tab ohne Funktion 🔴 ENTSCHEIDUNG NÖTIG

**Severity:** Low
**Status:** Offen - Entscheidung nötig
**Created:** 2026-01-25

**Description:**
Das Overview Tab (Tachometer-Icon) in der Sidebar hat aktuell keine Funktion. Der Bereich ist komplett leer.

**Optionen:**
1. **Entfernen** - Tab komplett entfernen, vereinfacht UI
2. **Dashboard** - Task-Statistiken, Agent-Performance, etc.
3. **Quick Actions** - Häufig genutzte Aktionen (z.B. letzter Task, aktive Agents)
4. **Status Overview** - Übersicht aller laufenden/geplanten Tasks

**Entscheidung:** In nächster Session klären - entfernen vs. sinnvoll nutzen

**Phase:** UI Cleanup oder 11F

---

### #30 - Agent Log Panel zeigt keine Runs an 🔴 BUG

**Severity:** Medium
**Status:** Offen - Bug
**Created:** 2026-01-25

**Description:**
Das Agent Log Panel (Agents Tab) zeigt "No agent activity yet", obwohl Agent Runs existieren sollten.

**Symptom:**
- Panel zeigt immer "No agent activity yet"
- Nach Agent-Run wird nichts angezeigt
- Historische Runs fehlen

**Mögliche Ursachen:**
1. API-Endpoint `/api/agent/runs` liefert keine Daten
2. Frontend lädt Runs nicht korrekt
3. DB wurde zurückgesetzt (Phase 11B) - aber auch neue Runs fehlen
4. SSE-Events für Agent-Logs nicht verbunden

**Zu prüfen:**
- `GET /api/agent/runs` Response
- AgentLogsPanel.svelte - Datenladung
- SSE Event-Subscription für agent_log

**Phase:** Bugfix - hohe Priorität

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

### ✅ Erledigt (18 Issues)
#1, #3, #4, #6, #7, #8, #14, #15, #16, #17, #18, #19, #20, #21, #23, #24, #25 (Konzept), #26 (Konzept)

### 🔧 Implementation ausstehend (2 Issues)

| Prio | # | Issue | Status | Phase |
|------|---|-------|--------|-------|
| 1 | #25 | Erweiterte Task-Definition | Konzept ✅, Implementation ausstehend | 11B |
| 2 | #26 | MCP Registry & Templates | Konzept ✅, Implementation ausstehend | 11C-D |

### 🔴 Offen (5 Issues)

| Prio | # | Issue | Severity | Phase |
|------|---|-------|----------|-------|
| 3 | #22 | Projekt-Management | HIGH | Backlog |
| 4 | #27 | Klickbare Pfade + Default Editor | LOW | 11F |
| 5 | #28 | Task-Summary im Board | MEDIUM | Konzept |
| 6 | #29 | Overview Tab ohne Funktion | LOW | UI Cleanup |
| 7 | #30 | Agent Log Panel Bug | MEDIUM | Bugfix |

### 📋 Nächste Schritte
```
Phase 11B: Backend Task-Model Erweiterung (#25)
Phase 11C: MCP Registry (.kanban/mcps.yaml)
Phase 11D: Templates (templates/)
Phase 11E: Kanban MCP API Update
Phase 11F: Frontend Anpassungen
Phase 12: Trilium Integration
```

---

## Summary

| Category | Count |
|----------|-------|
| ✅ Fixed/Closed | 16 |
| ✅ Konzept abgeschlossen | 2 |
| 🔧 Implementation ausstehend | 2 |
| 🔴 Open (High) | 1 |
| 🟡 Open (Medium) | 2 |
| 🔵 Open (Low) | 2 |
| **Total Issues** | **23** |

---

*Last Updated: 2026-01-25*
