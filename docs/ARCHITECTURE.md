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

### D10 — Diagram specs hard-fail on out-of-range notes; labels are the only note-name mechanism

**Date:** 2026-07-11
**Context:** The fretboard renderer silently dropped any highlight outside `fret_range`, and the scale renderer did the same for positions — the 2026-07-11 audit found a lesson diagram losing a note this way with no signal. Separately, `FretboardSpec.show_notes` was documented ("show note names in dots") but never implemented; content set it expecting behavior that labels were actually providing.
**Decision:** `FretboardSpec` (always) and `ScaleSpec` (when `fret_range` is explicit) validate range containment at model level — an out-of-range note raises `ValidationError` at load, consistent with the "startup failure over silent corruption" rule. `show_notes` was removed from the spec, renderer, content, and schema doc; explicit `label` fields (up to 2 chars, e.g. `"F#"`) are the single mechanism for note names.
**Alternatives considered:** Implementing `show_notes` by deriving note names from tuning — rejected because it would inject music knowledge into the music-agnostic engine. Renderer-side clamping/warnings — rejected as silent-ish; validation errors surface immediately during content authoring.
**Consequences:** Content authors must widen `fret_range` or remove the note; nothing renders partially. Pydantic ignores unknown fields, so stale `show_notes:` keys in external content would not break loading.

---

### D9 — Barre strings use the 1 = high e convention (matching ScaleNote/FretNote)

**Date:** 2026-07-11
**Context:** `BarreDef.from_string`/`to_string` were documented in `schemas/diagram_spec.md` as 1 = low E, and the chord renderer implemented that — but every partial barre actually authored (Bm, all A-shape voicings in `barre_chords.yaml`, Dm7's mini-barre) used 1 = high e, the standard guitar numbering already used by `ScaleNote.string` and `FretNote.string`. Full six-string barres masked the conflict; every partial barre rendered shifted onto the wrong strings, including across muted strings.
**Decision:** Strings in `BarreDef` are numbered 1 = high e … 6 = low E, like every other string-numbered field in the spec. The renderer maps string *n* to frets-array index `6 − n` (the frets array remains index 0 = low E). Schema doc corrected; regression tests pin the orientation.
**Alternatives considered:** Keeping the schema-as-written and rewriting all content — rejected: the content encoded the authors' (correct, conventional) intent; the doc was the artifact in error, and standard guitar string numbering should win.
**Consequences:** One spec-wide convention for string numbers (1 = high e) with a single documented exception: flat per-string *arrays* (`frets`, `fingers`, `dot_labels`, tab `notes`) run low-to-high by index. Any future string-numbered field must use the 1 = high e convention.

---

### D8 — Tab renderer: technique connectors produce a gap before the source note

**Date:** 2026-03-19
**Context:** Standard guitar tab writes hammer-ons, pull-offs, and slides by placing the technique character directly between two adjacent fret numbers — `5h8`, `8p5`, `5/9`. The tab renderer encodes these as two separate beats: beat 1 (the source note, plain) and beat 2 (the destination note, with `technique` replacing its leading dash). Beat 1 renders as `─5─` (with a trailing dash); beat 2 renders as `h8─`. Combined output is `─5─h8─`, which has a single `─` between `5` and `h` — a visible gap absent from strict traditional notation. Bends do not have this gap because `bend`/`bend_target` are suffixes on a single beat (`─5b7─`), so source and destination are encoded in one column.
**Decision:** Accept the gap as an inherent trade-off of the two-beat encoding for technique connectors. Do not add look-ahead logic to suppress beat 1's trailing dash when beat 2 carries a technique connector.
**Alternatives considered:** Look-ahead in `_render_tab_line` — when rendering beat N's trailing dash, check whether beat N+1 has a `technique` set and, if so, omit the trailing dash to produce `─5h8─`. This would require either a two-pass render or passing ahead context, adding complexity for a minor visual improvement. Rejected because `─5─h8─` is still readable and unambiguous to any guitarist familiar with tab.
**Consequences:** Bends (`5b7`) and technique connectors (`5h8`) are visually asymmetric — bends are compact, connectors have a gap. This is documented here so it is not mistaken for a bug. If look-ahead suppression is added in the future, existing tests in `TestTechniqueConnectors` would need to be updated. The gap does not affect correctness or readability in practice.

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
