# Design: Task-Delegations-System

**Phase:** 11A - Konzept
**Status:** ✅ Abgeschlossen
**Datum:** 2026-01-24

---

## 1. Vision & Philosophie

### Kern-Idee

Der Kanban Orchestrator ist ein **asynchrones Task-Delegations-System**. Er empfängt Tasks aus verschiedenen Quellen und verarbeitet sie im Hintergrund.

### Use Cases

1. **Aus Claude Code (MCP):** "Recherchiere X und speichere es in meinen Notizen"
2. **Direkt in UI:** Recherche-Projekte, To-Dos, Dev-Tasks
3. **Control Center:** Alle Tasks überwachen, Subtasks bestätigen, Ergebnisse reviewen

### Architektur-Prinzipien

| Prinzip | Beschreibung |
|---------|--------------|
| **Everything via MCP** | Alle I/O-Operationen laufen über MCPs (Filesystem, Trilium, etc.) |
| **Sandbox → Target** | Agent arbeitet in isoliertem Ordner, kopiert bei Completion zum Ziel |
| **Schema-Driven** | Enums und Validierung gegen Registry |
| **Defaults + Override** | Schnelle Task-Erstellung, aber volle Kontrolle wenn nötig |

---

## 2. System-Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                    Kanban UI (Control Center)                │
│  - Task-Monitoring (alle Tasks, egal woher)                 │
│  - Task-Kontrolle (NEEDS_REVIEW Flow)                       │
│  - Task-Erstellung (mit optionalen Feldern)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Task Orchestrator                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Task DB  │  │  Queue   │  │ Template │  │   MCP    │    │
│  │          │  │          │  │  Engine  │  │  Router  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  Filesystem │ │   Trilium   │ │  Perplexity │
    │     MCP     │ │     MCP     │ │     MCP     │
    └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 3. Task-Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                      Task Lifecycle                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CREATED                                                 │
