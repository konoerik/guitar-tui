# Guitar TUI — Claude Context

## Project

Guitar TUI is a Python terminal application built with Textual that teaches guitar music theory interactively. It presents chord diagrams, scale patterns, fretboard visualizations, and structured lessons entirely within the terminal. The application is designed for guitarists who prefer keyboard-driven tools and want a fast, distraction-free reference for theory concepts.

## Architecture

Four-layer model, built bottom-up:

```
Data Layer      guitar_tui/data/        YAML chord/scale data, tunings
Engine Layer    guitar_tui/engine/      DiagramSpec renderers (music-agnostic)
Content Layer   guitar_tui/loaders/     Lesson parser, diagram block dispatcher
TUI Layer       guitar_tui/ui/          Screens, widgets, stylesheet
```

**Critical rule**: the engine is music-agnostic. It renders DiagramSpec objects — it does not know chord names or scale theory. Music knowledge lives exclusively in the data layer and lesson content.

**Data validation**: the data loader validates all YAML files against Pydantic schemas on startup. Invalid data is a hard error, not a warning.

**Schema contract**: `schemas/` defines the interface between the Developer and Instructor personas. Both must agree on schema changes before acting.

**Diagram taxonomy**: `schemas/diagram_taxonomy.md` — full catalog of all diagram types (Groups A–F) identified during planning, with M2 scope vs. deferred notes. Read before implementing any new renderer.

## Personas

Two distinct roles share this codebase. See [PERSONAS.md](PERSONAS.md) for full details.

- **Developer** — owns engine, loaders, UI, schemas, tooling
- **Instructor** — owns `guitar_tui/data/` and `guitar_tui/content/`

## Key Commands

Prefer `make` targets — they wrap `uv run` and are the canonical interface:

```bash
make setup    # uv sync — install / refresh dependencies
make run      # launch the application
make dev      # launch with Textual devtools (live reload + inspector)
make test     # run the test suite
make check    # verify the package is importable
make clean    # remove .venv, caches, build artifacts
make build    # build distribution packages (future)
```

Raw `uv run` equivalents if needed:
```bash
uv run guitar-tui
uv run pytest
uv run textual run --dev guitar_tui/app.py
```

## Conventions

- **Python**: type hints on all functions, Pydantic models for all data schemas
- **Data files**: YAML for music data (`guitar_tui/data/`), Markdown+YAML frontmatter for lessons (`guitar_tui/content/lessons/`)
- **Naming**: `snake_case` for files and identifiers; diagram types use lowercase strings (`"chord"`, `"scale"`, `"tab"`, `"fretboard"`)
- **Diagram directives**: fenced code blocks with type `diagram` in lesson Markdown; YAML body per `schemas/diagram_spec.md`
- **Tests**: all engine renderers require tests; use `pytest-asyncio` for Textual widget tests

## Session Resumption

1. Read `TASKS.md` — find the current milestone and next unchecked task
2. Read `ROADMAP.md` — review the current milestone's acceptance criteria
3. Check `schemas/` if working on content or engine boundary code
4. Check `DECISIONS.md` before questioning an established pattern — the trade-offs were considered during planning

## Critical Rules

- Engine renders DiagramSpec objects only — never raw chord/scale data
- Data layer validates on startup; startup failure is acceptable, silent corruption is not
- `schemas/` is the dev-instructor contract; no unilateral changes
- Instructor does not modify engine or UI code
- Developer does not curate lesson content or decide music theory accuracy
