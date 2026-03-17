# Architecture

## Quick Reference
**Stack:** Python 3.12+, Textual 8+
**Entry point:** `guitar_tui/app.py` — `GuitarTUI` App subclass; wires loaders in `on_mount`, pushes `HomeScreen`
**Key paths:**
- `guitar_tui/ui/screens/` — all screens (HomeScreen is the main screen)
- `guitar_tui/ui/widgets/` — custom widgets (FullNeckWidget, MetronomeWidget, …)
- `guitar_tui/ui/app.tcss` — global stylesheet (design tokens throughout; no inline styles)
- `guitar_tui/engine/` — music-agnostic DiagramSpec renderers
- `guitar_tui/loaders/` — DataLoader, LessonLoader, ExerciseLoader, LickLoader
- `guitar_tui/data/` — YAML chord/scale data (validated on startup)
- `guitar_tui/content/` — Markdown lessons, exercises, licks

**Key constraints:**
- Engine is music-agnostic — renders DiagramSpec objects only; never reads YAML or chord names directly
- Data validates on startup via Pydantic; hard error on invalid data, never silent corruption
- No blocking I/O on the main thread; loaders run in `on_mount`
- `schemas/` is the dev–instructor contract; no unilateral changes by either persona

**Patterns:** Reactive state, message passing, screen composition, discriminated union DiagramSpec models


## Decisions (ADRs)

### D1 — Music-agnostic engine

**Decision**: The engine (`guitar_tui/engine/`) renders DiagramSpec objects and has no knowledge of music theory. It does not know what a G chord is, what intervals a pentatonic scale contains, or what strings are standard-tuned to.

**Rationale**: Coupling rendering logic to music knowledge makes both harder to change. If the engine knows chord theory, changing a voicing requires touching rendering code. Keeping them separate means the engine can be tested with arbitrary coordinate data, and music data can be corrected without risking rendering regressions. The engine is also reusable for any stringed instrument — it just renders grids and dots.

**Consequence**: All music knowledge lives in `guitar_tui/data/` (YAML) and `guitar_tui/content/` (lessons). The engine receives fully-resolved DiagramSpec objects from the loader layer — it never reads YAML directly.

---

### D2 — YAML for music data

**Decision**: Chord voicings, scale patterns, and tunings are stored as YAML files in `guitar_tui/data/`.

**Alternatives considered**:
- **SQLite** — rejected; adds query complexity and a schema migration story for what is essentially a static reference library. Overkill for read-only data.
- **JSON** — rejected; YAML is more readable for humans editing music data (the Instructor persona), handles comments, and handles multiline strings more gracefully.
- **Python literals** — rejected; hard-coding data in Python files blurs the data/code boundary and makes the Instructor persona impossible.

**Consequence**: Data is version-controlled alongside code, human-editable without tooling, and validated at startup by Pydantic rather than at query time.

---

### D3 — Markdown + YAML frontmatter for lessons

**Decision**: Lessons are `.md` files with YAML frontmatter (via `python-frontmatter`) and fenced `diagram` code blocks for embedded diagrams.

**Alternatives considered**:
- **Pure YAML** — rejected; lesson prose is better written in Markdown than as YAML string literals. Authoring experience matters for the Instructor.
- **reStructuredText** — rejected; less familiar than Markdown, heavier tooling requirements, no clear advantage for this use case.
- **Custom DSL** — rejected; unnecessary complexity. Markdown is readable outside the app (GitHub, VS Code, Obsidian), reducing the Instructor's dependency on the TUI being runnable.

**Consequence**: Lessons are readable and editable without running the app. The `diagram` fenced block is the only non-standard Markdown extension — everything else is plain GFM.

---

### D4 — Pydantic for schema validation

**Decision**: All data schemas — DiagramSpec variants, chord/scale YAML models — are defined as Pydantic v2 models.

**Alternatives considered**:
- **dataclasses** — rejected; no built-in validation, requires manual type coercion from YAML dicts.
- **TypedDict** — rejected; structural typing only, no runtime validation.
- **JSON Schema + jsonschema library** — rejected; requires maintaining a separate schema file and validation library alongside Python types. Pydantic unifies both.

**Consequence**: Validation errors are descriptive and field-specific. The Pydantic model is the single source of truth for what constitutes valid data — no separate schema files needed for the data layer.

---

### D5 — Bottom-up build order

**Decision**: Implementation proceeds Data → Engine → Content → TUI (M1 → M2 → M3 → M4).

**Rationale**: Each layer's API is the contract for the layer above. Building top-down would require mocking lower layers, then replacing the mocks — doing the work twice. Building bottom-up means each layer is real and tested before it is depended upon. The TUI is the thinnest layer; it should be assembled last from proven components.

**Consequence**: There is no visible UI until M4. This is intentional. Early milestones produce tested library code, not demos.

---

### D6 — Embedded content, no user content path

**Decision**: All lesson content and music data is bundled with the application. There is no mechanism for users to add their own lessons or chord libraries in the initial implementation.

