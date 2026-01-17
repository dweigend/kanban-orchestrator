# Debug Report: Kanban Orchestrator

Zentrales Dokument zum Tracken und Fixen aller Issues.

---

## Übersicht

| Status | Count |
|--------|-------|
| 🔴 Offen | 0 |
| 🟡 In Progress | 0 |
| 🟢 Gefixt | 2 |
| ⬜ Nicht verifiziert | 2 |
| 🟠 Architektur-Schulden | 4 |

---

## Bekannte Issues

### ISSUE-001: Port 8000 belegt
- **Status:** 🟢 Gefixt
- **Symptom:** `ERROR: [Errno 48] Address already in use`
- **Ursache:** Alte Backend-Instanz läuft noch
- **Fix:** Auto-cleanup in Makefile hinzugefügt
  ```makefile
  @lsof -ti:8000 | xargs kill -9 2>/dev/null || true
  ```
- **Verifiziert:** [ ]

---

### ISSUE-002: DB Schema veraltet
- **Status:** 🟢 Gefixt
- **Symptom:** `sqlite3.OperationalError: no such column: tasks.description`
- **Ursache:** Alte `kanban.db` wurde erstellt bevor `description` Feld hinzugefügt wurde
- **Fix:** `rm backend/kanban.db` - DB wird beim nächsten Start neu erstellt
- **Verifiziert:** [ ]

---

## Test-Checkliste

### Backend API
- [ ] `GET /api/tasks` → `[]` (leere Liste)
- [ ] `POST /api/tasks` → Task mit ID zurück
- [ ] `GET /api/tasks/{id}` → Task-Details
- [ ] `PUT /api/tasks/{id}` → Status geändert
- [ ] `DELETE /api/tasks/{id}` → 204 No Content
- [ ] `POST /api/projects` → Project erstellt
- [ ] `POST /api/agent/run` → 202 Accepted
- [ ] `GET /api/agent/runs` → Liste
- [ ] `GET /api/events` → SSE Stream

### Frontend UI
- [ ] Seite lädt (`http://localhost:5173`)
- [ ] Kanban Board zeigt 4 Spalten
- [ ] Task erstellen via "+ Add" Button
- [ ] Task editieren via Klick
- [ ] Drag & Drop zwischen Spalten
- [ ] Task löschen via Dropdown
- [ ] Agent starten via Dropdown
- [ ] SSE Live-Updates (Task erscheint ohne Refresh)

### Agent Flow
- [ ] Agent Run wird erstellt (status: pending)
- [ ] Agent startet (status: running)
- [ ] Logs erscheinen in Sidebar
- [ ] Agent beendet (status: completed/failed)
- [ ] Task-Status wird aktualisiert

---

## Architektur-Erkenntnisse (Session 2026-01-16)

### Datenfluss Frontend ↔ Backend

```
Frontend (TypeScript)              Backend (Python)
━━━━━━━━━━━━━━━━━━━━              ━━━━━━━━━━━━━━━━━

TaskCreate (TS interface)  ──JSON──►  TaskCreate (Pydantic)
TaskUpdate (TS interface)  ──JSON──►  TaskUpdate (Pydantic)
                                             │
                                             ▼
                                       Validation ✓
                                             │
                                             ▼
                                       SQLAlchemy Model
                                             │
                                             ▼
BackendTask (TS interface) ◄──JSON──  TaskResponse (Pydantic)
       │
       ▼
 mapBackendToTask()
       │
       ▼
 Task (Frontend Model)
```

### ARCH-001: Keine automatische Schema-Synchronisation
- **Risiko:** 🔴 Hoch
- **Problem:** Backend-Schema-Änderung → Frontend-Crash möglich
- **Beispiel:** Backend fügt `priority: int` hinzu → Frontend ignoriert es
- **Lösung:** OpenAPI Codegen (`openapi-typescript`)

### ARCH-002: Manuelle Mapping-Funktionen
- **Risiko:** 🟠 Mittel
- **Problem:** `mapBackendToTask()` muss bei jeder Änderung angepasst werden
- **Ort:** `frontend/src/lib/types/task.ts`
- **Lösung:** Codegen oder Zod-Validierung

### ARCH-003: Keine Runtime-Validierung im Frontend
- **Risiko:** 🟠 Mittel
- **Problem:** Backend sendet unerwartete Daten → `undefined` statt Error
- **Lösung:** Zod für Runtime-Validierung

### ARCH-004: Doppelte Typ-Definitionen
- **Risiko:** 🟡 Niedrig
- **Problem:** TypeScript-Types + Pydantic-Schemas müssen manuell synchron gehalten werden
- **Aktuell:** Kommentare `// IMPORTANT: Keep in sync with backend`
- **Lösung:** Single Source of Truth via OpenAPI

### Empfehlung: OpenAPI Codegen

```bash
# FastAPI generiert OpenAPI spec automatisch
# TypeScript-Typen generieren:
npx openapi-typescript http://localhost:8000/openapi.json -o src/lib/types/api.ts
```

**Priorität:** Phase 8+ (nach Plugin Manager)

---

## Neue Issues hier eintragen

### ISSUE-XXX: [Titel]
- **Status:** 🔴 Offen
- **Symptom:** [Was passiert?]
- **Reproduktion:** [Schritte]
- **Ursache:** [Wenn bekannt]
- **Fix:** [Wenn bekannt]
- **Verifiziert:** [ ]

---

## Verification Commands

```bash
# Backend starten
make dev

# API testen
curl http://localhost:8000/api/tasks

# Task erstellen
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task"}'

# Pytest
cd backend && uv run pytest -v

# Quality Gates
make check
```

---

*Updated: 2026-01-16 (Architektur-Erkenntnisse hinzugefügt)*
