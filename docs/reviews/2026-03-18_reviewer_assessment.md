# Reviewer Assessment — 2026-03-18

**App state**: Post-REDESIGN completion — Exercises and Licks tabs in lesson view, full lick library coverage across all scale categories, 14 exercises, 23 licks, content gaps closed.

---

## What Has Changed Since Last Review

The previous review (2026-03-11) identified five content gaps as priority concerns. Three were fully addressed:

| Previous gap | Status |
|---|---|
| Major scale licks (Track 08 had none) | ✓ Fixed — two licks added |
| Natural minor upper positions (only descent/pos1 covered) | ✓ Fixed — pos2, pos3, pos4, pos5 added |
| Pentatonic positions 3, 4, 5 (no licks) | ✓ Fixed — three licks added |
| Blues chord strip showing wrong harmony | ✗ Still open |
| Bm/F labelled as "Open Chords" | ✗ Still open |

The Lydian key mismatch (lesson in F, lick in G) flagged in the previous review has also not been addressed.

The lick and exercise coverage is now genuinely impressive for a free terminal tool. An intermediate player who has worked through Track 06 (Pentatonic) or Track 07 (Natural Minor) will find a lick for every position, which was the single most important gap to fill.

---

## Music Theory Accuracy — New Content

### Critical error: natural_minor_pos4 lick — wrong note

The "Classical Descent" lick for Natural Minor Position 4 contains a fret/note mismatch that produces the wrong pitch. The final note is listed in the tab as **B string, fret 14**, with the label "A (root)." In standard tuning, B string fret 14 is **C#**, not A. The root A in this position lives at G string fret 14.

The prose description compounds the error: "The phrase resolves to A (root, B string fret 14)" — this is the wrong string. A player following the tab will land on C# and wonder why the phrase sounds unresolved. The correct final note is **G string fret 14 = A**.

This is the most significant accuracy issue in the current release. It affects the last note of the phrase — the resolution — which is the most audibly obvious note to get wrong.

### Pentatonic_licks_1: Lick 5 is identical to Lick 1

The exercise is described as five distinct phrases, but Lick 5 ("Resolution") and Lick 1 ("Descend to Root") are note-for-note identical: G string fret 7 (D) → G string fret 5 (C) → B string fret 5 (E) → high e fret 5 (A, duration 2). The description claims Lick 5 has "a longer hold" as its distinguishing feature, but both licks already show duration 2 on the final A. There is no practical difference between them.

A player who learns all five will not realise they have only learned four. The exercise should either replace Lick 5 with a genuinely different phrase (a resolution arriving from below, or from the low-string area, for example) or remove it and acknowledge four licks.

### Phrygian Flamenco Run — title/content mismatch

The CURRICULUM originally described this as a "Flamenco Rasgueado Pattern." Rasgueado is a specific right-hand technique — a fan stroke using individual fingers in sequence — and is fundamental to flamenco guitar. The current lick is a single-note descending run (picado style), which is a legitimate flamenco technique but is not a rasgueado. The title has been changed to "Phrygian Flamenco Run" which softens the mismatch, but a flamenco guitarist reading this would note the distinction. Not an error per se, but the original intent was not delivered.

### Remaining content verified accurate

All other new lick tab diagrams were verified note-by-note against standard tuning. The following are correct:

- `natural_minor_pos2`, `natural_minor_pos3`, `natural_minor_pos5` — all fret numbers match note labels
- `phrygian_flamenco`, `mixolydian_chord_riff` — all fret numbers match note labels
- `major_scale_lower_run`, `major_scale_upper_phrase` — correct
- `pent_position3_run`, `pent_position4_run`, `pent_position5_run` — correct
- `string_skipping`, `position_shifts`, `major_scale_sequences` — correct

The description of diatonic thirds in `major_scale_sequences` is accurate: the sequence A → C# → B → D → C# → E → D → F# correctly traces diatonic thirds ascending through A major.

---

## Pedagogical Observations — New Exercises

### String Skipping

The exercise is correct and well-explained. One limitation: it demonstrates the skipping concept only within the fret-5 window of A minor pentatonic position 1. A player who completes it has learned the technique within one position but has no guidance on applying it elsewhere. The "Progression" section at the end addresses this verbally, which is the right approach.

### Position Shifts

The exercise shows the shift between position 1 and position 2 using only the top two strings (B and high e). This is mechanically accurate but pedagogically incomplete — a player shifting positions in practice will need the whole hand to move, not just the fingers on two strings. The exercise correctly identifies the key concept (same fret, different finger) but a player might complete it without developing the full-hand shift that improvisation requires. A second example on the lower strings would strengthen this considerably.

### Major Scale Sequences — Diatonic Thirds

This is the strongest of the new exercises. The concept is clearly explained, the rationale ("scale runs that jump over a note start to sound intentional") is genuinely useful framing, and the tab is accurate. The instruction to say note names aloud while playing is good pedagogy. The "Extending the Pattern" section correctly notes that natural minor will produce different major/minor third distributions, which shows theoretical awareness.

---

## Previously Open Issues — Still Unresolved

### Blues chord strip

As noted in the March 2026 review: selecting Blues in the Key View shows natural minor diatonic chords (Am, Bdim, C, Dm, Em, F, G in the key of A). Blues harmony uses dominant 7th chords — I7, IV7, V7. An intermediate player opening the Blues view to understand what to play over a 12-bar blues gets the wrong harmonic picture. This remains the most misleading feature in the app.

### Bm and F in Track 02 — Open Chords

Both are full barre chords. Bm requires a full index barre at fret 2 and is one of the hardest chords for beginners to produce cleanly. Labelling them as "Open Chords" creates a false category that will confuse beginners who struggle with them and wonder if they are doing something wrong. At minimum these two lessons need a note that they are "first barre chord" content, not open chord shapes.

### Lydian lick in G, Lydian lesson in F

The Lydian mode lesson teaches the position at frets 12–15 in F Lydian. The `lydian_raised_fourth` lick is in G Lydian at a different fret region. A player who works through the Lydian lesson, then goes to Practice → Licks → Lydian, will find a lick in a completely different key and fret area from what they just learned. The shapes are transposable, but the mismatch will cause disorientation for the target audience of intermediate players who are still connecting shapes to sounds.

---

## Summary

| Area | Status |
|---|---|
| Lick coverage — pentatonic, natural minor, major scale | ✓ Now complete across all positions |
| Lick coverage — modes | ✓ One lick per mode, adequate |
| `natural_minor_pos4` final note | ✗ **Error: B string fret 14 = C#, not A** |
| `pentatonic_licks_1` Lick 5 | ✗ Identical to Lick 1 — should be a different phrase |
| Phrygian flamenco content | ⚠ Not a rasgueado — title softened but concept undelivered |
| Blues chord strip | ✗ Still shows wrong harmony |
| Bm/F in Open Chords track | ✗ Still miscategorised |
| Lydian lick key mismatch | ✗ Still misaligned with lesson key |
| New exercises | ✓ Accurate; position_shifts could use lower-string example |
| Expressive techniques | ✗ Still absent (vibrato, bending, hammer-ons, slides) |

**Must fix before release:**
1. `natural_minor_pos4` beat 6: change to G string fret 14, correct the prose ("B string fret 14" → "G string fret 14")
2. `pentatonic_licks_1` Lick 5: replace with a distinct phrase
3. Blues chord strip: show I7–IV7–V7 or add explicit framing note

**Recommended before release:**
4. Bm/F label clarification in Track 02
5. Lydian lick key alignment to F
