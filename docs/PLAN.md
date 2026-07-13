# Plan

## Active
<!-- Current sprint items. Keep this short — 5-10 items max.
     If it grows beyond that, move lower-priority items to Backlog. -->

### Agreed order of work (2026-07-12, post-M8)

1. **Review all work since v0.1.0** (user request) — full pass over M8, Track 16, worksheet v1
2. **Worksheet v2 evaluation** — after v1 has been used on real songs (below)
3. **Track 15 (ear training) last** — value capped until/unless the audio milestone happens

### Song Analysis Worksheet (feature, agreed 2026-07-12 — ADR D12)

The practice artifact of Track 11's Four Questions: a per-song, per-*section* analysis
template (sections solve intros/bridges — repeating blocks, not multiple templates).
One future schema, three consumers: user worksheet, Songbook entries, Song Analysis tool.
v1 shipped 2026-07-12 (see Done); remaining phases:

- **v2 — interactive worksheet:** form inputs per section in Tools; **key-candidate
  inference** — intersect `chord_memberships()` of the chords entered so far and rank keys
  by diatonic coverage ("Em G C D → G major or E minor"); selected key hydrates the
  existing Song Analysis panel. Requires the section schema in `schemas/` first, and the
  app's first Input-widget UX. Evaluate after v1 has been used on real songs.
- **v3 — persisted analysis library:** save/load analyses in the user data dir
  (`user_config_dir` precedent from settings.py); render saved analyses through the same
  viewer as Phase 4 Songbook entries. Sequence alongside Songbook.

### Infrastructure

- **Demo GIF doesn't render on PyPI** — README embeds `demo.gif` (rendered from `demo.tape`)
  by relative path; GitHub resolves it, PyPI's long description does not. Fix: point the image
  at the absolute `https://raw.githubusercontent.com/konoerik/guitar-tui/main/demo.gif` URL
  (verify PyPI renders it), or strip the image from the PyPI description.
- **Evaluate line wraps in lesson prose** — this is a TUI: the Markdown/Static widgets wrap text
  to widget width, and the size warning already guarantees ≥110 cols for tables/diagrams. There is
  therefore no reason for content to fight "runaway sentences" — prose can be written naturally and
  wrap. Audit: (a) whether any rendered surface fails to wrap (diagram captions inside rendered
  Text, Static summaries, welcome/info cards); (b) whether source-file hard-wrapping conventions
  (some files ~75-col wrapped, some single-line paragraphs) have any rendering effect, and settle
  on one authoring convention for content files.
- **Metronome** — user: "kinda hacky"; revisit separately later (rest of the 2026-07-11
  "Tools section improvements" list shipped with M8 — see Done)
- Inline content blocks — `exercise` and `lick` slug references in lesson Markdown; two-pass loading (loaders independent, resolved in `on_mount`); evaluate alongside Study screen redesign before implementing

### Content gaps (Tier 3b) — staged


**Stage 3** (ear training — constrained by no-audio):
- Track 15 (5 lessons): ear training guide; explicit about app limitation; looper-as-ear-training format
- Optional: add `listening_exercise:` Markdown section convention to lick files (no engine change)

**Stage 4** (world sounds): ✓ complete 2026-07-12 — see Done

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
- v0.2.0 released to PyPI (tag v0.2.0): Tracks 13–14 content, Key View fixes, exercises redesign ✓
- Key View enhancements: `v` voicing cycling (24 multi-voicing chords), key-context line, ◆ characteristic-note highlighting (modes, blues, harmonic-minor family) ✓
- M8 Theory Web data layer (ADR D11): theory/web.py (chord_memberships, realize_progression, transposition helpers), data/progressions.yaml (16 validated progressions + schemas/progression_format.md), theory_refs frontmatter + reverse index (~49 lessons tagged) ✓
- M8 scale view (Key View extension): progressions realized in key + lesson cross-refs panel; 6 world scales selectable; harmonic minor + Phrygian dominant degree tables incl. augmented chords ✓
- Track 16 scale YAML: 6 files generated from interval formulas, verified by content suite ✓
- M8 Chord View: all voicings side by side, spelled tones, key-function OptionList → Key View jump; Song Analysis workflow (key+quality → full workup + Explore links); history-stack navigation (`g` / backspace) ✓
- M8 reference overhaul: shared theme-aware palette (ui/styles.py), quality-colored diatonic table, notes panel with inlay markers, grouped chord formulas, lesson-unified interval symbols, Circle of Fifths ASCII ring, Interactive/Reference tree sections ✓
- Key View neck-overflow bug fixed: #chord-row ≤55% + #key-content min-height 12; regression test to MIN_COLS×MIN_ROWS ✓
- v0.3.0 released to PyPI (tag v0.3.0) via new Makefile release targets (version-check/build/publish/release) ✓
- Track 16 content: 6 world-scale lessons (16-world-scales) + 6 looper licks (World Scales branch), all pitch-verified; CURRICULUM at 103/108 lessons ✓
- Song analysis worksheet v1 (ADR D12): Worksheet leaf in [4] Practice (template-first, spaced) + lesson closing Track 11; v2/v3 phased in Active ✓

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
