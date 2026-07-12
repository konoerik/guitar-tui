# Plan

## Active
<!-- Current sprint items. Keep this short — 5-10 items max.
     If it grows beyond that, move lower-priority items to Backlog. -->

### Agreed order of work (2026-07-11, post-audit review)

1. **M8 Theory Web** — fold Track 16's 6 new scale YAML files in as scale-view test material;
   revisit the Exercises-tab redesign decision (Infrastructure below) before or alongside
2. **Track 15 (ear training) last** — value capped until/unless the audio milestone happens

### M8 — Theory Web

- [x] Data layer (2026-07-12, ADR D11): `theory/web.py` (chord_memberships, realize_progression, transposition helpers); `data/progressions.yaml` (16 progressions, validated vs degree tables at startup, `schemas/progression_format.md`); `theory_refs` lesson frontmatter + reverse index (35 lessons tagged)
- [x] Scale view (2026-07-12) — shipped as Key View extension: positions navigable (existed), diatonic chord strip (existed), + progressions realized in key + lesson cross-refs (`#key-related` panel); 6 world scales selectable (harmonic minor + Phrygian dominant with full degree tables incl. augmented chords; symmetric/gapped scales show "(no diatonic chord set)")
- [x] Track 16 scale YAML (2026-07-12): 6 files generated from interval formulas (`harmonic_minor`, `phrygian_dominant`, `hungarian_minor`, `whole_tone`, `diminished`, `hirajoshi`), verified by content suite; Track 16 *lessons* still to write (Stage 4 below)
- [x] Chord view (2026-07-12): all voicings side by side (+ labels), spelled tones, key functions as an OptionList (Enter jumps to Key View landing on the chord's strip slot), tagged lessons; `g` in Key View opens the current chord; `backspace` pops the navigation history stack
- [x] Song Analysis workflow UI (2026-07-12): key + quality → scale, transposed position spans (suggests lowest), key context, diatonic chords, progressions realized in key, lessons; "Explore" links into Key View / Chord View with history back

### Bugs

- [x] **Key View neck overflow** — fixed 2026-07-12: `#chord-row` capped at 55% + `#key-content`
  min-height 12; regression test pins zero neck scroll down to MIN_COLS×MIN_ROWS.

### Infrastructure

- **Evaluate line wraps in lesson prose** — this is a TUI: the Markdown/Static widgets wrap text
  to widget width, and the size warning already guarantees ≥110 cols for tables/diagrams. There is
  therefore no reason for content to fight "runaway sentences" — prose can be written naturally and
  wrap. Audit: (a) whether any rendered surface fails to wrap (diagram captions inside rendered
  Text, Static summaries, welcome/info cards); (b) whether source-file hard-wrapping conventions
  (some files ~75-col wrapped, some single-line paragraphs) have any rendering effect, and settle
  on one authoring convention for content files.
- **Tools section improvements** (evaluated 2026-07-11; correctness fixes shipped same day —
  enharmonic chord lookup, 12 moveable diminished voicings, chord-tone fallback). Remaining:
  - [x] **Key View enhancements** (2026-07-12): voicing cycling (`v` key, 24 multi-voicing
    chords); context line above the neck; characteristic note (◆) for modes, blues, and the
    harmonic-minor family
  - [x] **Reference-tables visual overhaul** (2026-07-12): shared theme-aware palette in
    `guitar_tui/ui/styles.py` (also used by full_neck); quality-colored Diatonic Chords table
    with legend; Notes-on-Strings with dimmed accidentals + highlighted inlay frets; Chord
    Formulas regrouped (Triads/Sevenths/Sus/Power) with altered degrees highlighted; new
    Circle of Fifths panel (programmatic ASCII ring, majors outside, relative minors inside);
    interval symbols unified with the intervals lesson (no P-prefixes); tree section headers
    (Interactive / Reference); panels rebuild on theme change
  - **Metronome** — user: "kinda hacky"; revisit separately later
- Inline content blocks — `exercise` and `lick` slug references in lesson Markdown; two-pass loading (loaders independent, resolved in `on_mount`); evaluate alongside Study screen redesign before implementing

### Content gaps (Tier 3b) — staged


**Stage 3** (ear training — constrained by no-audio):
- Track 15 (5 lessons): ear training guide; explicit about app limitation; looper-as-ear-training format
- Optional: add `listening_exercise:` Markdown section convention to lick files (no engine change)

**Stage 4** (world sounds):
- Track 16 — Sounds and Scales Around the World (6 lessons): harmonic minor, Phrygian dominant, Hungarian minor, whole tone, diminished, Japanese pentatonic
- ~~Data prerequisites~~ ✓ done 2026-07-12 — all 6 scale YAML files shipped with M8; lessons unblocked
- 1 lick per lesson (looper-ready, captures characteristic phrase shape of each tradition)




### Low priority

- **GitHub Actions release workflow** — build + publish to PyPI on tag push (`uv build` / `uv publish` with a `PYPI_API_TOKEN` repo secret or trusted publishing); replaces the manual `.env` + `uv publish` flow. Not urgent — manual flow works.
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

- Full content/engine audit (docs/reviews/2026-07-11_reviewer_assessment.md): ~30 fixes — wrong chord diagrams, reversed lick, scale-box gaps, partial-barre orientation bug, 2-char fretboard labels ✓
- PyPI release: guitar-tui 0.1.0 live (`uv tool install guitar-tui`), package metadata, README install docs, in-app AI disclosure, .env token flow, tag v0.1.0 pushed ✓
- Content-verification pytest: 563 mathematical checks over all diagrams, licks, and data; mutation-verified ✓
- Content gaps Stage 1: Track 14 rhythm core (4 lessons) + Track 13 phrasing core (3 lessons); phrasing/rhythm/expressive-techniques tracks registered in index.yaml ✓
- Exercise module-field fix: barre_strength → barre-chords, pentatonic_licks_1/pentatonic_sequences → pentatonic-scale (were orphaned, never shown on their tracks) ✓
- Content gaps Stage 2: Tracks 13–14 complete — 5 lessons (motif_development, rhythmic_placement, building_a_solo, ghost_strokes, rhythm_in_leads), 7 exercises (4 rhythm + 3 phrasing modules), 5 licks (Phrasing + Rhythm categories); 96 lessons, 30 licks, 875 tests ✓
- Exercises tab redesign: lesson tab now shows track-specific drills only (licks model); universal warmups relabeled "Warm-ups" in Practice tree; Practice module order/labels updated for all 9 exercise modules; overview text explains the split ✓
- chord_melody_intro exercise: Ode to Joy chord-melody arrangement (module seventh-chords, advanced) — last open Chord Exercises item ✓
- Tools/Key View correctness: enharmonic chord lookup (C#↔Db, Abm↔G#m), 12 moveable diminished voicings (data), chord-tone fallback for missing voicings — "(no voicing)" dead-ends 23% → 0% ✓

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
- Track progress indicator `[pos / total]` in lesson border title (left-anchored) ✓
- uv.lock committed; removed from .gitignore ✓
- Community standards: CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, bug + feature issue templates ✓
- Curriculum planned: Tracks 13–16 scoped (Phrasing, Rhythm Depth, Ear Training, Sounds and Scales Around the World) ✓
- Audio feature scoped and stored as single future milestone (metronome + tuning + intervals + playback, one library) ✓
