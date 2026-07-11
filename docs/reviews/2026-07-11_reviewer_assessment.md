# Reviewer Assessment — 2026-07-11

**Scope:** Full audit on two fronts: (1) Developer — engine/renderer implementation with focus on
visual output (alignment, notation); (2) Instructor — music-theory correctness of all data files,
lesson diagrams, licks, and exercises.

**Method:** All 209 diagram blocks in content were rendered through the real dispatcher and checked
programmatically for alignment invariants. Every chord voicing, scale-position note, and lick tab
was re-derived mathematically from standard tuning and compared against the chord name / stated
degree / declared key+scale. Theory-heavy lesson prose was read in full. Test suite baseline:
276 passed.

**Overall:** The engine is in good shape — no rendering misalignment exists in any shipped diagram.
The problems are concentrated in *content*: a number of diagrams and prose passages are musically
wrong, several written as if the tab `notes` array ran high-to-low, and the "shape relationship"
paragraphs in Track 09 repeatedly mis-attribute notes to strings.

---

## Part 1 — Developer (implementation / visual)

### Verified sound

- All 209 rendered diagrams have internally consistent row widths; chord grids are 25 chars and
  header/marker/dot columns align; scale/fretboard 5-char columns align including 2-digit fret
  headers; tab measures, durations, two-row labels, bends (`8b10~`), and connectors align.
- `theory/keys.py` is fully correct: key signatures, modal diatonic-chord tables, capo chart.
- `FullNeckWidget` column math (4-char columns, header centering, bracket placement) is correct.
- `tunings.yaml` all correct. Chord data YAML all correct (C7 omits the 5th — standard voicing,
  fine). Pentatonic/blues scale YAML fully correct.

### D1 — Latent: tab renderer pads mixed-width beats with spaces (`tab_renderer.py:158`)

`note_str.ljust(note_str_width)` pads with **spaces**. Any beat whose notes render at different
widths (a chord beat mixing frets `3` and `12`, or a bend suffix on one note of a chord) would put
literal spaces inside the staff line: `─3  ─`. No current content triggers it (verified across all
diagrams), but it is one lick away. Fix: `note_str.ljust(note_str_width, "─")`. Same issue in the
rest column at line 147 (`"r".ljust(note_str_width)`), harmless today since rest width is fixed.

### D2 — Fretboard renderer silently drops out-of-range highlights (`fretboard_renderer.py`)

A `FretNote` outside `fret_range` simply never appears — no warning. This is already destroying
content: `intervals.md` block#0 lists `{string: 3, fret: 9}` with `fret_range: [0, 7]`, so one of
the "E notes above" the prose refers to is invisible. Consider a validation warning at load time
(range check belongs in loader/schema, not the music-agnostic renderer).

### D3 — `show_notes` is a no-op (`fretboard_renderer.py:40`)

`_col(note, show_notes)` never reads the parameter; note-name display only happens via explicit
`label`. Several lessons set `show_notes: true` expecting it to do something. Either implement
(derive note names from tuning — requires passing tuning knowledge, a design decision) or drop the
field from the spec.

### D4 — Stale docstring (`chord_renderer.py:7-13`)

Docstring shows 5-cell borders and 19-char geometry; code renders 6 cells / 25 chars. Cosmetic.

### D5 — Known, already tracked

Trailing dash before technique connector (`─5─h8─` vs `─5b7─`) — ADR-D8, in PLAN Low priority.

---

## Part 2 — Instructor (music correctness)

### Wrong diagrams — render fine, sound wrong (fix frets)

| # | File | Problem | Fix |
|---|------|---------|-----|
| I1 | `lessons/01-orientation/reading_chord_diagrams.md` "A Minor (5th position)" | `[1,1,3,3,2,1]` @ base 5 sounds **D–F–A (Dm/A)**, not Am | E-shape Am: `frets [1,3,3,1,1,1]`, `fingers [1,3,4,1,1,1]` |
| I2 | `lessons/05-barre-chords/barre_progressions.md` "E Major — V (E-shape, 7th fret)" | E-shape @ 7 = **B major**; V of A is E | A-shape @ 7 (`[null,1,3,3,3,1]`), retitle; also fix intro sentence "All three chords played as E-shape barres" (the IV is A-shape) |
| I3 | `lessons/05-barre-chords/caged_overview.md` "C Major — G-shape (5th fret)" | `[3,1,x,x,1,3]` @ 5 = B, D, E | `[4,3,null,null,1,4]` @ 5 → C E … E C (frets 8-7-x-x-5-8) |
| I4 | same file, "C Major — D-shape (10th fret)" | `[null,null,1,3,3,3]` @ 10 = **Cmaj7** (B on B-string) | B-string relative 4: `[null,null,1,3,4,3]` |

### Licks/exercises with wrong notes

