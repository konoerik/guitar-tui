# Tasks

## Completed: M0 — Project Scaffold

- [x] Define architecture and diagram types (session 1)
- [x] Initialize uv project (`pyproject.toml`, `.python-version`)
- [x] Create directory structure
- [x] Write `CLAUDE.md`
- [x] Write `PERSONAS.md`
- [x] Write `ROADMAP.md`
- [x] Write `schemas/diagram_spec.md`
- [x] Write `schemas/lesson_format.md`
- [x] Verify uv install + textual hello world runs

---

## Completed: M1 — Data Layer

- [x] Define Pydantic model for chord voicings (`guitar_tui/loaders/models.py`)
- [x] Define Pydantic model for scale patterns (`guitar_tui/loaders/models.py`)
- [x] Populate `open_chords.yaml` (Am, A, Bm, C, D, Dm, E, Em, F, G)
- [x] Populate pentatonic minor scale — 5 positions
- [x] Write `guitar_tui/loaders/data_loader.py` with startup validation
- [x] Tests: loader validation (valid file, malformed file, missing required field)

## Completed: M2 — Diagram Engine

- [x] Finalize DiagramSpec Pydantic models (chord, scale, tab, fretboard variants)
- [x] Implement chord box renderer
- [x] Implement scale position renderer
- [x] Implement tab renderer
- [x] Implement static fretboard renderer
- [x] Implement diagram dispatcher
- [x] Tests: all renderer types with known inputs (85 engine tests, 104 total)

## Completed: M3 — Content Layer

- [x] Implement lesson parser (frontmatter + body) — `guitar_tui/loaders/lesson_loader.py`
- [x] Implement diagram block dispatcher (integrated in lesson parser via engine dispatcher)
- [x] Implement lesson index (`by_tag`, `by_difficulty`, `by_module`)
- [x] Write 2 stub lessons (`open_g_chord.md`, `minor_pentatonic_intro.md`)
- [x] Tests: parser, dispatcher, validation errors (42 tests, 146 total)

## Completed: M4 — TUI Application

- [x] Main navigation screen (`ui/screens/home.py` — TabbedContent, Lessons + Reference tabs)
- [x] Lesson viewer screen (`ui/screens/lesson.py` — TextBlock/DiagramBlock rendering)
- [x] Reference lookup screen (chord/scale Selects + live diagram in HomeScreen Reference tab)
- [x] Keyboard navigation + Footer bindings (q, l, r, Escape)
- [x] Stylesheet for all screens (`ui/app.tcss`)
- [x] Smoke tests: app mounts, lesson list populated, navigate to lesson and back (149 total)

## Completed: M4 follow-up — Engine/Schema items

- [x] FEAT-001: Tab measure grouping — `TabMeasure`, `measures` field on `TabLine`, bar lines in renderer
- [x] FEAT-002: Tab beat duration — `duration` field on `TabBeat`, column expansion
- [x] FEAT-004: Multiple chord voicings — `ChordEntry`, voicing selector in Reference tab
- [x] Updated `g_d_em_c_progression.md` tab diagram to use measures + duration

## Completed: Layout A — Two-panel split

- [x] Replace TabbedContent + ListView with Horizontal split layout
- [x] Left panel: collapsible Tree (lessons by module) + reference selects
- [x] Right panel: ContentSwitcher (welcome → inline lesson viewer)
- [x] Lesson viewer: TabbedContent with Lesson (live), Practice + References (placeholders)
- [x] Lesson loads inline via _show_lesson(); no longer pushes LessonScreen

## Upcoming: M5 — Interactive Features

- [ ] Rolling-window fretboard widget
- [ ] Interactive fretboard (note highlighting)
- [ ] Scale degree overlay on chord diagrams
- [ ] Position navigator for scale patterns

## Completed: M6 — Content Expansion (partial)

- [x] Reorganise lessons into track subdirectories (`01-orientation/` … `06-pentatonic-scale/`)
- [x] Update lesson loader to use `rglob` for recursive discovery
- [x] Track 1 — Orientation: 4/4 lessons complete
- [x] Track 2 — Open Chords: 10/10 lessons complete
- [x] Track 3 — First Progressions: 5/5 lessons complete (G–D–Em–C, C–G–Am–F, A–D–E, 12-Bar Blues in A, I–IV–V)
- [x] Track 6 — Pentatonic Scale: 5/9 lessons complete (positions 1–5)

## Completed: M6 — Content Expansion (second batch)

- [x] Track 6 — Pentatonic Scale: 9/9 lessons complete (connections, major pent intro, major vs minor, blues scale)
- [x] Track 4 — Theory Basics: 8/8 lessons complete
- [x] Track 5 — Barre Chords: 7/7 lessons complete
- [x] Data: barre_chords.yaml, seventh_chords.yaml, natural_minor.yaml, major.yaml, major_pentatonic.yaml, blues_scale.yaml

## Completed: M6 — Content Expansion (third batch)

- [x] Track 7 — Natural Minor: 7/7 lessons complete
- [x] Track 8 — Major Scale: 7/7 lessons complete
- [x] Track 9 — Seventh Chords: 5/5 lessons complete
- Total: 62 lessons across 9 tracks

## Upcoming: M6 — Content Expansion (remaining)

- [ ] Track 10 — Modes (6 lessons; requires mode scale YAML data)
- [ ] Track 11 — Song Analysis (9 lessons)
- [ ] Complete reference section
