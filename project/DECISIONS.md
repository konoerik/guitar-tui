# Architecture Decision Log

Rationale for key decisions made during planning. Read this before questioning an established pattern — the trade-offs were considered. If a decision needs revisiting, note it here first.

---

## D1 — Music-agnostic engine

**Decision**: The engine (`guitar_tui/engine/`) renders DiagramSpec objects and has no knowledge of music theory. It does not know what a G chord is, what intervals a pentatonic scale contains, or what strings are standard-tuned to.

**Rationale**: Coupling rendering logic to music knowledge makes both harder to change. If the engine knows chord theory, changing a voicing requires touching rendering code. Keeping them separate means the engine can be tested with arbitrary coordinate data, and music data can be corrected without risking rendering regressions. The engine is also reusable for any stringed instrument — it just renders grids and dots.

**Consequence**: All music knowledge lives in `guitar_tui/data/` (YAML) and `guitar_tui/content/` (lessons). The engine receives fully-resolved DiagramSpec objects from the loader layer — it never reads YAML directly.

---

## D2 — YAML for music data

**Decision**: Chord voicings, scale patterns, and tunings are stored as YAML files in `guitar_tui/data/`.

**Alternatives considered**:
- **SQLite** — rejected; adds query complexity and a schema migration story for what is essentially a static reference library. Overkill for read-only data.
- **JSON** — rejected; YAML is more readable for humans editing music data (the Instructor persona), handles comments, and handles multiline strings more gracefully.
- **Python literals** — rejected; hard-coding data in Python files blurs the data/code boundary and makes the Instructor persona impossible.

**Consequence**: Data is version-controlled alongside code, human-editable without tooling, and validated at startup by Pydantic rather than at query time.

---

## D3 — Markdown + YAML frontmatter for lessons

**Decision**: Lessons are `.md` files with YAML frontmatter (via `python-frontmatter`) and fenced `diagram` code blocks for embedded diagrams.

**Alternatives considered**:
- **Pure YAML** — rejected; lesson prose is better written in Markdown than as YAML string literals. Authoring experience matters for the Instructor.
- **reStructuredText** — rejected; less familiar than Markdown, heavier tooling requirements, no clear advantage for this use case.
- **Custom DSL** — rejected; unnecessary complexity. Markdown is readable outside the app (GitHub, VS Code, Obsidian), reducing the Instructor's dependency on the TUI being runnable.

**Consequence**: Lessons are readable and editable without running the app. The `diagram` fenced block is the only non-standard Markdown extension — everything else is plain GFM.

---

## D4 — Pydantic for schema validation

**Decision**: All data schemas — DiagramSpec variants, chord/scale YAML models — are defined as Pydantic v2 models.

**Alternatives considered**:
- **dataclasses** — rejected; no built-in validation, requires manual type coercion from YAML dicts.
- **TypedDict** — rejected; structural typing only, no runtime validation.
- **JSON Schema + jsonschema library** — rejected; requires maintaining a separate schema file and validation library alongside Python types. Pydantic unifies both.

**Consequence**: Validation errors are descriptive and field-specific. The Pydantic model is the single source of truth for what constitutes valid data — no separate schema files needed for the data layer.

---

## D5 — Bottom-up build order

**Decision**: Implementation proceeds Data → Engine → Content → TUI (M1 → M2 → M3 → M4).

**Rationale**: Each layer's API is the contract for the layer above. Building top-down would require mocking lower layers, then replacing the mocks — doing the work twice. Building bottom-up means each layer is real and tested before it is depended upon. The TUI is the thinnest layer; it should be assembled last from proven components.

**Consequence**: There is no visible UI until M4. This is intentional. Early milestones produce tested library code, not demos.

---

## D6 — Embedded content, no user content path

**Decision**: All lesson content and music data is bundled with the application. There is no mechanism for users to add their own lessons or chord libraries in the initial implementation.

**Rationale**: User-configurable content paths add path resolution, validation, merge conflict, and error reporting complexity that is not warranted before the core experience is proven. The target user is a single guitarist, not a platform.

**Consequence**: Content is version-controlled. Adding new lessons means contributing to the repository. This can be revisited post-M6 if needed.

---

## D7 — Textual as the TUI framework

**Decision**: The application is built on [Textual](https://textual.textualize.io/) (not urwid, blessed, curtsies, or raw curses).

**Rationale**: Textual provides a component model (widgets, screens, CSS styling) that maps well to the application's structure. It has active development, good documentation, async-native design (required for responsive UI), and built-in devtools. The Rich library (bundled with Textual) handles all styled terminal output in the engine layer.

**Consequence**: The minimum Python version is 3.12 (Textual's async features work best there). The CSS-based styling system (`app.tcss`) is Textual-specific — it is not transferable to other frameworks.