| # | File | Problem |
|---|------|---------|
| I5 | `licks/natural_minor_pos5.md` | **Entire tab is string-reversed** (written as if index 0 = high e). As shipped it plays wrong strings and out-of-scale notes (C#, A#). Reversing every `notes` array reproduces the prose exactly. |
| I6 | `licks/lydian_raised_fourth.md` | Beats 3–5 are on the B string (D#, F, F#) but the melody G A **B C# D** E needs G-string frets 4, 6, 7. Beat 6 (G-string fret 9 = E) is the right pitch but prose says "E on the B string". |
| I7 | `licks/phrygian_half_step.md` | Beat 5 (D-string fret 4) = F#, not in E Phrygian — prose says B (A-string fret 2 or D-string fret 9). Beat 6 (A-string fret 5) = D but prose says the phrase ends on "a low E". |
| I8 | `licks/pent_blues_turnaround.md` | Beat 3 (B-string fret 7) = F# — should be fret 8 (G) for the descending A-minor-pentatonic line. Prose also promises a pull-off to open E that the tab doesn't contain. |
| I9 | `exercises/natural_minor_positions.md` | B-string fret 7 = F# (A natural minor has F). The line also jumps down an octave mid-"ascent" (e-fret-8 C6 → G-fret-7 D5), contradicting the handoff narrative. Needs a rewrite. |
| I10 | `licks/slide_connector.md` | Tab beats 1–2 sit on the G string (C, D); prose says "D string fret 5 = G (b7); fret 7 = A (root)". One of the two is wrong — pick and align. |

### Scale-box data errors (systematic)

- **I11 — E-shape box is missing its high-e 7th-degree note in six data files.** String 1 must
  mirror string 6 (frets 7-8-10): `major.yaml` pos 1, `dorian.yaml` pos 1, `lydian.yaml` pos 4,
  `mixolydian.yaml` pos 2, `natural_minor.yaml` pos 2, `phrygian.yaml` pos 5 all have string 1 =
  {8, 10} while string 6 = {7, 8, 10}. The same omission is copied into lesson diagrams:
  `major_scale_construction.md`, `major_scale_p1.md`, `dorian_mode.md`, `natural_minor_p2.md`.
- **I12 — Lesson boxes contradict the data layer.** `relative_minor.md` (both diagrams),
  `natural_minor_intro.md`, and `natural_minor_p1.md` omit A-string fret 8 (b6 F / 4th) that
  `natural_minor.yaml` pos 1 includes.
- **I13 — Other in-range gaps** (D-shape fret 13 on both E strings; A-shape fret 1; C-shape
  B-string fret 12; nat-minor pos 4 D-string 15) are consistent across all seven-note scale files
  and may be deliberate pattern-edge choices — but they sit inside the declared `fret_range`.
  Instructor should either add the notes or tighten the ranges. Note the Dorian lesson's claim that
  the 6th "appears once" is already false in its own diagram (degree 6 at s6 f7 *and* s4 f9).

### Prose / theory errors

| # | File | Problem |
|---|------|---------|
| I14 | `lessons/08-major-scale/major_scale_chords.md` | I-IV-V-vi table, "In D" column: **IV=A, V=E** — correct is IV=G, V=A |
| I15 | `lessons/04-theory-basics/key_signatures.md` | "G and D … share the A minor chord" — Am contains C natural, not in D major. They share Bm and Em. |
| I16 | `lessons/04-theory-basics/intervals.md` | Fretboard block: `{string: 6, fret: 7}` labeled "E" is **B**; `{string: 3, fret: 9}` is outside `fret_range [0,7]` and never renders. |
| I17 | `lessons/01-orientation/tuning_your_guitar.md` | The 12th-fret-harmonic "sanity check" is physically wrong: the harmonic always matches the open string (node at the midpoint). Intonation is checked by comparing the harmonic against the **fretted** 12th-fret note. |
| I18 | `lessons/01-orientation/reading_scale_diagrams.md` | "three ■ markers appear at the 5th fret" — two are at fret 5, the third is at fret 7 (D string). |
| I19 | Track 09 "shape relationship" paragraphs | Multiple wrong string/note attributions: `dominant_7th.md` — "E7 removes the G# / lets the G string ring open" (E7 keeps G#; it opens the **D** string, D = b7). `major_7th.md` — "E7 has an open G string (G = b7); Emaj7 frets the G string at 1 (G# = major 7th)" (the E7→Emaj7 change is on the **D** string, D→D#; G# is E's major **3rd**); "Dmaj7 … high e stays at fret 2 (E = 9th)" (high-e fret 2 = **F#**, the 3rd). `minor_7th.md` — "Dm7 … the high e at fret 1 is also C" (it is **F**, the b3); plus a published self-correction artifact: "(C# — wait, no: A minor has C natural…)". |
| I20 | `lessons/09-seventh-chords/sus_and_add.md` | "Dsus2 … opens the B string" (it opens the **high e**; B stays fret 3); "Dsus4 frets B string at 3 (G = the 4th)" (B-string 3 = **D**; the G is high-e 3); "Esus4 … B and G strings are lifted … to fret 2" (B stays open); **a Gsus4 diagram sits in the Add-chords section where Gadd9 is discussed**, and "Gadd9 … the A note on the B string" matches no shown voicing. |
| I21 | `lessons/03-first-progressions/strumming_basics.md` folk strum | Count row is malformed: "1 and 2 and · **and** 3 and 4 and" (extra "and", 9 slots); as aligned, no strum falls on beat 4. Prose says the ghost is on "the and of 2", but D-DU-UDU's gap is **beat 3** — their own chart shows a U on &2. |
| I22 | `lessons/11-song-analysis/analysing_common_progressions.md` | Am–F–C–G labeled "the 'Andalusian'" — the Andalusian cadence is i–bVII–bVI–V (Am–G–F–E), listed correctly elsewhere in the same lesson. |
| I23 | `lessons/11-song-analysis/scale_selection.md` | Purple Haze: "the opening F#-G movement implies Phrygian" — F# is not in E Phrygian (which has F natural); contradicts the Phrygian lesson. |
| I24 | `lessons/06-pentatonic-scale/pentatonic_major_vs_minor.md` | "C (the **major 3rd** of A minor is the relative major root)" — C is the *minor* 3rd of A. |
| I25 | `licks/major_scale_upper_phrase.md` | Prose contour ("ascends in two waves … each wave ends a step higher") contradicts the tab — each wave starts lower than the previous ended. |

### Minor nits

- `phrygian_mode.md`: "metallica" lowercase.
- `minor_scale_chords.md`: "II°" should be "ii°" in the D-minor transposition line; lesson uses
  III/VI/VII while `theory/keys.py` renders bIII/bVI/bVII in the Analyze strip — pick one notation.
- `dorian_mode.md`: mixes "i – VII – IV" and "i – bVII – IV – i" in adjacent lines.
- `musical_alphabet.md`: "a gap of one semitone called an accidental" — the *note in the gap* is
  the accidental; adjacent naturals (other than E-F/B-C) are two semitones apart.
- `roman_numerals.md`: "uppercase indicate major chords **borrowed** from the parallel or relative
  major" — III/VI/VII are diatonic to natural minor, not borrowed.
- `scale_selection.md`: "B natural minor works either way" over Hotel California — it clashes with
  the F# major chord (A# needed); worth a hedge.

---

## Suggested priority

1. **I1, I5** — orientation lesson chord and a fully-reversed lick: first-contact content, wrong.
2. **I2–I4, I14** — wrong chords in CAGED/barre lessons and the D-major table: core teaching.
3. **I11–I12** — scale box fixes (data files first, then re-sync lesson copies).
4. **I19–I20** — Track 09 shape paragraphs: rewrite against the actual diagrams.
5. **I6–I10, I21–I25** — remaining licks/prose.
6. **D1–D4** — engine hardening; none user-visible today.

---

## Outcome — 2026-07-11 (same session)

All findings fixed in priority order. Every issue above (D1–D5 except the
already-tracked D5, I1–I25, and the minor nits) was resolved; I13 was resolved
by **adding** the missing in-range notes rather than tightening ranges, making
every box complete against its declared `fret_range`.

Notable decisions made while fixing:

- **I2**: the V diagram became an A-shape barre at the 7th fret (parallels the
  IV); the section intro was rewritten to match.
- **I3**: the G-shape C diagram now shows the full shape
  (`[4,3,1,1,1,4]` @ 5 with a partial barre) — the 4-note fragment had no 5th.
- **D3**: `show_notes` was removed from `FretboardSpec`, the renderer, content,
  and the schema doc (it was never implemented; labels are the mechanism).
- **D2**: out-of-range notes are now hard `ValidationError`s on both
  `FretboardSpec` and `ScaleSpec` (when `fret_range` is explicit), per the
  "startup failure over silent corruption" rule. Schema doc updated.

**New finding fixed during verification — D6, partial barre orientation.**
The chord renderer interpreted `barre.from`/`to` as 1 = low E (and the schema
doc agreed), but all content and data were authored with 1 = high e (the
`ScaleNote`/`FretNote` convention). Every partial barre in the app — Bm, all
A-shape barre chords in `barre_chords.yaml` (Reference screen), Dm7's
mini-barre — rendered shifted onto the wrong strings, including barres drawn
across muted strings. Fixed the renderer mapping (`6 - to_string .. 6 -
from_string`), corrected the schema doc, documented the convention on
`BarreDef`, and added orientation regression tests.

Verification: 285 tests pass (was 276; 9 added). A full mathematical re-audit
of all 209 diagram blocks, every chord voicing, scale position note, and lick
tab reports zero issues (the C7 open voicing's omitted 5th is standard and
intentionally kept). All loaders load warning-free: 53 chords, 9 scales,
84 lessons.
