# Backlog

Single source of truth for what to work on next. Items are ordered within each tier by estimated impact.
Milestone history lives in `TASKS.md`. Future milestone specs live in `ROADMAP.md`.

---

## Active — M6 wrap-up

- [x] Complete reference section — ✓ done — Reference tab now includes: intervals table, major scale interval formula, notes-per-string (open → 12th fret), diatonic chords for all 12 major keys (circle-of-fifths order); CAGED shapes and common-progressions-by-key deferred (require chord/fretboard diagram rendering)

---

## Tier 1 — Quick wins (data/infrastructure already exists)

Items where the content or data is in place but not surfaced or polished.

| # | Item | Area | Source |
|---|------|------|--------|
| 1 | Surface tunings reference in Tools screen | UI | ✓ done — Reference tab added to Tools screen |
| 2 | Add prerequisite note to welcome screen | UI | ✓ done |
| 3 | Add closing "What's Next" paragraph to lessons that end abruptly | Content | ✓ done — 60 lessons across Tracks 01–11 now have closing "What's Next" or "Where to Go From Here" sections |
| 3a | Review and rewrite lesson `summary` fields for reader-facing clarity | Content | ✓ done — 34 summaries rewritten across Tracks 1–9; now specific, hook-driven reader teasers |
| 4 | Add chord formula quick-reference | Tools / Content | Reviewer: maj, min, dom7, maj7, min7, dim, aug, sus2, sus4, add9 formulas in one view — ✓ done |

---

## Tier 2 — Medium effort, high impact

New views or content requiring moderate work; no new data layer needed.

| # | Item | Area | Source |
|---|------|------|--------|
| 5 | Add key signatures quick-reference | Tools / Content | ✓ done — combined with item 6 in Reference tab |
| 6 | Add circle of fifths reference | Tools | ✓ done — merged with key signatures; Reference tab shows all 12 keys in circle-of-fifths order with relative minor and accidentals |
| 7 | Make diatonic chord strip interactive | Tools / UI | ✓ done — , / . navigate chords; selected chord shows voicing diagram in right panel; diminished chords show "no voicing" gracefully |
| 8 | Add capo reference table | Tools / Content | ✓ done — Reference tab; capo frets 1–7 × 7 open shapes (E Em A Am D G C) → sounding chord |
| 9 | Design a proper Welcome screen | UI | ✓ done — three-zone layout: identity (pitch + prereq), curriculum arc (3 phases), navigation with new-user nudge |

> **Welcome screen design note**: The current screen is a stopgap — title, prereq note, and a nav menu. A proper welcome screen should establish the app's identity, summarise what's inside (tracks, scope, target audience), and guide first-time users toward a starting point. This is a UX design task before a coding task — content and layout should be agreed first. Coordinate with the Reviewer persona for first-impression feedback before implementing.

---

## Tier 3 — Scope additions

Content gaps that require new lessons or reference sections.

| # | Item | Area | Source |
|---|------|------|--------|
| 10 | Barre chord position finder | Tools / Content | ✓ done — Reference tab panel: note → E-shape fret (low E string) and A-shape fret (A string), computed from theory data |
| 11 | Rhythm and strumming patterns lesson | Content | ✓ done — Track 03 position 6; `strumming_basics.md`; covers D/U mechanics, ghost strums, four patterns (4-down, 3/4, D DU UDU, full 4/4) |

---

## Open bugs and engine feature requests

Tracked in detail in `BUGS.md`. Summarised here for prioritization.

