# Plan

## Active
<!-- Current sprint items. Keep this short — 5-10 items max.
     If it grows beyond that, move lower-priority items to Backlog. -->

### Open decisions

- `uv.lock` in `.gitignore` — commit before PyPI release for reproducible contributor/CI installs.

### M8 — Theory Web

- Scale view: select scale → all 5 positions (navigable) + diatonic chord panel (with diagrams) + common progressions + cross-references to lessons
- Chord view: select chord → all voicings + keys/scales it belongs to + chord function in those keys + cross-references
- Song Analysis workflow UI: key + mode → scale, diatonic chords, common progressions, suggested positions, links to lessons and Theory Web
- Data layer: model scale-to-chord relationships (diatonic chord sets from interval formulas); chord-to-key membership; scale transposition support

### Infrastructure

- Persistent settings (`platformdirs`, `AppSettings` Pydantic model in `guitar_tui/settings.py`) — unblocks inline block toggle state, last-lesson resume, metronome BPM persistence, reference key/scale persistence
- Inline content blocks — `exercise` and `lick` slug references in lesson Markdown; two-pass loading (loaders independent, resolved in `on_mount`); evaluate alongside Study screen redesign before implementing

### Content gaps (Tier 3b) — staged

**Stage 1** (highest value, no new notation or infrastructure needed):
- Track 14 core (4 lessons): `subdivisions`, `syncopation`, `sixteenth_strumming`, `palm_muting` — D/U labels + `rest: true` + `caption:` covers everything; palm muting uses `caption:` + prose workaround
- Track 13 core (3 lessons): `phrase_shape`, `question_and_answer`, `space_and_silence`

**Stage 2** (complete both technique-adjacent tracks):
- Track 13 remaining (3 lessons): `motif_development`, `rhythmic_placement`, `building_a_solo`
- Track 14 remaining (2 lessons): `ghost_strokes`, `rhythm_in_leads`
- Track 13–14 exercises (~7) and licks (~5–7)

**Stage 3** (ear training — constrained by no-audio):
- Track 15 (5 lessons): ear training guide; explicit about app limitation; looper-as-ear-training format
- Optional: add `listening_exercise:` Markdown section convention to lick files (no engine change)

**Stage 4** (world sounds — requires new YAML data files):
- Track 16 — Sounds and Scales Around the World (6 lessons): harmonic minor, Phrygian dominant, Hungarian minor, whole tone, diminished, Japanese pentatonic
- Data prerequisites: ~6 new scale YAML files before lessons can be written
- 1 lick per lesson (looper-ready, captures characteristic phrase shape of each tradition)




### Release

- PyPI publication: `uv build` + install smoke test → `uv publish`; update README install instructions from `git+https://...` to `uv tool install guitar-tui`

### Low priority

- FEAT-007: chord diagram tuning-aware string labels — not needed until alternate tuning lessons are written
- **Tab renderer: suppress trailing dash before technique connector** — `─5─h8─` has a gap that `─5b7─` does not (ADR-D8). Fix approach: second pass over the rendered staff rows — after all beats are written, scan each string row for `─` immediately before `h`/`p`/`/`/`\` and remove it. Requires no look-ahead during render; operates on the completed string. Update `TestTechniqueConnectors` tests if implemented.
- Thumb notation — `fingers` accepts integers 1–4 only; classical/fingerstyle thumb (T) not supported; no planned lesson requires it
- Multi-barre chords — `ChordSpec.barre` is a single `BarreDef`; advanced jazz voicings with two independent partial barres not supported
- Metronome audio click (afplay macOS / aplay Linux) — deferred; platform fragmentation and asyncio jitter at high BPM
- Lesson → lick cross-references: `licks:` field already in REDESIGN Step 1; typed inline links (`[lesson:slug]`) deferred

### Future ideas — Audio (reevaluate as a single feature milestone)

If audio is added, implement it as one coherent feature rather than piecemeal — one library (`miniaudio`) covers all use cases. Adding audio only for the metronome and revisiting later risks doing the dependency and architecture work twice.

**Use cases in priority order:**
- **Metronome click** — high/low PCM click; precision-timed dedicated thread (not asyncio); graceful degradation when no audio device
- **Tuning reference tones** — 6 sustained sine waves (E2 A2 D3 G3 B3 E4); simple but high value for beginners
- **Interval demonstration** — two simultaneous tones; directly supports ear training (Track 15) and intervals lesson (Track 4); closes the biggest gap in audio-dependent pedagogy
- **Scale/lick playback** — sequential tones from tab fret+string data using `f = 82.41 × 2^(n/12)`; sine waves for simplicity, sampled guitar for quality (samples are larger to bundle)
- **Chord playback** — polyphonic; useful for harmony/seventh chord lessons

**Architecture notes:**
- All pitched content generated programmatically from frequency formula — no sample files needed except click WAVs
- Dedicated audio thread with `time.perf_counter()` for metronome timing — separate from Textual event loop
- Graceful degradation required: app must function fully without audio (SSH, headless, CI)
- Audio files (click WAVs if bundled) must live inside `guitar_tui/` — hatchling includes them in the wheel
- Adds `miniaudio` as 5th dependency; justified by breadth of use across metronome, tuning, ear training, and playback

**Estimated effort:** ~20–30 hrs total for all use cases together; ~14–19 hrs for metronome alone (see Developer notes from 2026-03-21 session). Doing it once for all use cases is significantly more efficient than staged additions.

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
- Bend notation in tab renderer: `bend`/`bend_target`/`vibrato` suffixes + `technique` connectors (`h`, `p`, `/`, `\`) on `TabBeat`; col_width auto-expands for suffix length; 30 new tests ✓
- Track 12 — Expressive Techniques: 5 lessons (string_bending, vibrato_technique, hammer_ons_pull_offs, slides, combining_techniques) + 2 licks; label convention (Option A) applied; slide notation bug fixed; spider exercise corrected ✓
- Two-row collision-detection label system in tab renderer; Option A label convention documented in `schemas/diagram_spec.md`; ADR-D8 recorded ✓
- Label convention sweep: refined to contextual rules; swept 45 files (14 exercises, 25 licks, 6 lessons); D/U preserved in `alternate_picking.md` ✓
- Persistent settings wired: BPM persists on every change (not just stop); last lesson restored on re-open; `action_back` clears saved lesson ✓
- Track progress indicator `[3 / 9]` in lesson border title ✓
