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

## Upcoming: M2 — Diagram Engine

- [ ] Finalize DiagramSpec Pydantic models (chord, scale, tab, fretboard variants)
- [ ] Implement chord box renderer
- [ ] Implement tab renderer
- [ ] Implement static fretboard renderer
- [ ] Implement diagram dispatcher
- [ ] Tests: all renderer types with known inputs

## Upcoming: M3 — Content Layer

- [ ] Implement lesson parser (frontmatter + body)
- [ ] Implement diagram block dispatcher
- [ ] Implement lesson index
- [ ] Write 2 test lessons exercising parser and diagrams
- [ ] Tests: parser, dispatcher, validation errors

## Upcoming: M4 — TUI Application

- [ ] Main navigation screen
- [ ] Lesson viewer screen
- [ ] Reference lookup screen
- [ ] Keyboard navigation + Footer bindings
- [ ] Stylesheet for all screens

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
