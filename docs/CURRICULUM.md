# Guitar TUI — Curriculum

**Owner**: Instructor
**Purpose**: Defines all planned content — lessons, reference, exercises, and extended
content areas. Use this to plan the UI, scope data requirements, and sequence content
creation.

**Status markers**: ✓ = complete · ◑ = stub exists · ○ = planned

---

## Content Areas

The app has five distinct content areas. Each maps to a section of the UI.

| Area | Description |
|---|---|
| **Lessons** | Sequential, module-based learning content |
| **Reference** | Non-sequential quick-access charts and chord/scale libraries |
| **Exercises** | Focused technique drills with diagrams |
| **Songbook** | Theory analysis of real songs (see PLAN.md — future ideas) |
| **Artists** | Style profiles and original exercises (see PLAN.md — future ideas) |

---

## 1. Lessons

Organized into tracks. Each track is a self-contained learning arc. Tracks are
independent — a player can start at Theory Basics without completing Open Chords.
Within a track, lessons are ordered by `position`.

### Track 1 — Orientation

*Reading the app's diagram formats. No instrument knowledge assumed.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | reading_chord_diagrams | Reading Chord Diagrams | beginner | chord |
| ✓ | reading_tab | Reading Guitar Tab | beginner | tab |
| ✓ | reading_scale_diagrams | Reading Scale Diagrams | beginner | scale |
| ✓ | the_fretboard | The Guitar Fretboard | beginner | fretboard |

> **Note**: These are meta-lessons. They teach how to read diagrams, not how to play
> specific chords. `the_fretboard` shows all natural notes across all strings using the
> `fretboard` diagram type.

---

### Track 2 — Open Chords

*The ten essential open chord shapes. Ordered by physical difficulty.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | open_e_chord | The Open E Major Chord | beginner | chord |
| ✓ | open_em_chord | The Open E Minor Chord | beginner | chord |
| ✓ | open_a_chord | The Open A Major Chord | beginner | chord |
| ✓ | open_am_chord | The Open A Minor Chord | beginner | chord |
| ✓ | open_d_chord | The Open D Major Chord | beginner | chord |
| ✓ | open_dm_chord | The Open D Minor Chord | beginner | chord |
| ✓ | open_g_chord | The Open G Major Chord | beginner | chord |
| ✓ | open_c_chord | The Open C Major Chord | beginner | chord |
| ✓ | bm_chord | The Bm Chord | beginner | chord, tab |
| ✓ | f_major_chord | The F Major Chord | beginner | chord, tab |

> **Note**: Bm and F are technically barre chords but are taught early because they
> appear constantly in beginner progressions. Each lesson shows finger placement,
> common mistakes, and a brief arpeggio tab to check each string rings.

---

### Track 3 — First Progressions

*Connecting chords into musical sequences. Introduces strumming context.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | g_d_em_c_progression | The G–D–Em–C Progression | beginner | chord ×4, tab |
| ✓ | c_g_am_f_progression | The C–G–Am–F Progression | beginner | chord ×4, tab |
| ✓ | a_d_e_progression | The A–D–E Progression | beginner | chord ×3, tab |
| ✓ | twelve_bar_blues_a | 12-Bar Blues in A | beginner | chord ×3, tab |
| ✓ | one_four_five | The I–IV–V Progression | beginner | tab |
| ✓ | strumming_basics | Rhythm and Strumming Patterns | beginner | — |

> **Note**: `one_four_five` is the first theory-forward lesson — it explains Roman
> numeral notation and shows the same progression in multiple keys.

---

### Track 4 — Music Theory Basics

*How the fretboard is organized. Foundational for all scale and chord work.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | musical_alphabet | The Musical Alphabet | beginner | fretboard |
| ✓ | sharps_and_flats | Sharps, Flats, and Enharmonics | beginner | fretboard |
| ✓ | intervals | Intervals — Distance Between Notes | beginner | fretboard, tab |
| ✓ | major_scale_construction | Building the Major Scale | beginner | scale, fretboard |
| ✓ | key_signatures | Key Signatures and the Circle of Fifths | intermediate | fretboard |
| ✓ | chord_construction | How Chords Are Built from Scales | intermediate | chord, scale |
| ✓ | roman_numerals | Roman Numeral Notation | intermediate | chord ×4 |
| ✓ | relative_minor | The Relative Minor | intermediate | scale ×2, fretboard |

