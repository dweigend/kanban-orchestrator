# Troubleshooting Guide

Dokumentation bekannter Probleme und deren Lösungen.

---

## 🐛 CORS Error bei API Calls

### Symptom

```
Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:5173'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

### Ursache

**CORS-Fehler sind oft Symptome, nicht die eigentliche Ursache!**

Wenn FastAPI crasht BEVOR eine Response gesendet wird, fehlen die CORS-Header. Das kann passieren bei:

1. **DB-Schema Mismatch** - Model hat Felder, die in der DB-Tabelle fehlen
2. **Import-Fehler** - Module können nicht geladen werden
3. **Pydantic-Validierung** - Response-Model erwartet Werte, die `None` sind
4. **Unbehandelte Exceptions** - Server crasht ohne Response

### Debugging-Schritte

```bash
# 1. Teste den Endpoint direkt mit curl (ohne Browser/CORS)
curl -X POST http://localhost:8000/api/agent/run \
  -H "Content-Type: application/json" \
  -d '{"task_id": "test-id"}'

# Wenn curl "Internal Server Error" zurückgibt → Server-seitiger Bug!

# 2. Prüfe DB-Schema
sqlite3 kanban.db ".schema <table_name>"

# 3. Vergleiche mit SQLAlchemy Model
# Alle Felder im Model müssen in der DB existieren
```

### Lösung

```bash
# Option A: DB Reset (Development)
cd backend
rm kanban.db
uv run python main.py  # Erstellt DB neu

# Option B: Migration (wenn Daten erhalten bleiben sollen)
sqlite3 kanban.db "ALTER TABLE <table> ADD COLUMN <column> <type> DEFAULT <value>;"
```

---

## 🐛 DB-Schema Mismatch nach Model-Änderungen

### Ursache

SQLAlchemy erstellt Tabellen nur beim ersten Start. Wenn ein Model geändert wird (neues Feld), muss die DB manuell aktualisiert werden.

### Prävention

**WICHTIG:** Nach jeder Model-Änderung:

1. Prüfe ob die DB-Tabelle das neue Feld hat
2. Entweder DB löschen oder ALTER TABLE ausführen
3. Teste den betroffenen Endpoint

### Betroffene Dateien

| Model | Tabelle | Kritische Felder |
|-------|---------|------------------|
| `models/task.py` | `tasks` | created_at |
| `models/project.py` | `projects` | created_at |
| `models/agent_run.py` | `agent_runs` | created_at |

### Check-Script

```bash
# Alle Tabellen-Schemas anzeigen
sqlite3 kanban.db ".schema"

# Spezifische Tabelle prüfen
sqlite3 kanban.db ".schema agent_runs" | grep created_at
```

---

## 🐛 Biome "unused imports" bei Svelte-Komponenten

### Symptom

```
lint/correctness/noUnusedImports - This import is unused.
import FieldText from './FieldText.svelte';
```

### Ursache

Biome erkennt nicht, dass Svelte-Komponenten im Template verwendet werden.

### Lösung

```svelte
<!-- Option A: biome-ignore Kommentar -->
<script lang="ts">
// biome-ignore lint/correctness/noUnusedImports: Used in Svelte template
import FieldText from './FieldText.svelte';
</script>

<!-- Option B: In biome.json für .svelte Dateien deaktivieren -->
```

---

## 🐛 Server startet nicht / Port belegt

### Symptom

```
Error: Address already in use
# oder
curl: (7) Failed to connect
```

### Lösung

```bash
# Finde Prozess auf Port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill Prozess
kill -9 <PID>

# Neustart
cd backend && uv run uvicorn main:app --port 8000 &
cd frontend && bun dev &
```

---

## 🐛 Agent Run startet nicht

### Checkliste

1. ✅ Backend läuft? (`curl http://localhost:8000/health`)
2. ✅ Task existiert? (`curl http://localhost:8000/api/tasks`)
3. ✅ Kein aktiver Run für diesen Task? (409 Conflict)
4. ✅ DB-Schema korrekt? (siehe oben)

### Logs prüfen

```bash
# Backend-Logs (wenn im Terminal gestartet)
# Oder: uvicorn mit --log-level debug starten
uv run uvicorn main:app --log-level debug
```

---

## Allgemeine Debugging-Tipps

### Systematisches Debugging

1. **Error Message lesen** - Genau lesen, nicht überfliegen
2. **Reproduzieren** - Kann der Fehler konsistent ausgelöst werden?
3. **Isolieren** - Funktioniert es mit curl? → CORS/Browser-Problem vs Server-Problem
4. **Eine Änderung** - Nur EINE Sache gleichzeitig testen
5. **Dokumentieren** - Fix hier eintragen für zukünftige Referenz

### Quick Health Checks

```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:5173 -o /dev/null -w "%{http_code}"

# DB existiert
ls -la backend/kanban.db

# DB-Schema
sqlite3 backend/kanban.db ".tables"
```

---

*Updated: 2026-01-18*
