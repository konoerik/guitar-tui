# Roadmap
<!-- Load only when explicitly discussing goals or priorities.
     This is a high-level document — avoid granular tasks here, those belong in PLAN.md. -->

## Goal

Guitar TUI teaches guitar music theory interactively in the terminal. Success means a complete curriculum covering open chords through modes and song analysis, an interconnected theory reference (Theory Web) where selecting any element surfaces its musical context, and a practice system with exercises and a licks library — all navigable without leaving the keyboard. The app installs via `uv tool install`, requires no configuration, and runs anywhere a modern terminal does.

## Phases

### Phase 1: Core (M0–M4) ✓ Complete
Data layer (YAML chord/scale data, Pydantic validation), diagram engine (chord, scale, tab, fretboard renderers), lesson content parser, and TUI application wired together end-to-end. Two-panel split layout with inline lesson viewer.

### Phase 2: Curriculum (M5–M7) ✓ Complete
78 lessons across 11 tracks (Orientation through Song Analysis), full-neck scale display, Practice screen (exercises + licks library), complete reference section, UI redesign groundwork, and public GitHub release. 230 tests.

### Phase 3: Theory Web + UI Redesign (M8)
Transform the reference area into an interconnected theory system: scale → diatonic chords → common progressions → positions; chord → voicings → keys/scales → lessons. Song Analysis workflow UI (key + mode → full theory context). Parallel: Study/Reference screen restructure per REDESIGN spec in PLAN.md.

### Phase 4: Extended Content (Post-M8)
Songbook (theory breakdowns of real songs), Artist profiles (style vocabulary + original exercises), additional licks for underserved positions, expressive techniques track (bending, vibrato, hammer-ons, slides), advanced harmony (jazz, secondary dominants, borrowed chords).

## Out of Scope

- No binary bundling (PyInstaller/Nuitka) — Textual incompatibility, wrong audience
- No audio playback — platform fragmentation and asyncio jitter at high BPM
- No user-configurable content paths — no plugin system in initial implementation
- No tab transcription or reproduction of copyrighted note sequences
- No backwards-compatibility for Python < 3.12

## Deployment Constraints

Standing rules that apply to all future implementation work:

- **Primary install path**: `uv tool install guitar-tui`; pipx and pip work but are not the first recommendation
- **Data files inside the package**: content (lessons, exercises, licks), YAML data, and `app.tcss` must stay under `guitar_tui/` — hatchling includes them in the wheel automatically; never move content outside the package directory
- **Minimal dependencies**: current four (textual, pyyaml, python-frontmatter, pydantic) cover everything; new dependencies require justification
- **Versioning**: `0.1.x` = bug fixes and content additions; `0.2.0` = next significant feature milestone; `1.0.0` = curriculum complete and UI stable