---

### Track 5 — Barre Chords

*Moveable chord shapes derived from open chord fingerings.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | barre_intro | What Is a Barre Chord? | intermediate | chord ×2 |
| ✓ | e_shape_major | The E-Shape Major Barre | intermediate | chord ×3 |
| ✓ | e_shape_minor | The E-Shape Minor Barre | intermediate | chord ×3 |
| ✓ | a_shape_major | The A-Shape Major Barre | intermediate | chord ×3 |
| ✓ | a_shape_minor | The A-Shape Minor Barre | intermediate | chord ×3 |
| ✓ | barre_progressions | Barre Chord Progressions | intermediate | chord ×4, tab |
| ✓ | caged_overview | The CAGED System | intermediate | chord ×5, fretboard |

---

### Track 6 — Pentatonic Scale

*The most practical scale for improvisation in rock, blues, and pop.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | minor_pentatonic_intro | Minor Pentatonic — Position 1 | intermediate | scale |
| ✓ | minor_pentatonic_p2 | Minor Pentatonic — Position 2 | intermediate | scale |
| ✓ | minor_pentatonic_p3 | Minor Pentatonic — Position 3 | intermediate | scale |
| ✓ | minor_pentatonic_p4 | Minor Pentatonic — Position 4 | intermediate | scale |
| ✓ | minor_pentatonic_p5 | Minor Pentatonic — Position 5 | intermediate | scale |
| ✓ | pentatonic_connections | Connecting the Five Positions | intermediate | scale ×2, fretboard |
| ✓ | major_pentatonic_intro | Major Pentatonic — Position 1 | intermediate | scale |
| ✓ | pentatonic_major_vs_minor | Major vs Minor Pentatonic | intermediate | scale ×2 |
| ✓ | blues_scale | The Blues Scale | intermediate | scale ×2 |

---

### Track 7 — Natural Minor Scale

*The foundation of minor keys, ballads, and classical-influenced playing.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | natural_minor_intro | The Natural Minor Scale | intermediate | scale, fretboard |
| ✓ | natural_minor_p1 | Natural Minor — Position 1 | intermediate | scale |
| ✓ | natural_minor_p2 | Natural Minor — Position 2 | intermediate | scale |
| ✓ | natural_minor_p3 | Natural Minor — Position 3 | intermediate | scale |
| ✓ | natural_minor_p4 | Natural Minor — Position 4 | intermediate | scale |
| ✓ | natural_minor_p5 | Natural Minor — Position 5 | intermediate | scale |
| ✓ | minor_scale_chords | Chords of the Minor Scale | intermediate | chord ×7 |

---

### Track 8 — Major Scale

*Full diatonic theory. Required for modes, chord extensions, and songwriting.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | major_scale_p1 | Major Scale — Position 1 | intermediate | scale |
| ✓ | major_scale_p2 | Major Scale — Position 2 | intermediate | scale |
| ✓ | major_scale_p3 | Major Scale — Position 3 | intermediate | scale |
| ✓ | major_scale_p4 | Major Scale — Position 4 | intermediate | scale |
| ✓ | major_scale_p5 | Major Scale — Position 5 | intermediate | scale |
| ✓ | major_scale_chords | Chords of the Major Scale | intermediate | chord ×7 |
| ✓ | diatonic_progressions | Diatonic Chord Progressions | intermediate | chord ×4, tab |

---

### Track 9 — Seventh Chords

*Adding colour and sophistication to chord vocabulary.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | dominant_7th | Dominant 7th Chords | intermediate | chord ×4 |
| ✓ | major_7th | Major 7th Chords | intermediate | chord ×4 |
| ✓ | minor_7th | Minor 7th Chords | intermediate | chord ×4 |
| ✓ | seventh_progressions | 7th Chord Progressions | intermediate | chord ×4, tab |
| ✓ | sus_and_add | Sus and Add Chords | intermediate | chord ×4 |

---

### Track 12 — Expressive Techniques

