# Plan

## Active
<!-- Current sprint items. Keep this short — 5-10 items max.
     If it grows beyond that, move lower-priority items to Backlog. -->

### Open decisions

- `uv.lock` in `.gitignore` — currently ignored; removing gives reproducible installs. Decide before next release.
- Track progress indicator (`3 / 9`) in lesson header — low effort; useful context for learners.

### M8 — Theory Web

- Scale view: select scale → all 5 positions (navigable) + diatonic chord panel (with diagrams) + common progressions + cross-references to lessons
- Chord view: select chord → all voicings + keys/scales it belongs to + chord function in those keys + cross-references
- Song Analysis workflow UI: key + mode → scale, diatonic chords, common progressions, suggested positions, links to lessons and Theory Web
- Data layer: model scale-to-chord relationships (diatonic chord sets from interval formulas); chord-to-key membership; scale transposition support

### Infrastructure

- Persistent settings (`platformdirs`, `AppSettings` Pydantic model in `guitar_tui/settings.py`) — unblocks inline block toggle state, last-lesson resume, metronome BPM persistence, reference key/scale persistence
- Inline content blocks — `exercise` and `lick` slug references in lesson Markdown; two-pass loading (loaders independent, resolved in `on_mount`); evaluate alongside Study screen redesign before implementing

### Content gaps (Tier 3b)

- Expressive techniques lessons — bending, vibrato, hammer-ons/pull-offs, slides; candidate track between Tracks 6 and 7 (4–6 lessons)

### Release

- Screenshot or screen recording in README — ASCII art chord grid is a placeholder; a real screenshot would dramatically improve first impressions
- PyPI publication: `uv build` + install smoke test → `uv publish`; update README install instructions from `git+https://...` to `uv tool install guitar-tui`

### Low priority

- FEAT-007: chord diagram tuning-aware string labels — not needed until alternate tuning lessons are written
- Thumb notation — `fingers` accepts integers 1–4 only; classical/fingerstyle thumb (T) not supported; no planned lesson requires it
- Multi-barre chords — `ChordSpec.barre` is a single `BarreDef`; advanced jazz voicings with two independent partial barres not supported
- Metronome audio click (afplay macOS / aplay Linux) — deferred; platform fragmentation and asyncio jitter at high BPM
- Lesson → lick cross-references: `licks:` field already in REDESIGN Step 1; typed inline links (`[lesson:slug]`) deferred

### Future ideas (post-M8)

- Songbook area — theory breakdowns of real songs (key, mode, progression, scale, technique; no copyrighted note sequences). Candidates: Sultans of Swing, Wonderful Tonight, House of the Rising Sun, Wish You Were Here, Knockin' on Heaven's Door
- Artist area — style profiles with original licks and exercises. Candidates: Knopfler, Clapton, Hendrix, BB King, Gilmour
- Styles area — genre-organized theory profiles (Blues, Rock, Jazz, Country, Funk, Classical Fingerstyle)
- Chord Builder / Interval Explorer — interactive utility; root + intervals → chord name; evaluates whether fretboard-based or abstract interval builder
- Prev/next lesson navigation shortcuts — not planned; tree click is sufficient
- Numerical lesson navigation — jump to lesson by number from lesson picker
- Advanced harmony — jazz, secondary dominants, borrowed chords, chord substitution (post-M8 curriculum extension)


## Done
<!-- Completed items land here temporarily.
     The stop hook archives these to .claude/archive/YYYY-MM.md and clears this section. -->

- M0 — Project Scaffold: uv project, CLAUDE.md, schemas, hello-world app ✓
- M1 — Data Layer: Pydantic chord/scale models, YAML data, startup validation, tests ✓
- M2 — Diagram Engine: chord/scale/tab/fretboard renderers, dispatcher, 85 engine tests ✓
- M3 — Content Layer: lesson parser, diagram block dispatcher, lesson index, 42 tests ✓
- M4 — TUI Application: HomeScreen, LessonScreen, Reference tab, keyboard nav, stylesheet, smoke tests ✓
- M4 follow-up: tab measures + beat duration, multiple chord voicings (ChordEntry), FEAT-001/002/004 ✓
- Layout A — Two-panel split: Tree navigator, ContentSwitcher, inline lesson viewer ✓
- M5 — Interactive Features (partial): full-neck FullNeckWidget, position navigation, theme-aware colors ✓
- M6 — Content Expansion: 78 lessons across 11 tracks, Practice screen, reference section, barre position finder ✓
- Post-M6 — Tier 1–3 additions: strumming basics, FEAT-003/005/006/008, welcome screen redesign, diatonic chord strip interactive ✓
- M7 — Polish and Release: metronome widget, terminal size warning, lick cross-references (`licks:` frontmatter), US English sweep, GitHub live, 230 tests ✓
- REDESIGN Step 1 (Instructor): added `licks:` to 12 lessons; authored 9 lick files; all exercises complete ✓
- REDESIGN (complete): Exercises + Licks tabs in lesson view, contextual filtering, lick library in Practice screen; `[1]–[4]` nav retained; Tools screen kept as-is ✓
