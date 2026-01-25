# MCP Discovery & Workflow Design

> Konzeptionelle Überlegungen für MCP-Integration und Workflow-Orchestrierung.

## Kernprinzip: KISS + Orchestrierung

```
┌─────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (minimal, stabil)                         │
│  ════════════════════════════════                       │
│  Delegiert Arbeit an MCPs                               │
│  Kettet Tools hintereinander (Workflow)                 │
│  Strukturiert Output via Templates                      │
└─────────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Perplexity │  │  OpenAlex   │  │   Trilium   │
│  (Search)   │  │  (Papers)   │  │   (Store)   │
└─────────────┘  └─────────────┘  └─────────────┘
```

**Die Macht liegt in:**
- **Orchestrierung**: Mehrere Tools hintereinander nutzen
- **Templates**: Strukturierter Output
- **Modulare MCPs**: Jedes Tool macht, was es am besten kann
- **Bestehende Funktionen nutzen**: Trilium, Zotero etc. haben schon alles eingebaut
- **Sandbox pro Task**: Zwischenergebnisse persistent speichern

---

## Sandbox-Konzept: Robustheit durch Persistenz

```
backend/output/
└── {task_id}/              ← Sandbox für jeden Task
    ├── step_1_search.json  ← Zwischenergebnis Perplexity
    ├── step_2_papers.json  ← Zwischenergebnis OpenAlex
    ├── step_3_draft.md     ← Entwurf vor Trilium-Upload
    └── final_output.md     ← Fertiges Ergebnis
```

**Vorteile:**
- Bei Abbruch: Zwischenergebnisse erhalten
- Debugging: Jeden Schritt nachvollziehbar
- Review: User kann vor finalem Speichern prüfen
- Wiederaufnahme: Task kann fortgesetzt werden

---

## MCP Inventory

### Aktiv

| MCP | Quelle | Use Case |
|-----|--------|----------|
| `filesystem` | Intern | Sandboxed File I/O |
| `github_simple` | `~/mcp_code/github_simple` | GitHub Read-Only |
| `perplexity` | `~/mcp_code/perplexity_code` | Web Search |
| `openalex` | `~/mcp_code/openalex` | Academic Papers |

### Geplant

| MCP | Quelle | Use Case | Phase |
|-----|--------|----------|-------|
| `trilium` | `triliumnext-mcp` (npm) | Notes speichern | 11.5B |
| `zotero` | `54yyyu/zotero-mcp` | Bibliography, PDFs | 12 |

### MCP Details

#### OpenAlex (`LeoGitGuy/alex-paper-search-mcp`)
- **Install**: `git clone` + `uv sync`
- **Start**: `uv run python run_stdio.py`
- **Env**: `OPENALEX_EMAIL` (optional, für polite pool)
- **Tools**: `search_openalex`, `get_paper_by_id`, `search_recent_papers`, etc.

#### Trilium (`triliumnext-mcp`)
- **Install**: `npx -y triliumnext-mcp`
- **Env**: `TRILIUM_API_URL`, `TRILIUM_API_TOKEN`
- **Features**: CRUD Notes, Search, Attributes, Daily Notes

#### Zotero (`54yyyu/zotero-mcp`)
- **Voraussetzung**: Zotero + Better BibTeX Plugin
- **Features**: Semantic Vector Search, BibTeX Export, PDF Annotations

---

## Template-System

### Template-Typen

| Template | Use Case | Sections |
|----------|----------|----------|
| `quick.md` | Schnelle Fragen | TL;DR, Key Points, Sources |
| `deep.md` | Umfassende Recherche | Summary, Background, Findings, Open Questions |
| `paper.md` | Paper-Analyse | Abstract, Contributions, Methods, Results, BibTeX |
| `idea.md` | Brainstorming | Problem, Related Concepts, Open Questions, Next Steps |

### Beispiel: `quick.md`

```markdown
# {topic}
> Erstellt: {date} | Quellen: {source_count}

## TL;DR
{one_paragraph_summary}

## Key Points
- {point_1}
- {point_2}

## Sources
- {source_links}
```

---

## Workflow-Konzepte

### 1. Topic Research (ohne Review)

```
CREATED → IN_PROGRESS → DONE
           │
           ├─ Perplexity Search
           ├─ Optional: OpenAlex Papers
           └─ Output: Trilium Note
```

**MCPs:** `perplexity`, `openalex`, `trilium`
**Template:** `quick.md` oder `deep.md`