*Left-hand techniques that add pitch variation, flow, and character to melodic playing.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | string_bending | String Bending | intermediate | tab |
| ✓ | vibrato_technique | Vibrato | intermediate | tab |
| ✓ | hammer_ons_pull_offs | Hammer-ons and Pull-offs | intermediate | tab |
| ✓ | slides | Slides | intermediate | tab |
| ✓ | combining_techniques | Combining Expressive Techniques | intermediate | tab |

> **Note**: Positioned between Tracks 6 (Pentatonic) and 7 (Natural Minor) in the learning arc — prerequisites point to `minor_pentatonic_intro`, and the lick library now uses proper bend/vibrato/technique notation.

---

### Track 13 — Phrasing and Musicality

*Turning technique vocabulary into musical expression. Covers phrase shape, space, motif development, and rhythmic placement. Learning arc position: after Track 12.*

**Notation note:** Fully achievable with current engine. `rest: true` handles space/silence; `measures` + multi-`lines` handle longer phrases; `duration` and beat labels handle rhythmic placement.

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | phrase_shape | The Shape of a Phrase | intermediate | tab |
| ✓ | question_and_answer | Question and Answer Phrasing | intermediate | tab |
| ✓ | space_and_silence | Space and Silence | intermediate | tab |
| ✓ | motif_development | Motif Development | intermediate | tab |
| ✓ | rhythmic_placement | Rhythmic Placement | intermediate | tab |
| ✓ | building_a_solo | Building a Solo | intermediate | tab |

> **Note**: `combining_techniques` (Track 12) is effectively the first lesson of this arc — prerequisites chain naturally. Exercises: 2–3 phrase-shape drills. Licks: 3–4 new (question-answer phrase, space/rest phrase, motif example).

---

### Track 14 — Rhythm Depth

*Subdivision awareness, syncopation, strumming texture, and rhythmic lead playing. Learning arc position: between Tracks 6 and 7 — players learning to improvise need rhythm vocabulary simultaneously.*

**Notation notes:** D/U labels handle strumming patterns. `rest: true` + labels handle syncopation. Palm muting: no P.M. staff notation exists; use `caption:` field + prose (consistent with how ASCII tab handles this generally). Ghost strokes: approximate with `rest: true` + prose distinction.

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | subdivisions | Subdivisions — Quarters, Eighths, and Sixteenths | beginner | tab |
| ✓ | syncopation | Syncopation and the Backbeat | intermediate | tab |
| ✓ | sixteenth_strumming | 16th-Note Strumming Patterns | intermediate | tab |
| ✓ | palm_muting | Palm Muting | intermediate | tab |
| ✓ | ghost_strokes | Ghost Strokes and Rhythmic Muting | intermediate | tab |
| ✓ | rhythm_in_leads | Rhythm in Lead Playing | intermediate | tab |

> **Note**: Exercises: 3–4 (16th-note strumming drill, syncopation exercise, palm-muting pattern). Licks: 2–3 (syncopated pentatonic phrase, rhythmically displaced lick).

---

### Track 16 — Sounds and Scales Around the World

*Why does flamenco sound Spanish? Why does gypsy jazz never seem to resolve? Why does a whole-tone scale feel like it's floating? Each lesson starts from a sound the player recognises and traces it back to the interval or scale responsible. Learning arc position: standalone; most valuable after Track 10 (Modes), but accessible from Track 7 onward.*

**Notation note:** Each new scale requires a YAML data file following the existing scale pattern. ~5–6 new files. Scale diagrams (existing type) handle all visual content; tab licks use existing format.

**Framing note:** Not all musical character is scale-driven. Bossa nova's sound is jazz harmony + Brazilian rhythm, not a distinctive scale — this is noted explicitly rather than forcing a lesson where the premise doesn't hold. The track leads with the listening question, not the scale name.

