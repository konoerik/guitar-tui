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

## Completed: M6 — Content Expansion (fourth batch)

- [x] Track 10 — Modes: 6/6 lessons complete (intro, Dorian, Phrygian, Lydian, Mixolydian, in context)
- [x] Data: dorian.yaml, phrygian.yaml, lydian.yaml, mixolydian.yaml
- [x] Track 11 — Song Analysis: 9/9 lessons complete
- [x] index.yaml updated with Modes and Song Analysis tracks
- Total: 77 lessons across 11 tracks

## Completed: Post-M6 — Tier 3 content additions

- [x] `strumming_basics.md` — Track 03 position 6; D/U mechanics, ghost strums, 4 essential strumming patterns; 78th lesson in curriculum
- [x] Barre chord position finder — Reference tab panel; root note → E-shape fret (low E) and A-shape fret (A string) for all 12 notes; computed from `note_to_semitone()`

## Completed: M6 — Content Expansion (reference section)

- [x] Reference tab: intervals table (name / semitones / symbol)
- [x] Reference tab: major scale interval formula (W W H W W W H pattern + C major example)
- [x] Reference tab: notes on each string — open to 12th fret (all 6 strings)
- [x] Reference tab: diatonic chords for all 12 major keys (circle-of-fifths order)
- Deferred: CAGED shapes and common-progressions-by-key (require chord/fretboard diagram rendering — developer scope, post-M6)