| ID | Item | Priority | Notes |
|----|------|----------|-------|
| BUG-001 | Barre character `▬` right-aligned in chord cells (wide Unicode) | ~~Medium~~ | ✓ resolved — renders correctly in current terminal |
| BUG-002 | Tab key cycles within active tab instead of switching tabs | Low | ✓ resolved — `t` binding in ToolsMode cycles between Key View ↔ Reference tabs |
| BUG-003 | Tunings table columns misalign on accidentals (Eb, F#, etc.) | Low | ✓ resolved — switched to left-aligned columns in `_build_tunings_panel()` |
| FEAT-003 | Cross-reference system: `see_also` frontmatter + typed inline links | Medium | ✓ done (phase 1) — `see_also` field in frontmatter; loader warns on missing refs; lesson view appends "See Also" line. Typed inline links deferred. |
| FEAT-005 | Chord diagram: note labels and root distinction on dots | Medium | ✓ done — `dot_labels` (≤2 chars/string) overrides dot; `root_strings` (0-based indices) renders ◉ for root dots; both fields optional |
| FEAT-006 | Tab: rest notation (`rest: bool` on TabBeat) | Medium | ✓ done — `rest: true` renders `r` on all strings; label defaults to "rest" |
| FEAT-007 | Chord diagram: tuning-aware string labels | Low | Not needed until alternate tuning lessons are written |
| FEAT-008 | Theme-aware diagram colors | Low | ✓ done — `FullNeckWidget` now watches `App.dark` and switches between `_DARK_COLORS` / `_LIGHT_COLORS` palettes; `app.tcss` uses design tokens throughout so no TCSS changes needed |

---

## Persistent settings (implementation ready)

**Goal**: Store user preferences across sessions in a platform-appropriate config
file. Unblocks the inline block toggle state, last-lesson resume, and metronome
persistence.

**File location**: resolved by `platformdirs` (new dependency — small, well-maintained):
- macOS: `~/Library/Application Support/guitar-tui/settings.json`
- Linux: `~/.config/guitar-tui/settings.json`
- Windows: `%APPDATA%\guitar-tui\settings.json`

**Settings model** (`guitar_tui/settings.py`):
```python
class AppSettings(BaseModel):
    last_lesson: str | None = None
    compact_mode: bool = False
    collapsed_blocks: dict[str, list[str]] = {}  # lesson slug → collapsed block slugs
    metronome_bpm: int = 80
    metronome_time_sig: tuple[int, int] = (4, 4)
    reference_key: str = "C"
    reference_scale: str = "major"
```

**Behaviour:**
- Load on startup in `on_mount`; missing or corrupt file → default values, never a crash
- Validated by Pydantic on load — consistent with existing data layer pattern
- Write on meaningful events (lesson opened, mode toggled, BPM confirmed) — not on every keypress, not only on exit
- Settings path overridable via `GUITAR_TUI_CONFIG_DIR` env var for test isolation

**Work breakdown:**
- `guitar_tui/settings.py` — Pydantic model + `load()` / `save()` helpers: ~80 lines
- `pyproject.toml` — add `platformdirs>=4.0` to dependencies
- `guitar_tui/app.py` — load settings in `on_mount`, expose as `app.settings`
- Individual screens/widgets write back to `app.settings` and call `save()` on relevant events
- Total: ~110 lines across new + modified files

**Unblocks:**
- Inline block collapsed/expanded state (REDESIGN proposal)
- Last-lesson resume on startup
- Metronome BPM + time signature persistence
- Reference screen last-used key/scale persistence

**Owner**: Developer

---

## Metronome tool (implementation ready)

**Goal**: A visual metronome in the Reference screen — keeps the player in the app during practice sessions and makes odd time signatures readable.

**Scope**: Visual-only. No audio (platform fragmentation, added dependencies, asyncio jitter audible at high BPM). Audio is a future enhancement.

**Feature set:**
- BPM: 40–220, adjustable in +/-1 and +/-5 increments
- Time signature: numerator (2–12) × denominator (2, 4, 8, 16)
- Beat grouping for odd meters: user-configurable (e.g. 7/8 → 2+2+3 or 3+2+2 or 2+3+2); group separators shown visually
- Beat display: current beat highlighted (●), downbeat distinct, others dim (○)
- Tap tempo: two keypresses calculate BPM from interval
- Start/stop toggle

**Visual example (7/8, grouping 2+2+3, beat 5):**
```
  ○  ○  │  ○  ○  │  ○  ●  ○
  1  2  │  3  4  │  5  6  7      92 BPM
```

**Implementation:**
- `guitar_tui/ui/widgets/metronome.py` — `MetronomeWidget`, uses `set_interval(60 / bpm)`
- Timer attached to widget, not to screen — survives focus changes and intra-screen navigation
- Integrated into Reference screen (current Tools screen until redesign lands)
- ~150–180 lines Python + CSS; no new dependencies

**Future enhancement (not in scope now):** audio click via platform-specific subprocess (`afplay` macOS, `aplay` Linux); optional `bpm` field on exercise blocks that pre-sets the metronome when an exercise is opened.

**Owner**: Developer

---

## Lesson → lick cross-references (deferred)

**Goal**: Lessons can reference relevant licks from the library so readers are pointed toward the Practice screen at the right moment.

**Design decisions settled:**
- Identifier: lick slugs (already unique, filename-derived, stable) — no new ID system needed
- Schema: add `licks: list[str] = []` to `LessonMeta`, parallel to `see_also`
- Validation: app-level in `on_mount` after both loaders are loaded; warn on unknown slugs
- Display: a "Practice:" line at the bottom of the lesson after the See Also line, e.g. `Practice: Box 1 Ascending Run  ·  Bend and Release   [4]` — the `[4]` reminds the user which key opens Practice
- Use slugs in frontmatter (not titles) for robustness, consistent with `see_also`

**Work breakdown:**
- Developer: add `licks` field to `LessonMeta`, app-level validation, lesson screen rendering, update `schemas/lesson_format.md`
- Instructor: add `licks:` to ~10–12 relevant lessons (scale/mode/technique lessons with a direct corresponding phrase)

**Candidate lessons:**
`minor_pentatonic_intro`, `blues_scale`, `major_pentatonic_intro`, `natural_minor_intro`, `dorian_mode`, `phrygian_mode`, `lydian_mode`, `mixolydian_mode`, `twelve_bar_blues_a`, `pentatonic_connections`

---

## Terminal size recommendation (deferred)

**Goal**: Tell users the optimal terminal dimensions and warn gracefully if the current size is too small.

**Agreed approach**: Option 1 + 2 — static documentation of the recommended size, plus a non-blocking startup warning modal if the terminal is below the threshold.

**Implementation notes**:
- Recommended size should be determined empirically by running the app at different widths and finding where the overall layout (sidebar + content + padding) starts feeling cramped — the diagram width is likely not the binding constraint; the two-pane layouts (licks, tools key view) probably set the floor
- The startup warning should be a small dismissible modal (any key press), not a hard block; user can still proceed
- `self.app.size` in `on_mount` gives `(columns, rows)`; also handle `on_resize` if the terminal shrinks mid-session (show a persistent status-bar note, not a repeated modal)
- Welcome screen should document the recommended size in a brief note alongside the nav guide
- Threshold should be a named constant (e.g. `MIN_COLS`, `MIN_ROWS`) at the top of `app.py`, not a magic number

**Owner**: Developer (UI wiring) + manual testing pass to settle on the right numbers before adding the constant.

---

## Tier 3b — Content expansion (from 2026-03-11 review)

Gaps identified by the Reviewer for intermediate players. No infrastructure work required — purely new lick and lesson content.

| # | Item | Area | Notes |
|---|------|------|-------|
| C1 | Major scale licks (Track 08) | Content | Zero lick cross-references across 7 lessons. Most significant gap — major scale is essential for classic rock, country, pop lead. Need at least one phrase per position range (lower neck, upper neck). |
| C2 | Natural minor licks for positions 2–5 | Content | Only `natural_minor_descent` exists (covers pos 1 only). Upper-neck positions (3–5) have nothing. |
| C3 | Pentatonic licks for positions 3, 4, 5 | Content | Positions 1 and 2 are covered. Positions 3–5 unlinked — exactly where intermediate players get stuck breaking out of the box. |
| C4 | Expressive technique lessons | Content | Bending, vibrato, hammer-ons/pull-offs, slides are not taught anywhere. A short Techniques section (4–6 lessons) would address the intermediate plateau of knowing the right notes but not making them sound expressive. Candidate track: between Tracks 6 and 7, or as a standalone track. |

---

## Tier 4 — Future milestones

Larger scoped work tracked in `ROADMAP.md`. Listed here for backlog completeness.

| # | Item | Milestone | Notes |
|---|------|-----------|-------|
| 11 | Rolling-window fretboard, interactive note highlighting, scale degree overlay, position navigator | M5 | Full spec in ROADMAP.md |
| 12 | Theory Web — scale↔chord↔key relationships, multiple voicings per chord, progression builder | M7 | Full spec in ROADMAP.md |
| 13 | Song Analysis UI — guided workflow screen, songbook entries | M8 | Full spec in ROADMAP.md |
| 14 | Extended curriculum — jazz harmony, secondary dominants, borrowed chords, chord substitution | Post-M8 | Reviewer: advanced players hit the ceiling at Track 11 |

---

## Review history

| Date | File | App state |
|------|------|-----------|
| 2026-03-05 | [reviews/2026-03-05_reviewer_assessment.md](reviews/2026-03-05_reviewer_assessment.md) | M6 — 77 lessons, Tracks 1–11 |
| 2026-03-07 | [reviews/2026-03-07_reviewer_assessment.md](reviews/2026-03-07_reviewer_assessment.md) | M6 complete — 78 lessons, Practice screen (Exercises + Licks Library) |
| 2026-03-11 | [reviews/2026-03-11_reviewer_assessment.md](reviews/2026-03-11_reviewer_assessment.md) | Post-M6 UI redesign — card-panel nav, lick cross-references, pentatonic key view |