| Status | Slug | Title | Distinctive interval | Cultural context |
|--------|------|-------|---------------------|-----------------|
| ✓ | harmonic_minor_sound | The Sound of Harmonic Minor | Augmented 2nd (b6→7) | Classical, metal, gypsy jazz |
| ✓ | phrygian_dominant | Phrygian Dominant — The Spanish Sound | b2 over major I | Flamenco, Middle Eastern, gypsy jazz |
| ✓ | hungarian_minor | Hungarian Minor — The Gypsy Sound | Two augmented 2nds | Romani music, Eastern European |
| ✓ | whole_tone_scale | The Whole Tone Scale — Floating and Unresolved | No half steps, no resolution | Debussy, impressionist jazz, film |
| ✓ | diminished_scale | The Diminished Scale — Tension and Symmetry | Symmetric whole-half / half-whole | Jazz, dramatic passages, horror film |
| ✓ | japanese_pentatonic | Japanese and East Asian Pentatonics | b2, omitted 3rd | Japanese koto music, game music, East Asian folk |

> **Data requirements:** ✓ done 2026-07-12 — all six scale YAML files shipped with M8 (the Japanese pentatonic file is named `hirajoshi.yaml` after the specific koto tuning taught, rather than the generic `japanese_pentatonic.yaml`). Licks: ✓ 1 per lesson (gypsy_cadence_run, spanish_descent, hungarian_aug_seconds, floating_whole_tone, diminished_tension_line, koto_phrase), all looper-ready, category `world`.

---

### Track 15 — Ear Training

*How to develop relative pitch — interval recognition, chord quality, transcription method, and singing what you play. Learning arc position: standalone; can begin after Track 4.*

**App limitation:** The app has no audio. This track teaches *how* to train your ear — methods, frameworks, and systematic practice routines — but the actual listening practice happens outside the app with the player's instrument and looper. This constraint is stated explicitly in the first lesson. The looper setup already present in the lick library partially bridges this: "looper ear exercises" instruct the player to record a phrase and listen back with specific attention targets, turning the looper into an ear training tool.

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ○ | ear_training_approach | How Ear Training Works | intermediate | tab (interval examples) |
| ○ | interval_recognition | Interval Recognition | intermediate | tab |
| ○ | chord_quality_by_ear | Chord Quality by Ear | intermediate | chord |
| ○ | transcription_basics | Transcription Basics | intermediate | — |
| ○ | singing_what_you_play | Singing What You Play | intermediate | — |

> **Note**: Mostly prose with minimal diagrams. A `listening_exercise:` section (Markdown convention, no engine change) could be added to lick files for the looper-as-ear-training format. No new diagram types needed.

---

### Track 17 — Your Equipment

*The gear side of playing, kept practical and vendor-neutral. Learning arc position:
standalone and unsequenced — no prerequisites beyond guitar_anatomy chaining within
the track; read any lesson when the topic comes up. Rationale: the app's practice
method assumes a looper (every lick's Looper Setup, phrasing/rhythm workflows, the
planned Track 15 bridge) but never explained one; lessons reference bridge, palm
placement, and distortion without anatomy or amp context for the returning-hobbyist
audience.*

**Scope guardrails:** No buying advice, prices, or model catalogs (dates fast,
opinion-laden). No setup/maintenance procedures (truss rod = "see a tech" sentence).
"Common guitars" deliberately reduced to the three families and what each changes
for the player. US English; "delay (echo)" is the taught term, echo noted as dated.

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | guitar_anatomy | Know Your Guitar | beginner | — |
| ✓ | amp_basics | Amplifier Basics | beginner | — |
| ✓ | effects_guide | Effects, One at a Time | beginner | — |
| ✓ | looper_guide | The Looper — Your Practice Partner | beginner | — |

> **Note**: Prose-only — no diagrams, no data files, no engine work. Module
> `equipment` is in the lesson view's practice-tab suppression list alongside
> `orientation` (no drills/licks apply). The looper guide is cross-linked from the
> Practice screen introduction and is prerequisite reading for Track 15's
> looper-as-ear-training format. Shipped 2026-07-16.

---

### Track 11 — Song Analysis

