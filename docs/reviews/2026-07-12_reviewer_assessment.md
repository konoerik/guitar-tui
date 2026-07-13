# Reviewer Assessment — 2026-07-12

**Scope:** Everything shipped since v0.1.0 (the 2026-07-11 audit covered content through
84 lessons; all its findings were fixed same-session). Delta reviewed here: Tracks 13–14
(12 lessons, 8 exercises), Track 16 (6 lessons, 6 licks, 6 scale data files), 5 phrasing/
rhythm licks, M8 Theory Web (theory/web.py, progressions.yaml, keys.py degree tables,
Circle of Fifths, Key/Chord/Song Analysis views), and the song-analysis worksheet v1.

**Method:** Test baseline 1043 passed. Confirmed all pre-existing lessons modified since
v0.1.0 changed only `theory_refs:` frontmatter (no prose drift). Every new tab block's
pitches were recomputed from standard tuning and compared against the prose narrative
note-by-note; every new scale diagram was re-derived degree-by-degree and checked for
in-range completeness; all rhythm charts were checked for slot counts and stroke parity
(D/U vs grid position); progressions and the new degree tables (Harmonic Minor, Phrygian
Dominant) were re-derived triad-by-triad; the Circle of Fifths placement was simulated
and checked for collisions and key/relative-minor correctness; UI names referenced by
content (◆ claims, "Notes on Strings", Practice → Worksheet, Chord View function format)
were verified against the code.

**Context:** The `test_content_verification.py` suite added since the last audit is doing
real work — chord voicings, scale positions/formulas, diagram degrees, and lick
scale-membership are now machine-checked, and none of last audit's error classes
reappeared. The findings below live precisely in the suite's two blind spots:
(a) tabs with no `key`/`scale` frontmatter (all Track 13/14 lesson tabs and all 8 new
exercises — 24 blocks with entirely unchecked notes), and (b) prose claims about what
the notes do.

**Overall:** Strong release. The engine and theory code are defect-free as far as this
audit reached; the two new degree-table families are exactly right; Tracks 13/14/16 are
pedagogically the best-written content in the app. Three content findings (one wrong-note
lick, two wrong prose claims), then notation nits.

---

## Part 1 — Content findings

### I1 — `licks/floating_whole_tone.md`: tab contradicts the lick's entire premise

