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

## Upcoming: M5 — Interactive Features

- [ ] Rolling-window fretboard widget
- [ ] Interactive fretboard (note highlighting)
- [ ] Scale degree overlay on chord diagrams
- [ ] Position navigator for scale patterns

## Upcoming: M6 — Content Expansion

> **Note**: This section is a placeholder. The Instructor should expand it into individual lesson tasks once M2 is complete and the DiagramSpec is locked. Each task should include the lesson slug, which diagram types it uses, and its prerequisites.

- [ ] Instructor: scope and expand this section (do after M2 is done)
- [ ] Module 1: Open Chords
- [ ] Module 2: Barre Chords
- [ ] Module 3: Pentatonic Scale
- [ ] Module 4: Major Scale
- [ ] Module 5: Chord Progressions
- [ ] Complete reference section