### 2. Literature Review (mit Review)

```
CREATED → IN_PROGRESS → NEEDS_REVIEW → DONE
           │                │
           ├─ OpenAlex     └─ User wählt
           │   Query          relevante Paper
           └─ Paper-Liste
```

**Schritt 1:** OpenAlex Query → Paper-Liste mit Abstracts
**Review:** User wählt relevante Paper (weniger = besser)
**Schritt 2:** Synthese + BibTeX auf Basis der Auswahl

**MCPs:** `openalex`, `trilium`
**Template:** `paper.md`

### 3. Prototyping

```
CREATED → IN_PROGRESS → DONE
           │
           ├─ Code schreiben
           ├─ Git Commit
           └─ README generieren
```

**MCPs:** `filesystem`, `github`
**Template:** `idea.md`

### 4. Content Pipeline

```
CREATED → IN_PROGRESS → NEEDS_REVIEW → DONE
           │                │
           ├─ Research     └─ User prüft
           └─ Draft           Draft
```

**Varianten:**
- Social Media: Research → Post-Draft → Review → Publish
- Blog: Research → Artikel → Trilium → Export
- Docs: Code analysieren → Dokumentation

---

## Kanban + Workflows

Das Kanban-Board ermöglicht klare Trennung der Phasen:

```
┌──────────┐   ┌─────────────┐   ┌──────────────┐   ┌────────┐
│ CREATED  │ → │ IN_PROGRESS │ → │ NEEDS_REVIEW │ → │  DONE  │
└──────────┘   └─────────────┘   └──────────────┘   └────────┘
     │               │                  │                │
  Sammeln      Systematisieren      Review          Delegieren
  (Input)       (Agent arbeitet)   (User prüft)    (Output)
```

**Wann NEEDS_REVIEW?**
- Literature Review: Nach Paper-Auswahl (Schritt 1)
- Content: Vor Veröffentlichung
- Prototyping: Bei kritischen Entscheidungen
- Simple Research: Direkt zu DONE (kein Review nötig)

---

## Trilium-Struktur (Hybrid-Ansatz)

Empfohlen für den Start:

```
📁 Research/       ← Output vom Orchestrator
   📄 2026-01-25_MCP-Servers
   📄 2026-01-26_Agent-Patterns
📁 Projects/       ← Manuelle Projekt-Notes
📁 Archive/        ← Verarbeitete Research-Notes
```

**Prinzip:** Der Orchestrator schreibt in `Research/`, du verarbeitest weiter.

---

## Brainstorming: Zukünftige Features

### Automatisierung

- **Scheduled Research**: Monitoring von Topics → Neue Infos → Trilium Inbox
- **Auto-Kategorisierung**: ML-basierte Zuordnung zu Topics/Projects

### Content Pipelines

- **Social → Publish**: Research → Post-Draft → Review → Scheduling
- **Blog → Website**: Research → Artikel → Trilium → Hugo/Jekyll Export
- **Code → Docs**: Repo analysieren → API-Dokumentation generieren

### Chaos → Ordnung

- Lokale Dateien analysieren
- Kontext identifizieren
- Verknüpfungen zu bestehendem Wissen
- Richtige Ablage (Zotero, Trilium, Dateisystem)
- Audio transkribieren → Reports

### Multi-Step Workflows

- Agent-Chaining: Output von Agent A → Input für Agent B
- Conditional Flows: "Wenn Paper-Anzahl > 20, dann NEEDS_REVIEW"
- Parallel Execution: Mehrere MCPs gleichzeitig anfragen

---

## Quellen-Handling

### Einfache Recherche
Inline-Links reichen: `[Titel](URL)`

### Wissenschaftliche Recherche (2-Schritt)

```
┌─────────────────────────────────────────────────────────┐
│  SCHRITT 1: Literatur-Identifikation                   │
├─────────────────────────────────────────────────────────┤
│  OpenAlex Query → Paper-Liste                          │
│  → User reviewed relevante Paper (weniger = besser)    │
│  → Auswahl bestätigen                                   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  SCHRITT 2: Synthese                                    │
├─────────────────────────────────────────────────────────┤
│  Auf Basis der ausgewählten Quellen:                   │
│  → Antwort formulieren                                  │
│  → BibTeX generieren                                    │
│  → Quellenanalyse                                       │
│  → Literaturübersicht                                   │
└─────────────────────────────────────────────────────────┘
```

---

*Erstellt: 2026-01-25*
