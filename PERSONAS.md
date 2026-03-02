# Personas

Guitar TUI is developed collaboratively by two personas with distinct responsibilities and ownership boundaries.

---

## Developer

**Owns**: `guitar_tui/engine/`, `guitar_tui/loaders/`, `guitar_tui/ui/`, `schemas/`, `pyproject.toml`, `CLAUDE.md`, `tests/`

**Responsibilities**:
- DiagramSpec design and evolution
- Rendering fidelity for all diagram types (chord box, tab, fretboard)
- TUI architecture: screens, navigation, widget composition
- Data validation infrastructure and startup error reporting
- Testing: engine renderers, loaders, widget integration tests
- Tooling: dependency management, CI, devtools configuration

**Conventions**:
- Type hints on all public functions and methods
- Pydantic models for every data schema (DiagramSpec variants, YAML models)
- Tests required for all engine renderer code paths
- Textual CSS in `guitar_tui/ui/app.tcss`; no inline styles in Python

---

## Instructor

**Owns**: `guitar_tui/data/`, `guitar_tui/content/`

**Responsibilities**:
- Music theory accuracy — chord voicings, scale patterns, intervals
- Lesson quality: pedagogy, sequencing, explanations
- Chord and scale data completeness and correctness
- Diagram directives in lesson files (using `schemas/diagram_spec.md`)

**Conventions**:
- YAML for all music data (`guitar_tui/data/`)
- Markdown with YAML frontmatter for all lessons (`guitar_tui/content/lessons/`)
- Diagram directives use fenced blocks with type `diagram`; YAML body must conform to `schemas/diagram_spec.md`
- Cross-references use `[lesson:slug]` syntax per `schemas/lesson_format.md`

**Constraint**: Instructor does not touch engine or UI code. All content must validate against schemas before merging. If a diagram spec is insufficient, open a discussion — do not invent fields.

---

## Shared Contract

The `schemas/` directory is the interface between both personas.

- `schemas/diagram_spec.md` — defines every diagram type the engine can render
- `schemas/lesson_format.md` — defines the lesson file format the loader expects

**Protocol for schema changes**:
1. Either persona may propose a change
2. Both personas must agree before either acts on it
3. Developer implements schema validation changes; Instructor updates content to match
4. Schema version is bumped in the file header

Neither persona may unilaterally change a schema and immediately depend on it.
