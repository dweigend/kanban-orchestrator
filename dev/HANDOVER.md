# HANDOVER

## Phase: Phase 11B Abgeschlossen ✅ - Backend Task-Model Erweiterung

---

## Session 2026-01-25 (Phase 11B - Implementation + Frontend Test)

### Was wurde gemacht

**1. Backend Task-Model Erweiterung**

| Datei | Änderungen |
|-------|------------|
| `backend/src/models/task.py` | TaskSource Enum + 6 neue Columns |
| `backend/src/api/schemas.py` | TaskCreate/Update/Response erweitert |
| `backend/src/api/task_service.py` | sandbox_dir Generation + copy-to-target |
| `frontend/src/lib/types/task.ts` | TypeScript Interfaces synchronisiert |

**Neue Task-Felder:**
- `sandbox_dir` - Auto-generiert: `output/{task_id}/`
- `target_path` - Optionale Ziel-Destination
- `read_paths` - Erlaubte Lese-Pfade (JSON)
- `allowed_mcps` - Erlaubte MCPs (JSON)
- `template` - Template-Name
- `source` - Herkunft: ui/mcp/api

**2. Frontend: Task Info Sektion**

- TaskEditor zeigt jetzt Sandbox + Target + Source
- `frontend/src/lib/components/panel/TaskEditor.svelte` erweitert

**3. Verifikation**

- ✅ 78 Backend-Tests bestanden
- ✅ Task-Erstellung via UI → sandbox_dir wird generiert
- ✅ Task-Erstellung via API mit target_path funktioniert
- ✅ Copy-to-target bei status → DONE funktioniert
- ✅ Frontend zeigt neue Felder korrekt an

**4. Neue Issues angelegt**

| # | Issue | Severity |
|---|-------|----------|
| #27 | Klickbare Pfade + Default Editor (Zed) | LOW |
| #28 | Task-Summary im Board (Konzept nötig) | MEDIUM |
| #29 | Overview Tab ohne Funktion | LOW |
| #30 | Agent Log Panel zeigt keine Runs | MEDIUM |

### Geänderte Dateien

```
backend/src/models/task.py              # TaskSource Enum + 6 neue Columns
backend/src/api/schemas.py              # Pydantic Schemas erweitert
backend/src/api/task_service.py         # sandbox_dir + copy-to-target
frontend/src/lib/types/task.ts          # TypeScript Interfaces
frontend/src/lib/components/panel/TaskEditor.svelte  # Task Info Sektion
dev/ISSUE_TRACKER.md                    # 4 neue Issues
dev/HANDOVER.md                         # Diese Datei
```

---

## Nächste Session: Phase 11C - MCP Registry

### Ziel

Dynamische MCP-Konfiguration aus YAML-Datei.

### Tasks

| # | Task | Datei |
|---|------|-------|
| 1 | `.kanban/mcps.yaml` Format definieren | `.kanban/mcps.yaml` |
| 2 | YAML-Parser für MCP-Registry | `backend/src/mcp_client/registry.py` |
| 3 | `get_mcp_config()` liest aus YAML | `backend/src/mcp_client/registry.py` |
| 4 | Validierung: nur enabled MCPs erlaubt | Service Layer |
| 5 | Environment-Variable Auflösung | `${SANDBOX_DIR}` etc. |

### Reihenfolge der Phasen

```
Phase 11B: Backend Task-Model ✅ DONE
Phase 11C: MCP Registry ← NÄCHSTE SESSION
Phase 11D: Templates
Phase 11E: Kanban MCP API
Phase 11F: Frontend Anpassungen
Phase 12: Trilium Integration
```

---

## Offene Issues (Priorisiert)

| Prio | # | Issue | Severity | Phase |
|------|---|-------|----------|-------|
| 1 | #25 | Erweiterte Task-Definition | ✅ Backend done | 11B ✅ |
| 2 | #26 | MCP Registry & Templates | Konzept ✅ | 11C-D |
| 3 | #22 | Projekt-Management | HIGH | Backlog |
| 4 | #30 | Agent Log Panel Bug | MEDIUM | Bugfix |
| 5 | #28 | Task-Summary im Board | MEDIUM | Konzept |
| 6 | #27 | Klickbare Pfade + Editor | LOW | 11F |
| 7 | #29 | Overview Tab | LOW | UI Cleanup |

---

## Verification Commands

```bash
# Server starten
make dev

# Backend Checks
cd backend
uv run ruff check --fix . && uv run ruff format .
uvx ty check
uv run pytest

# Frontend Checks
cd frontend
bunx biome check --write .
bunx svelte-check --threshold warning
```

---

## API Test (Phase 11B)

```bash
# Task mit neuen Feldern erstellen
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "target_path": "/tmp/output", "source": "mcp"}'

# Response enthält:
# - sandbox_dir: "output/{uuid}/"
# - source: "mcp"
# - target_path: "/tmp/output"
```

---

## User-Präferenzen (für Phase 11F)

- **Default Editor:** Zed (`zed <path>`)

---

*Updated: 2026-01-25*
