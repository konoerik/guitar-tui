# Roadmap

## M0 — Project Scaffold ← current

**Goal**: Establish durable project foundation before any feature code.

**Key files**: `CLAUDE.md`, `PERSONAS.md`, `TASKS.md`, `ROADMAP.md`, `pyproject.toml`, `schemas/`

**Acceptance criteria**:
- `uv run python -c "import guitar_tui"` succeeds
- `uv run textual run guitar_tui/app.py` launches a blank Textual app without error
- All top-level docs exist and are coherent
- `schemas/diagram_spec.md` and `schemas/lesson_format.md` exist with complete specs
- `uv run pytest` passes (empty suite)

---

## M1 — Music Theory Data Layer

**Goal**: Define and populate the core music data: chord voicings and scale patterns in validated YAML.

**Key files**: `guitar_tui/data/chords/`, `guitar_tui/data/scales/`, `guitar_tui/loaders/data_loader.py`

**Deliverables**:
- Pydantic models for chord voicings and scale patterns
- YAML schema documented (in schemas or inline comments)
- At least 10 open chord voicings (Am, A, Bm, C, D, Dm, E, Em, F, G)
- Pentatonic minor scale — 5 positions (CAGED)
- Data loader with startup validation (hard error on invalid data)
- Tests for loader and validation

**Acceptance criteria**:
- All YAML validates against Pydantic models on load
- Loader raises a clear error for malformed files
- Test suite passes

---

## M2 — Diagram Engine

**Goal**: Build the music-agnostic rendering engine that converts DiagramSpec objects to Rich renderables.

**Key files**: `guitar_tui/engine/`, `schemas/diagram_spec.md`

**Deliverables**:
- `DiagramSpec` base model and type-specific variants
- Chord box renderer (grid, finger dots, open/mute markers, barre)
- Tab renderer (multi-string tab lines with timing marks)
- Fretboard renderer (static snapshot, highlighted notes)
- Dispatcher: given a DiagramSpec, return the correct renderer output
- Tests for each renderer type

**Acceptance criteria**:
- All renderers produce correct output for known inputs
- Engine has no imports from `guitar_tui.data` or `guitar_tui.content`
- Test coverage for all renderer code paths

---

## M3 — Content Layer

**Goal**: Parse lesson Markdown files, dispatch diagram blocks to the engine, and expose a clean API to the TUI.

**Key files**: `guitar_tui/loaders/lesson_loader.py`, `schemas/lesson_format.md`

**Deliverables**:
- Lesson parser: read frontmatter + body, validate required fields
- Diagram block dispatcher: detect fenced `diagram` blocks, parse YAML, call engine
- Lesson index: list available lessons, filter by tag/difficulty
- At least 2 complete lesson files to exercise the parser
- Tests for parser and dispatcher

**Acceptance criteria**:
- Parser correctly reads frontmatter and body for all test lessons
- Invalid frontmatter raises a clear validation error
- Diagram blocks dispatch to the correct engine renderer
- Test suite passes

---

## M4 — TUI Application

**Goal**: Wire the data, engine, and content layers into a navigable terminal application.

**Key files**: `guitar_tui/ui/screens/`, `guitar_tui/ui/widgets/`, `guitar_tui/ui/app.tcss`

**Deliverables**:
- Main navigation screen (lesson list + reference lookup)
- Lesson viewer screen (rendered lesson with embedded diagrams)
- Reference screen (chord/scale lookup by name)
- Keyboard navigation throughout
- Stylesheet for all screens and widgets

**Acceptance criteria**:
- User can browse and open a lesson end-to-end
- User can look up a chord or scale by name
- All keyboard shortcuts documented in Footer
- No crashes on navigation

---

## M5 — Interactive Features

**Goal**: Add dynamic fretboard and interactive diagram exploration.

**Deliverables**:
- Rolling-window fretboard widget (scrolls as position changes)
- Interactive fretboard: click/key to highlight notes by name or interval
- Scale degree overlay on chord diagrams
- Position navigator for multi-position scale patterns

**Acceptance criteria**:
- Rolling fretboard correctly maps notes to positions for standard tuning
- Interactive fretboard highlights correct notes for selected scale/key
- Position navigation cycles through all available positions

---

## M6 — Content Expansion

**Goal**: Build out a full first set of lesson modules with the Instructor persona.

**Deliverables**:
- Module 1: Open Chords (10 chords, strumming intro)
- Module 2: Barre Chords (E-shape, A-shape, CAGED intro)
- Module 3: Pentatonic Scale (5 positions, blues application)
- Module 4: Major Scale (patterns, modes intro)
- Module 5: Chord Progressions (I-IV-V, I-V-vi-IV, 12-bar blues)
- Reference section: complete open chord library, common scales

**Acceptance criteria**:
- All lessons parse and render without errors
- All diagram directives validate against schemas
- Lesson flow is pedagogically sequenced (prerequisites enforced)
