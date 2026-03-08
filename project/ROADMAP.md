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

---

## M7 — Theory Web

**Goal**: Transform the reference area from two independent lookups (chord, scale) into
an interconnected theory system where selecting any element reveals its musical context.

**Background**: A guitarist who knows a scale should immediately see which chords belong
to it, which progressions are idiomatic, and which positions cover the neck. Conversely,
selecting a chord should reveal which scales and keys it belongs to. This is the
information a learner needs to connect isolated knowledge into practical musicianship.

**Deliverables**:

*Data layer*
- Model scale-to-chord relationships (diatonic chord sets computed from interval formulas)
- Model chord-to-key membership (which keys/scales contain this chord)
- Multiple voicings per chord name (FEAT-004)
- Scale transposition support (DECISIONS.md D5 deferral resolved here)

*UI — Scale View*
- Select a scale → show all 5 positions (navigable, not just position 1)
- Diatonic chord panel: the chords built from that scale, with chord diagrams
- Common progressions panel: typical I-IV-V, I-vi-IV-V etc. for the selected key
- Cross-references to lessons, artists, and songs that feature this scale

*UI — Chord View*
- Select a chord → show all voicings (open, barre positions) — FEAT-004
- Keys/scales this chord belongs to (e.g. Am belongs to C major, A minor, D minor...)
- Common chord functions (tonic, subdominant, dominant) in those keys
- Cross-references to progressions and lessons

*UI — Progression Builder (stretch goal)*
- Select a key → see all diatonic chords laid out
- Click chords to build a progression and see it rendered as a tab diagram

**Acceptance criteria**:
- Selecting a scale shows its diatonic chords with diagrams
- Selecting a chord shows which keys/scales it belongs to
- All positions of a scale are navigable from the scale view
- All voicings of a chord are accessible from the chord view
- Cross-references to lessons and content are populated

---

## M8 — Song Analysis

**Goal**: Give the learner a systematic method for figuring out how to play a song —
finding the key, identifying the scale, mapping the chord progression — and an
interactive tool that guides the process.

**Background**: The endpoint of learning guitar theory is applying it to real music.
A learner who can navigate the Theory Web (M7) has all the pieces; M8 teaches them
the analytical process for using those pieces on an unfamiliar song. This is the
"flip side" of the reference: instead of browsing known theory, the learner starts
from a song and works backwards to the theory.

**Deliverables**:

*Instructor — Song Analysis track (see CURRICULUM.md)*
- Lessons on finding a song's key by ear and by chord recognition
- Lessons on identifying major vs. minor tonality
- Lessons on mapping progressions to Roman numerals
- Lessons on choosing the right scale for a given key/feel
- Lessons on using the Theory Web as an analytical tool

*Developer — Analysis workflow UI*
- "Analyse a Song" guided screen: user inputs a key and mode (major/minor), the UI
  surfaces the relevant scale, diatonic chords, common progressions, and suggested
  scale positions — all linked to lessons
- This is the Theory Web (M7) used in reverse: start from what you hear, arrive at
  the theory

*Developer — Songbook area (see IDEAS.md)*
- Each Songbook entry demonstrates the analysis methodology applied to a real song
- Links back to the relevant Theory Web entries (scale, chords, progressions)

**Acceptance criteria**:
- Song Analysis lesson track is complete and sequenced
- Analysis workflow UI accepts a key + mode and returns theory context
- At least three Songbook entries exist demonstrating the methodology
- Songbook entries link correctly to scale, chord, and lesson content