The tab plays **C D E F# Bb C** — it skips G# (so the "even whole steps" climb contains
a major-3rd leap) and **ends on the root**, resolved. But the summary ("ends suspended on
the b7"), the intro ("ending deliberately in mid-air on the b7"), the technique notes
("resist adding vibrato until the *final* Bb, then let it hang"), and the parent lesson
(`whole_tone_scale.md`: "rises through the shape and hangs on the b7 — unresolved by
design") all describe a line ending on Bb. The intended lick is clearly
**C D E F# G# Bb**: last two beats should be G-string frets **1 and 3** (G#, Bb), not
3 and 5. One sentence in the bold analysis paragraph ("The last two notes are Bb (b7)
and C…") was written to match the wrong tab and needs rewriting to match the fix.
The scale-membership test passed because C is in-scale — this is exactly the
prose-vs-tab class the suite cannot see.

### I2 — `lessons/13-phrasing/question_and_answer.md`: example licks fail the lesson's own criterion

Practice item 3: "The *Blues Turnaround* is a textbook answer phrase; the *B.B. King
Box* phrase asks." But the B.B. King Box lick **ends on A, the root** — by the lesson's
own ending-note table (root = "full stop … answer a question") it is an answer, not a
question. And the Blues Turnaround ends on **E, the 5th** — the table's "comma …
ask a question" row. The two labels are wrong by the lesson's own rule; either swap
them or pick examples that fit.

### I3 — `lessons/14-rhythm/sixteenth_strumming.md`: strum count

"Nine strums out of sixteen passes" — the half-bar pattern D··U·UD· has 4 strums,
played twice = **eight**.

### Notation / slot-count nits

- **N1** — `exercises/two_bar_rule.md`: bar 1 sums to **7** eighth-slots (1+1+1+4)
  while bars 2–4 have 8; bar 1 renders visibly narrower than its siblings.
- **N2** — `licks/question_answer_pair.md`: both lines sum to 7 slots under the
  eighth-slot convention every sibling lick uses (displaced_cell, syncopated_332,
  space_phrase are all exact); and the prose "count it ('3 &, 4 &')" describes a
  two-beat rest but the rest's `duration: 2` is one beat in that convention.
- **N3** — `lessons/13-phrasing/question_and_answer.md` tab: same pattern — question
  line 7 slots, answer line 6. (Free `beats` lines, so nothing breaks visually.)
- **N4** — `exercises/subdivision_pyramid.md` Rules: "D on the numbers and '&'s,
  U between" is the sixteenth-grid rule; on the eighth-note rung the "&"s take
  upstrokes — as the diagram's own labels correctly show.
- **N5** — `lessons/13-phrasing/phrase_shape.md`: "the same position, the same
  rhythm, but no contour" — the arc has held notes (12 slots), the anti-phrase is
  straight eighths (8); same notes, not same rhythm.
- **N6** — `lessons/16-world-scales/hungarian_minor.md`: "Nearly half the scale's
  steps are leaps" — 2 of 7.
- **N7** — `lessons/16-world-scales/phrygian_dominant.md`: "the open-string F on
  string 4 fret 3" — that F is fretted; and "the descending run E–F–G–Am" lists the
  Andalusian chords ascending while calling it descending.
- **N8** — Misirlou (cited in `harmonic_minor_sound.md` and `phrygian_dominant.md`)
  is technically double harmonic — the full run includes D#. Common guitar-pedagogy
  simplification; worth a hedge ("its opening phrase"), not a rewrite.

---

## Part 2 — Verified sound (highlights)

- **Track 16 scale diagrams**: all six lesson boxes re-derived note-by-note — degrees,
  roots, and in-range completeness all correct, including the harmonic → Hungarian
  "only change is D → D#" cross-lesson claim and hirajoshi's "twelve notes" count.
- **Licks**: gypsy_cadence_run, hungarian_aug_seconds (both augmented 2nds land on the
  stated strings/frets), koto_phrase (exact 9-note arch), spanish_descent (all seven
  tones, chord-tone claims over F and E both right), diminished_tension_line (cells
  climb in minor 3rds, non-chord-tone analysis correct), and all five phrasing/rhythm
  licks match their prose, including the mirrored Q/A pair and exact 3-3-2 slot math.
- **Track 14 rhythm charts**: subdivision grids are internally consistent (16
  sixteenth-slots in all three densities); the pop-groove caption matches its tab
  slot-for-slot with correct D/U parity; ghost-stroke rings land on the 3-3-2 grid.
- **chord_melody_intro**: the Ode to Joy arrangement is exact — melody is always the
  top voice (bar 3 correctly silences the high e), G-with-D-on-top half cadence,
  Cmaj7 re-harmonization voicing (`x32000`) correct.
- **Worksheet**: the E Dorian micro-example (Em–G–D–A = i–bIII–bVII–IV, ◆ = C#) is
  exactly right; the Practice-tab template matches the lesson field-for-field.
- **M8 theory code**: both new degree tables verified triad-by-triad (harmonic minor's
  bIII+ and vii°, Phrygian dominant's iii°/v°/bVI+ — all correct); characteristic-note
  table matches every ◆ claim in lessons; `chord_memberships`/`realize_progression`
  correct by construction over those tables; Circle of Fifths simulated — no label
  collisions, all 12 majors and relative minors correct.
- **progressions.yaml**: all 16 entries musically correct, including the Andalusian
  entry's careful "continues down to a major V" hedge.

### D1 — stale comment (only Developer-side finding)

`progressions.yaml` header says quality "must be one of … (Major, Minor, Blues, Dorian,
Phrygian, Lydian, Mixolydian)" but the loader and `DEGREE_QUALITIES` accept nine —
the file itself uses Harmonic Minor and Phrygian Dominant. Update the comment.

---

## Recommendation

The 24 tab blocks with no `key`/`scale` frontmatter are the suite's remaining blind
spot, and I1 shows the failure mode is real. Nearly all Track 13 lesson tabs and half
the exercises are plain A minor pentatonic / E5 vamps — adding frontmatter (or a
per-block key) would bring them under `test_lick_notes_in_declared_scale` for free.
A slot-count invariant for `measures` blocks (all bars in a line sum equal) would have
caught N1/N3 mechanically.

## Suggested priority

1. **I1** — wrong notes shipped against an explicit teaching claim (fix tab + one sentence + no lesson change needed).
2. **I2, I3** — wrong prose in core Track 13/14 lessons.
3. **N1–N5** — slot-count and rule-wording cleanups.
4. **N6–N8, D1** — hedges and comment.

---

## Outcome — 2026-07-12 (same session)

All findings fixed in priority order.

- **I1**: `floating_whole_tone` last two beats moved to G-string frets 1 and 3 —
  the line is now C D E F# G# Bb, six even whole steps ending suspended on the
  b7; the one prose sentence written to the wrong tab was rewritten.
- **I2**: the lick labels were swapped to match reality (B.B. King Box answers
  on the root; Blues Turnaround asks on the 5th over the V).
- **I3**: "Nine strums" → "Eight strums".
- **N1/N3**: durations corrected so every bar sums to 8 eighth-slots.
- **N2**: `question_answer_pair` restructured — the question bar now sums to 8
  (G held its stated two beats) and the silence got its own full bar, matching
  the looper setup ("rest through G"); count guidance updated to the full bar.
- **N4–N8, D1**: rule wording, prose claims, Misirlou hedges, and the
  progressions.yaml family-list comment all corrected as specified.

**Recommendation implemented (invariant only).** `test_tab_measures_equal_slots`
now enforces equal slot-sums across all bars of a tab line (+27 parametrized
tests). It immediately caught one additional defect in *pre-existing* content:
`exercises/position_shifts.md` bar 2 summed to 5 quarter-slots against bar 1's
4, contradicting the exercise's own "four beats per measure" rule — the stray
`duration: 2` on the final note was removed. The frontmatter half of the
recommendation (bringing the 24 key/scale-less tab blocks under scale-membership
checking) touches the lesson frontmatter schema — a Developer/Instructor contract
change — and is left as an open item.

Verification: 1070 tests pass (was 1043). Both restructured tabs re-rendered
and visually confirmed; the fixed whole-tone line re-verified note-by-note.