*Reverse-engineering the theory of real music. Builds on Tracks 4–8. Requires the
Theory Web (M7) to be in place for full value — the lessons teach the methodology,
the UI provides the tools.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | what_is_song_analysis | What Is Song Analysis? | intermediate | — |
| ✓ | finding_the_key | Finding the Key of a Song | intermediate | fretboard |
| ✓ | major_or_minor | Major or Minor — Identifying the Tonality | intermediate | scale ×2 |
| ✓ | chord_function_analysis | Chord Function Analysis | intermediate | chord ×4 |
| ✓ | scale_selection | Scale Selection | intermediate | scale, chord ×7 |
| ✓ | analysing_common_progressions | Analysing Common Progressions | intermediate | chord ×3, scale |
| ✓ | modal_progressions | Modal Progressions | intermediate | scale ×2, fretboard |
| ✓ | ear_training_basics | Ear Training Basics | intermediate | tab |
| ✓ | putting_it_together | Putting It All Together | advanced | chord ×4, scale, tab |
| ✓ | song_analysis_worksheet | The Song Analysis Worksheet | intermediate | — |

> **Note**: `analysis_walkthrough` is a capstone lesson — it works through a complete
> song analysis (key → scale → progression → positions → song feel) as a single
> end-to-end example. It should be one of the first Songbook entries.

---

### Track 10 — Modes

*Expanding beyond major and minor to modal colour.*

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | modes_intro | What Are Modes? | advanced | scale ×2, fretboard |
| ✓ | dorian_mode | The Dorian Mode | advanced | scale |
| ✓ | mixolydian_mode | The Mixolydian Mode | advanced | scale |
| ✓ | phrygian_mode | The Phrygian Mode | advanced | scale |
| ✓ | lydian_mode | The Lydian Mode | advanced | scale |
| ✓ | modes_in_context | Modes Over Chord Progressions | advanced | scale ×2, chord ×4, tab |

---

## 2. Reference

Quick-access content with no prerequisite structure. Browsable, not sequential.

### Chord Library

| Item | Description | Status |
|------|-------------|--------|
| Open chords — major | E, A, D, G, C | ✓ data |
| Open chords — minor | Em, Am, Dm | ✓ data |
| Open chords — other | Bm, F (barre) | ✓ data |
| Barre chords — E-shape major | All 12 keys (F through E) | ✓ data |
| Barre chords — E-shape minor | All 12 keys | ✓ data |
| Barre chords — A-shape major | All 12 keys | ✓ data |
| Barre chords — A-shape minor | All 12 keys | ✓ data |
| Dominant 7th — open | E7, A7, D7, G7, C7, B7 | ✓ data |
| Major 7th — open | Emaj7, Amaj7, Dmaj7, Gmaj7, Cmaj7, Fmaj7 | ✓ data |
| Minor 7th — open | Em7, Am7, Dm7, Bm7 | ✓ data |
| Power chords | E5, A5, D5, G5, C5 | ✓ data |
| Sus chords | Dsus2, Dsus4, Asus2, Asus4, Esus4, Gsus4 | ✓ data |
| Add chords | Cadd9, Gadd9 | ✓ data |

### Scale Library

| Item | Description | Status |
|------|-------------|--------|
| Minor pentatonic | 5 positions, key of A | ✓ data |
| Major pentatonic | 5 positions, key of C | ✓ data |
| Blues scale | 5 positions, key of A | ✓ data |
| Natural minor (Aeolian) | 5 positions, key of A | ✓ data |
| Major (Ionian) | 5 positions, key of C | ✓ data |
| Dorian | 5 positions | ✓ data |
| Phrygian | 5 positions | ✓ data |
| Lydian | 5 positions | ✓ data |
| Mixolydian | 5 positions | ✓ data |

### Theory Tables

| Item | Format | Status |
|------|--------|--------|
| Notes on each string (open to 12th fret) | text table | ✓ |
| Interval names and distances | static table | ✓ |
| Major scale interval formula | static text | ✓ |
| Circle of fifths | static text (TUI-friendly summary) | ✓ |
| Key signatures — major | static table (key / sharps / flats) | ✓ |
| Key signatures — minor | static table | ✓ |
| Common chord progressions by key | chord diagrams | ○ |
| CAGED system shapes | chord ×5 + fretboard | ○ |
| Diatonic chords — all major keys | static table | ✓ |

---

## 3. Exercises

Focused, repeatable drills. Not lessons — no prose explanation beyond the minimum
needed to perform the exercise correctly.