**Rationale**: User-configurable content paths add path resolution, validation, merge conflict, and error reporting complexity that is not warranted before the core experience is proven. The target user is a single guitarist, not a platform.

**Consequence**: Content is version-controlled. Adding new lessons means contributing to the repository. This can be revisited post-M8 if needed.

---

### D7 — Textual as the TUI framework

**Decision**: The application is built on [Textual](https://textual.textualize.io/) (not urwid, blessed, curtsies, or raw curses).

**Rationale**: Textual provides a component model (widgets, screens, CSS styling) that maps well to the application's structure. It has active development, good documentation, async-native design (required for responsive UI), and built-in devtools. The Rich library (bundled with Textual) handles all styled terminal output in the engine layer.

**Consequence**: The minimum Python version is 3.12 (Textual's async features work best there). The CSS-based styling system (`app.tcss`) is Textual-specific — it is not transferable to other frameworks.


## Detail

### App structure
```
guitar_tui/
├── app.py                        # GuitarTUI App subclass; on_mount loads all loaders, pushes HomeScreen
├── settings.py                   # AppSettings Pydantic model + load()/save() helpers (platformdirs)
├── ui/
│   ├── app.tcss                  # Global stylesheet; design tokens throughout
│   ├── screens/
│   │   ├── home.py               # HomeScreen — main screen; always mounted
│   │   ├── lesson.py             # LessonScreen — kept for potential fullscreen; not part of main nav
│   │   └── ...                   # Welcome, Tools, Practice screens (being restructured per REDESIGN)
│   └── widgets/
│       ├── metronome.py          # MetronomeWidget — visual metronome; timer attached to widget
│       ├── full_neck.py          # FullNeckWidget — rolling-window fretboard; watches App.dark
│       └── ...                   # Additional custom widgets
├── engine/
│   ├── models.py                 # DiagramSpec discriminated union (ChordSpec, ScaleSpec, TabSpec, FretboardSpec)
│   ├── chord_renderer.py         # 19-char grid; nut/sep/bottom box-drawing chars
│   ├── scale_renderer.py         # Horizontal 5-char columns; strings top-to-bottom e→E
│   ├── fretboard_renderer.py     # Same structure as scale; root=■, highlight=●, muted=×
│   ├── tab_renderer.py           # 6-line staff; supports measures (bar lines) and beat duration
│   └── dispatcher.py             # TypeAdapter routes dict→spec→renderer; ValidationError on bad input
├── loaders/
│   ├── data_loader.py            # DataLoader — validates all YAML on startup; hard error on invalid
│   ├── lesson_loader.py          # LessonLoader — parses frontmatter + body; two-phase (parse then prereq warn)
│   ├── exercise_loader.py        # Second LessonLoader instance for exercises
│   └── lick_loader.py            # LickLoader — parses lick files
├── data/
│   ├── chords/                   # open_chords.yaml, barre_chords.yaml, seventh_chords.yaml, …
│   └── scales/                   # minor_pentatonic.yaml, major.yaml, dorian.yaml, …
└── content/
    ├── lessons/                  # 78 lessons in 11 track subdirectories (01-orientation/ … 11-song-analysis/)
    ├── exercises/                # Focused technique/scale/chord drills
    └── licks/                    # 10 looper-ready melodic phrases (8 categories)
```

### State model
- **App-level**: `app.data` (DataLoader), `app.lessons` (LessonLoader), `app.exercises` (ExerciseLoader), `app.licks` (LickLoader), `app.settings` (AppSettings — persisted via platformdirs)
- **Screen-level**: active lesson slug, current reference key/scale selection, metronome BPM/time sig/running state
- **Cross-screen reactive**: `App.dark` watched by FullNeckWidget for theme-aware palette switching
- Loaders are independent at parse time; cross-loader validation (`see_also`, `licks:` frontmatter) runs as a post-processing step in `on_mount`

### Screen map
| Screen | Key | Description |
|--------|-----|-------------|
| HomeScreen | — | Always mounted; Horizontal split: left=VerticalScroll(Tree + ref selects), right=ContentSwitcher(welcome \| lesson-view) |
| Lesson view | inline | TabbedContent inside HomeScreen right pane: Lesson / Practice / References tabs |
| ToolsMode (Tools screen) | `[3]` / `r` | Key View (FullNeckWidget + diatonic chord strip) + Reference tab; being restructured to spatial layout per REDESIGN |
| PracticeMode | `[4]` | Exercises tab + Licks Library tab; being dissolved into Study screen per REDESIGN |
| LessonScreen | — | Kept for potential fullscreen use; not part of current main nav flow |

**Planned screen structure (REDESIGN — not yet implemented)**:
- `[s]` Study — merges Lessons + Practice; left=track tree, right=Lesson/Drills/Lick sub-tabs
- `[r]` Reference — spatial layout replacing two-tab Tools; key/scale selector + full-neck + quick panels
- `[a]` Analyze — reserved; placeholder until Songbook content is built
