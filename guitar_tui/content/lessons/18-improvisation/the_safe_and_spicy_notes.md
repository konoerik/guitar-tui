---
title: The Safe Note and the Spicy Note
slug: the_safe_and_spicy_notes
difficulty: intermediate
tags: [improvisation, soloing, natural-minor, scales]
theory_refs: [scale:natural_minor, progression:minor_pop]
prerequisites: [beyond_one_scale, natural_minor_intro]
licks: [spicy_note_resolve]
module: improvisation
position: 2
summary: Adding B and F to the pentatonic box completes the natural minor scale — but the two notes could not behave more differently. B is safe to land anywhere; F demands resolution.
---

## Two Notes from a Full Scale

A minor pentatonic is five notes: A C D E G. A natural minor is seven:

| Scale | Notes | Degrees |
|-------|-------|---------|
| A Minor Pentatonic | A C D E G | 1 b3 4 5 b7 |
| A Natural Minor | A **B** C D E **F** G | 1 **2** b3 4 5 **b6** b7 |

You already knew this from the Natural Minor track. What that track did not
dwell on is that, for improvising, B and F are opposites — and treating them
identically is why "I added the extra notes and it sounded worse" happens.

## Where They Live in the Box

```diagram
type: scale
title: A Natural Minor — Position 1
root: A
fret_range: [5, 8]
positions:
  - {string: 6, fret: 5, degree: "1",  root: true}
  - {string: 6, fret: 7, degree: "2"}
  - {string: 6, fret: 8, degree: "b3"}
  - {string: 5, fret: 5, degree: "4"}
  - {string: 5, fret: 7, degree: "5"}
  - {string: 5, fret: 8, degree: "b6"}
  - {string: 4, fret: 5, degree: "b7"}
  - {string: 4, fret: 7, degree: "1",  root: true}
  - {string: 3, fret: 5, degree: "b3"}
  - {string: 3, fret: 7, degree: "4"}
  - {string: 2, fret: 5, degree: "5"}
  - {string: 2, fret: 6, degree: "b6"}
  - {string: 2, fret: 8, degree: "b7"}
  - {string: 1, fret: 5, degree: "1",  root: true}
  - {string: 1, fret: 7, degree: "2"}
  - {string: 1, fret: 8, degree: "b3"}
```

The additions to the pentatonic shape: **B** (the 2) at fret 7 on both E
strings, and **F** (the b6) at fret 8 on the A string and fret 6 on the B
string. Four new dots, two new notes.

## B — the Safe Note

B is the 2nd degree — over an Am chord it is the **9th**, and the 9th is one
of the prettiest colors available over a minor chord. You can land on it, hold
it, start phrases on it, end phrases on it. It works essentially everywhere in
the key. The instant payoff: pentatonic phrases that end on B stop sounding
"rock" and start sounding "melodic" — closer to a singer's note choice.

## F — the Spicy Note

F is the b6, a half step above the chord's 5th (E). That half step gives it
**gravity**: play F over Am and it audibly leans down onto E. Held, it is
dramatic, dark, unresolved. Resolved, it is the most emotional sound in
natural minor — film scores and classical minor-key melodies run on the
b6-to-5 sigh.

```diagram
type: tab
title: One phrase landing, one phrase leaning
caption: "Phrase one climbs to B (high E string, fret 7) and simply stays — the 9th needs no rescue. Phrase two climbs to F (B string, fret 6), holds the tension, then releases onto E. Same shape of phrase, opposite obligations."
lines:
  - measures:
      - beats:
          - notes: [null, null, null, null, 5, null]
          - notes: [null, null, null, null, 8, null]
          - notes: [null, null, null, null, null, 5]
          - notes: [null, null, null, null, null, 7]
            duration: 1
      - beats:
          - notes: [null, null, null, 5, null, null]
          - notes: [null, null, null, 7, null, null]
          - notes: [null, null, null, null, 6, null]
            duration: 1
          - notes: [null, null, null, null, 5, null]
            duration: 1
```

## Practice

1. Loop **Am**. Play pentatonic phrases that deliberately *end on B* (high E
   string, fret 7 is the easiest target). Notice you never feel the urge to
   move afterward.
2. Same loop, phrases that *end on F → E* (B string, fret 6 → fret 5). Lean
   on the F for a full beat before resolving. Then break the rule once: end on
   F and stop. Hear the difference between a question mark and a period.
3. Loop the minor pop progression **Am – F – C – G** (Key View in [3] Tools
   has it under A minor). Something interesting happens in bar two: over the
   F *chord*, the F *note* is suddenly the most consonant note you can play —
   it is the chord's root. The spicy note went safe because the chord
   underneath changed. Hold that thought.
4. **The Spicy Note Resolve** in [4] Practice works the b6 → 5 gesture as a
   complete looper phrase.

## What's Next

Step 3 gave it away: whether a note is a color or a tension depends on the
chord under it. The next lesson makes that concrete with the most famous case —
the second minor-key sixth, F#, and the chord that votes for it.