### Technique Exercises

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | chromatic_warmup | Chromatic Warm-Up | beginner | tab |
| ✓ | spider_exercise | Spider Exercise | beginner | tab |
| ✓ | one_minute_changes | One-Minute Chord Changes | beginner | chord ×2 |
| ✓ | alternate_picking | Alternate Picking on One String | beginner | tab |
| ✓ | string_skipping | String Skipping | intermediate | tab |
| ✓ | position_shifts | Position Shifts Across the Neck | intermediate | tab |

### Scale Exercises

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | pentatonic_sequences | Pentatonic in Sequences of Three | intermediate | tab |
| ✓ | major_scale_three_nps | Major Scale — Three Notes Per String | intermediate | tab |
| ✓ | natural_minor_positions | Natural Minor Position Linking | intermediate | tab |
| ✓ | pentatonic_licks_1 | Five Essential Pentatonic Licks | intermediate | tab ×5 |
| ✓ | major_scale_sequences | Major Scale Sequences — Diatonic Thirds | intermediate | tab |

### Chord Exercises

| Status | Slug | Title | Difficulty | Diagrams needed |
|--------|------|-------|------------|-----------------|
| ✓ | barre_strength | Barre Chord Strength Builder | intermediate | chord ×2 |
| ✓ | seventh_voicings | 7th Chord Voicing Practice | intermediate | chord ×4 |
| ✓ | open_chord_arpeggio | Open Chord Arpeggio Drill | beginner | chord, tab |
| ✓ | chord_melody_intro | Simple Chord Melody | advanced | tab |

---

## 4. Licks Library

Looper-ready melodic phrases organised by scale/mode category. Each lick
specifies a key, scale, backing chords, and feel/style tags. Designed to be
used with a loop pedal: record the backing, practise the phrase over it.

**Category order** (matches Practice screen display): pentatonic, blues,
major, natural_minor, dorian, phrygian, lydian, mixolydian.

| Status | Slug | Title | Key | Scale | Category |
|--------|------|-------|-----|-------|----------|
| ✓ | pent_box1_run | Box 1 Ascending Run | A | minor_pentatonic | pentatonic |
| ✓ | pent_bend_release | Bend and Release | A | minor_pentatonic | pentatonic |
| ✓ | pent_blues_turnaround | Blues Turnaround | A | minor_pentatonic | pentatonic |
| ✓ | pent_position2_run | Position 2 Connector Run | A | minor_pentatonic | pentatonic |
| ✓ | pent_position3_run | Position 3 — Dark Run | A | minor_pentatonic | pentatonic |
| ✓ | pent_position4_run | Position 4 — High-Energy Ascent | A | minor_pentatonic | pentatonic |
| ✓ | pent_position5_run | Position 5 — Neck Connector | A | minor_pentatonic | pentatonic |
| ✓ | blues_tritone_pass | Tritone Passing Tone | A | blues_scale | blues |
| ✓ | blues_bb_king_box | The B.B. King Box | A | minor_pentatonic | blues |
| ✓ | major_pent_country_walk | Country Walk | G | major_pentatonic | major |
| ✓ | major_scale_lower_run | Major Scale Lower-Neck Run | G | major | major |
| ✓ | major_scale_upper_phrase | Major Scale Upper-Neck Phrase | G | major | major |
| ✓ | natural_minor_descent | Natural Minor Descent | A | natural_minor | natural_minor |
| ✓ | natural_minor_pos2 | Natural Minor Position 2 — Night Walk | A | natural_minor | natural_minor |
| ✓ | natural_minor_pos3 | Natural Minor Position 3 — Rising Phrase | A | natural_minor | natural_minor |
| ✓ | natural_minor_pos4 | Natural Minor Position 4 — Classical Descent | A | natural_minor | natural_minor |
| ✓ | natural_minor_pos5 | Natural Minor Position 5 — Half-Step Rise | A | natural_minor | natural_minor |
| ✓ | dorian_groove | Dorian Groove Phrase | D | dorian | dorian |
| ✓ | phrygian_half_step | Phrygian Half-Step Descent | E | phrygian | phrygian |
| ✓ | lydian_raised_fourth | Lydian Raised Fourth Run | G | lydian | lydian |
| ✓ | mixolydian_b7_phrase | Mixolydian b7 Phrase | A | mixolydian | mixolydian |
| ✓ | phrygian_flamenco | Phrygian Flamenco Run | E | phrygian | phrygian |
| ✓ | mixolydian_chord_riff | Mixolydian Chord-Riff Hybrid | G | mixolydian | mixolydian |
| ✓ | legato_phrase | Legato Phrase | A | minor_pentatonic | pentatonic |
| ✓ | slide_connector | Slide Connector | A | minor_pentatonic | pentatonic |