│     ├─ sandbox_dir erstellt: output/{task_id}/             │
│     └─ target_path gespeichert (optional)                  │
│                                                             │
│  2. IN_PROGRESS                                             │
│     └─ Agent schreibt NUR in sandbox_dir                   │
│                                                             │
│  3. NEEDS_REVIEW (optional)                                 │
│     └─ User reviewed Ergebnis in Sandbox                   │
│                                                             │
│  4. DONE                                                    │
│     ├─ IF target_path definiert:                           │
│     │   └─ Kopiere sandbox_dir/* → target_path             │
│     └─ Sandbox bleibt als Archiv                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Wichtig:** Wenn kein `target_path` angegeben → alles bleibt in `output/{task_id}/`

---

## 4. Datenmodell

### Neue Task-Felder

| Feld | Typ | Default | Beschreibung |
|------|-----|---------|--------------|
| `sandbox_dir` | String (auto) | `output/{task_id}/` | Isolierter Arbeitsordner |
| `target_path` | String? | `null` | Finale Destination (optional) |
| `read_paths` | JSON? | `[]` | Erlaubte Lese-Pfade |
| `allowed_mcps` | JSON? | defaults aus Registry | Erlaubte MCPs |
| `template` | String? | default für `type` | Template-Name oder Inline-MD |
| `source` | String | `"ui"` | Woher: `ui`, `mcp`, `api` |

### Bestehende Felder (unverändert)

- `id`, `title`, `description`, `status`, `type`, `steps`, `parent_id`, `result`, `project_id`, `created_at`

### Beispiel-Task (via MCP)

```json
{
  "id": "abc123",
  "title": "Recherche: Farbwahrnehmung Rot",
  "description": "Wie nehmen Menschen rote Farbe wahr? Wichtig für UI-Design.",
  "type": "research",
  "status": "todo",
  "sandbox_dir": "output/abc123/",
  "target_path": "/Users/david/notes/research/",
  "read_paths": [],
  "allowed_mcps": ["perplexity", "filesystem"],
  "template": "research",
  "source": "mcp"
}
```

---

## 5. MCP Registry

### Datei: `.kanban/mcps.yaml`

```yaml
# Verfügbare MCP-Server
mcps:
  filesystem:
    enabled: true
    command: "python"
    args: ["-m", "src.mcp_servers.filesystem.server"]
    env:
      WORKSPACE_PATH: "${SANDBOX_DIR}"

  perplexity:
    enabled: true
    command: "npx"
    args: ["-y", "@anthropic/perplexity-mcp"]
    env:
      PERPLEXITY_API_KEY: "${PERPLEXITY_API_KEY}"

  trilium:
    enabled: false  # Phase 12
    command: "npx"
    args: ["-y", "@anthropic/trilium-mcp"]

# Defaults für neue Tasks
defaults:
  allowed_mcps: ["filesystem", "perplexity"]
  template: "research"
```

### Vorteile

- ✅ Keine Code-Änderung für neue MCPs
- ✅ Dynamische Environment-Variablen
- ✅ Enable/Disable per MCP
- ✅ Zentrale Defaults

---

## 6. Templates

### Ordner-Struktur

```
templates/
├── research.md   # Standard-Recherche
├── dev.md        # Development-Tasks
└── notes.md      # Einfache Notizen
```

### templates/research.md (Default)

```markdown
# {title}

## Kontext
{description}

## Recherche-Ergebnisse
[Agent füllt aus]

## Kernerkenntnisse
-

## Quellen
-
```

### Verwendung

- Templates werden dem Agent als Kontext mitgegeben
- Agent orientiert sich an der Struktur
- Custom-Template kann als Inline-Markdown übergeben werden

---

## 7. Kanban MCP API (Erweitert)

### create_task

```python
create_task(
    # Pflichtfelder
    title: str,
    description: str,

    # Optionale Felder (mit Defaults)
    type: Literal["research", "dev", "notes", "neutral"] = "research",
    target_path: str | None = None,
    read_paths: list[str] = [],
    allowed_mcps: list[str] | None = None,  # None = use defaults
    template: str | None = None,            # Name oder Inline-MD
) -> TaskCreatedResponse
```

### Response

```json
{
  "task_id": "abc123",
  "sandbox_dir": "output/abc123/",
  "status": "todo",
  "message": "Task erstellt. Ergebnis wird in output/abc123/ gespeichert."
}
```

### Weitere Tools

```python
# Schema-Discovery (für Clients)
get_task_options() -> {
    "types": ["research", "dev", "notes", "neutral"],
    "available_mcps": ["filesystem", "perplexity"],
    "templates": ["research", "dev", "notes"],
    "defaults": {...}
}

# Status abfragen
get_task_status(task_id: str) -> TaskStatusResponse

# Ergebnis abrufen
get_task_result(task_id: str) -> TaskResultResponse

# Tasks auflisten (mit Filtern)
list_tasks(
    status: str | None = None,
    type: str | None = None,
    source: str | None = None,
) -> list[TaskSummary]
```

---

## 8. Implementierungs-Roadmap

### Phase 11A: Konzept ✅
- Design-Dokument (dieses Dokument)

### Phase 11B: Backend Task-Model Erweiterung
- Neue Felder im SQLAlchemy Model
- Automatische `sandbox_dir` Generierung
- Copy-to-target Logik bei Task-Completion

### Phase 11C: MCP Registry
- `.kanban/mcps.yaml` Parser
- `get_mcp_config()` liest aus YAML
- Validierung gegen Registry

### Phase 11D: Templates
- `templates/` Ordner Setup
- Template-Loader für Agent-Prompt
- Default-Templates erstellen

### Phase 11E: Kanban MCP API Update
- `create_task()` erweitern
- `get_task_options()` implementieren
- Validierung gegen Registry

### Phase 11F: Frontend Anpassungen
- TaskEditor: Neue Felder
- Schema-Endpoint Integration
- Optional-Fields UI

### Phase 12: Trilium Integration (Später)
- Trilium MCP recherchieren/einbinden
- Als Output-Target verfügbar machen

---

## 9. Offene Fragen (für später)

1. **Cleanup-Policy:** Wie lange bleiben sandbox_dir Ordner erhalten?
2. **Permissions-Granularität:** Brauchen wir feinere read/write Berechtigungen?
3. **Template-Variablen:** Welche Platzhalter außer `{title}` und `{description}`?

---

*Erstellt: 2026-01-24*
