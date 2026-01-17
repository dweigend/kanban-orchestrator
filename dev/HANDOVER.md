# HANDOVER

## Phase: 7.3 - Cleanup 🧹

---

## Session 2026-01-17 ✅

**Fixes:**
1. Agent Message Type Detection (`orchestrator.py`)
2. Task Result Field (End-to-End)
3. SSE sendet alle Task-Felder
4. Pydantic Schemas mit Field-Beschreibungen

---

## Architektur-Entscheidung: Backend = Source of Truth

### Warum?

**Problem:** Frontend und Backend haben separate Type-Definitionen, die manuell synchron gehalten werden müssen. Jede Änderung (neues Feld, neuer Task-Type) erfordert Anpassungen an beiden Stellen.

**Lösung:** Das Backend definiert ALLE Datenstrukturen. Das Frontend liest diese und rendert dynamisch.

**Vorteile:**
- Eine Quelle der Wahrheit (Single Source of Truth)
- Änderungen nur im Backend nötig
- Frontend passt sich automatisch an
- LLMs können Backend-Schemas direkt nutzen (Pydantic → JSON Schema)

### Was bleibt gleich

Das aktuelle System ist gut aufgebaut:
- SQLAlchemy Models für DB
- Pydantic Schemas für API
- TypeScript Types für Frontend

**Nicht alles neu bauen!** Stattdessen: Schrittweise erweitern.

---

## Schema-Driven UI Konzept (GitHub #6)

> **Hinweis:** Die folgenden Ideen sind ein Ausgangspunkt für weitere Überlegungen - keine fertigen Anweisungen. Bitte zuerst die Codebasis analysieren und prüfen, wo elegantes Refactoring möglich ist. Ziel: Einfacher werden, nicht komplizierter.

### Grundidee

```
Backend (Pydantic)          Frontend (Svelte)
─────────────────          ─────────────────
TaskResponse               TaskEditor
  - id: str                  - rendert Felder basierend
  - title: str                 auf Schema
  - description: str?        - kennt UI-Komponenten für
  - result: str?               jeden Feld-Typ
  - status: enum
  - type: enum
```

### Schritt 1: Field-Typen definieren (Backend)

Einfache Enum für UI-Rendering-Hints:

```python
class FieldType(StrEnum):
    TEXT = "text"           # Einzeiliges Input
    TEXTAREA = "textarea"   # Mehrzeiliges Input
    SELECT = "select"       # Dropdown (braucht options)
    READONLY = "readonly"   # Nur Anzeige (z.B. Result)
    DATETIME = "datetime"   # Datum/Zeit Anzeige
```

### Schritt 2: Schema-Endpoint (Backend)

```python
@app.get("/api/schema/task")
def get_task_schema():
    return {
        "fields": [
            {"name": "title", "type": "text", "required": True},
            {"name": "description", "type": "textarea"},
            {"name": "result", "type": "readonly"},  # Agent füllt das
            {"name": "status", "type": "select", "options": ["todo", "in_progress", "done"]},
            {"name": "type", "type": "select", "options": ["research", "dev", "notes"]},
        ]
    }
```

### Schritt 3: Dynamisches Rendering (Frontend)

```svelte
{#each schema.fields as field}
  {#if field.type === 'text'}
    <TextInput name={field.name} required={field.required} />
  {:else if field.type === 'textarea'}
    <TextArea name={field.name} />
  {:else if field.type === 'readonly'}
    <ReadonlyDisplay name={field.name} />
  {:else if field.type === 'select'}
    <Select name={field.name} options={field.options} />
  {/if}
{/each}
```

### Was das ermöglicht

- Neues Feld im Backend → Frontend zeigt es automatisch
- Verschiedene Task-Types mit unterschiedlichen Feldern
- MCP-spezifische Felder ohne Frontend-Änderung

---

## Pydantic Best Practices (KISS)

### Ziel

Lesbar, typsicher, gut dokumentiert - nicht over-engineered.

### Regeln

1. **Jedes Feld hat eine `description`** (LLMs nutzen das)
2. **Beispiele wo sinnvoll** (nicht für jedes Feld)
3. **Validierung nur wo nötig** (min_length für title, nicht für alles)
4. **Klare Docstrings** für die Klasse
5. **`ConfigDict(from_attributes=True)`** für ORM-Konvertierung

### Beispiel (aktuell gut)

```python
class TaskCreate(BaseModel):
    """Create a new task on the Kanban board."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Brief task title",
    )
    description: str | None = Field(
        None,
        description="Detailed task description",
    )
    status: TaskStatus = Field(
        TaskStatus.TODO,
        description="Initial Kanban column",
    )
```

### Nicht over-engineeren

❌ Zu viel:
```python
title: Annotated[str, Field(
    min_length=1,
    max_length=255,
    pattern=r'^[A-Za-z].*',
    description="...",
    examples=["...", "...", "..."],
    json_schema_extra={"ui_component": "text", "placeholder": "..."}
)]
```

✅ Genug:
```python
title: str = Field(..., min_length=1, max_length=255, description="Brief task title")
```

---

## Nächste Sessions

### Session A: Backend

**Erst erkunden, dann entscheiden:**
1. Codebasis analysieren - wo gibt es Redundanz?
2. Refactoring-Möglichkeiten identifizieren
3. Elegantere Lösungen finden (weniger Code, nicht mehr)

**Checklist:**
- [ ] Schemas reviewen und vereinfachen
- [ ] Error Handling standardisieren
- [ ] Schema-Endpoint evaluieren (für dynamisches Frontend)
- [ ] Tests für neue Funktionalität
- [ ] Pydantic Best Practices prüfen

### Session B: Frontend

**Erst erkunden, dann entscheiden:**
1. Komponenten-Struktur verstehen
2. Wo kann vereinfacht werden?
3. Was braucht das Frontend wirklich vom Backend?

**Checklist:**
- [ ] Unused Imports entfernen (53 Biome Warnings)
- [ ] TypeScript Types mit Backend synchronisieren
- [ ] Dynamischer Field-Renderer evaluieren
- [ ] A11y Warnings fixen
- [ ] Redundante Komponenten identifizieren

---

## Commands

```bash
make dev                    # Server starten
cd backend && uv run pytest # Tests
make check                  # Quality Gates
```

---

*Updated: 2026-01-17*