---

## 5. Songbook

Theory breakdowns of real songs — key, mode, progression, scale, technique.

### Copyright policy

(Formerly deferred to IDEAS.md, which was never written — the policy lives here.)

- **Public domain songs** (the core of the Songbook): full worked examples — melody
  in tab, complete progression, chord voicings, section-by-section analysis.
- **Song vs. arrangement**: PD status covers the *traditional song*, not a famous
  recording's arrangement. Analyze the traditional changes and melody with our own
  voicings and patterns; never transcribe a specific recording note-for-note
  (House of the Rising Sun ≠ The Animals' arpeggiation; Scarborough Fair ≠ Simon &
  Garfunkel).
- **Jurisdiction**: the app ships worldwide — require life+70 on the *composer*,
  not just US pre-1931 publication (rules out e.g. Lecuona's Malagueña in the EU).
  Traditional/anonymous tunes, Foster, Bach, Beethoven, Carulli, Sor, Tárrega all clear.
- **Copyrighted songs**: chords and functions are not copyrightable, melodies are.
  Entries for copyrighted songs are abstract analyses only (key, progression,
  functions, scale advice) — no melody tab, no lyrics, ever.

### PD worked examples — ongoing effort (started 2026-07-16)

Approach one at a time; each entry doubles as a worksheet-v1 field test and a
Songbook draft. Classical guitar studies close with a **loop-and-solo** section —
the piece's own progression becomes the looper backing for improvisation, tying
the Songbook into the app's core practice method.

**Stage 0 (blocks the first entry):** decide the entry format/vehicle with the
Developer — likely reuse of lesson Markdown + existing diagram types under a
`songbook` content dir, rendered through the existing machinery; per ADR D12 the
section-based analysis schema is shared with worksheet v2/v3. No new engine work
expected (tab renderer has no p-i-m-a fingering — classical picks stay within the
existing tab spec, which keeps repertoire difficulty honest).

| Status | Song | Teaches | Ties to |
|--------|------|---------|---------|
| ○ 1 | House of the Rising Sun (trad.) | Flagship Four Questions workout: minor key mixing natural minor, major IV, harmonic-minor V; 6/8 | Track 11, harmonic minor |
| ○ 2 | Scarborough Fair (trad.) | The Dorian example | dorian_mode, dorian_vamp |
| ○ 3 | Amazing Grace | Major-pentatonic melody over I–IV–V; 3/4 | major pentatonic, Track 3 |
| ○ 4 | Lágrima — Tárrega | Parallel major/minor in 16 bars (E→Em); classical phrasing | Track 7, relative vs parallel |
| ○ 5 | Carulli arpeggio study (C/Am; opus TBD at authoring) | Arpeggiated I–V–I; loop-and-solo | Track 3, looper workflow |
| ○ 6 | Greensleeves (trad.) | Natural vs harmonic minor alternating; 6/8 | Track 7, Track 16 |
| ○ 7 | Wayfaring Stranger (trad.) | Straight natural minor with V | Track 7 |
| ○ 8 | Old Joe Clark (trad.) | The Mixolydian fiddle tune | mixolydian_mode |
| ○ 9 | Drunken Sailor (trad.) | i–bVII Dorian vamp at its simplest | dorian_vamp |
| ○ 10 | Hava Nagila (trad. melody) | Phrygian dominant / Freygish in the wild | phrygian_dominant |
| ○ 11 | St. James Infirmary (trad.) | Minor blues | Track 3 blues, Track 6 |
| ○ 12 | Frankie and Johnny (trad.) | 12-bar ancestry | twelve_bar_blues_a |
| ○ 13 | Romanza (anon.) | Em arpeggio piece; loop-and-solo | Track 7, looper workflow |
| ○ 14 | Bourrée in Em — Bach | Classical minor-key analysis; famous guitar repertoire | Tracks 7, 16 |
| ○ 15 | When the Saints / Oh! Susanna (Foster) | Simplest major-key functions | Track 3 |
| ○ 16 | Auld Lang Syne (trad.) | Pentatonic melody; 3/4 | major pentatonic |
| ○ 17 | Sakura (trad.) | Hirajoshi in actual repertoire | japanese_pentatonic |
| ○ 18 | Ode to Joy — Beethoven | Full entry expanding the chord-melody exercise | chord_melody_intro |

*Optional later: Adelita (Tárrega), Sor Op. 35 No. 22 (Bm), Swing Low Sweet Chariot,
Shenandoah, Man of Constant Sorrow.*

### Copyrighted-song candidates (abstract analyses only, unscheduled)

- Sultans of Swing — Dire Straits (D minor, pentatonic, hybrid picking)
- Wonderful Tonight — Eric Clapton (G major, I–V–vi–IV)
- Wish You Were Here — Pink Floyd (G, Am, C, D — fingerpicking)
- Knockin' on Heaven's Door — Bob Dylan (G–D–Am / G–D–C, beginner-friendly)

---

## 5. Artists

Style profiles with original licks and exercises. See IDEAS.md for scope definition.

*Initial candidates:*

- Mark Knopfler — fingerstyle, Dorian, D minor pentatonic, pull-off runs
- Eric Clapton — blues phrasing, minor pentatonic, SRV influence
- Jimi Hendrix — chord-melody, thumb bass, pentatonic vocabulary
- BB King — vibrato, call-and-response, position 1 pentatonic mastery
- David Gilmour — melodic soloing, sustain, major pentatonic, space

---

## Data Requirements Summary

Items below require new YAML data files before lessons or reference content can be
written.

| Data file | Contents | Required by |
|-----------|----------|-------------|
| `data/scales/major_pentatonic.yaml` | 5 positions, key of C | Track 6, Reference |
| `data/scales/blues_scale.yaml` | 5 positions, key of A | Track 6, Reference |
| `data/scales/natural_minor.yaml` | 5 positions, key of A | Track 7, Reference |
| `data/scales/major.yaml` | 5 positions, key of C | Track 8, Reference |
| `data/scales/dorian.yaml` | 5 positions | Track 10, Reference |
| `data/scales/mixolydian.yaml` | 5 positions | Track 10, Reference |
| `data/scales/phrygian.yaml` | 5 positions | Track 10, Reference |
| `data/scales/lydian.yaml` | 5 positions | Track 10, Reference |
| `data/chords/barre_chords.yaml` | E-shape and A-shape, all 12 keys, major + minor | Track 5, Reference |
| `data/chords/seventh_chords.yaml` | Dom7, maj7, min7 — open voicings | Track 9, Reference |
| `data/chords/extended_chords.yaml` | Sus, add, power chords | Reference |

---

## Lesson Count Summary

| Track | Lessons planned | Complete | Stubs |
|-------|----------------|----------|-------|
| 1 — Orientation | 5 | 5 | 0 |
| 2 — Open Chords | 10 | 10 | 0 |
| 3 — First Progressions | 6 | 6 | 0 |
| 4 — Theory Basics | 8 | 8 | 0 |
| 5 — Barre Chords | 7 | 7 | 0 |
| 6 — Pentatonic | 9 | 9 | 0 |
| 7 — Natural Minor | 7 | 7 | 0 |
| 8 — Major Scale | 7 | 7 | 0 |
| 9 — Seventh Chords | 5 | 5 | 0 |
| 10 — Modes | 6 | 6 | 0 |
| 11 — Song Analysis | 10 | 10 | 0 |
| 12 — Expressive Techniques | 5 | 5 | 0 |
| 13 — Phrasing and Musicality | 6 | 6 | 0 |
| 14 — Rhythm Depth | 6 | 6 | 0 |
| 15 — Ear Training | 5 | 0 | 0 |
| 16 — Sounds and Scales Around the World | 6 | 6 | 0 |
| **Total** | **108** | **103** | **0** |

Exercises: 14 complete; ~10 planned for Tracks 13–14.
Licks: 25 complete; ~5–7 planned for Tracks 13–14.
