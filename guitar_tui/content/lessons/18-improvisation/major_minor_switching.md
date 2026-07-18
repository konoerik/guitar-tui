---
title: The Major–Minor Switch
slug: major_minor_switching
difficulty: intermediate
tags: [improvisation, soloing, pentatonic, blues, major-pentatonic]
theory_refs: [scale:major_pentatonic, scale:minor_pentatonic, progression:twelve_bar]
prerequisites: [the_chords_vote, pentatonic_major_vs_minor]
licks: [major_minor_switch, blues_bb_king_box]
module: improvisation
position: 4
summary: Over a blues, A major pentatonic and A minor pentatonic are both available — and switching between them phrase by phrase is the oldest, most expressive trick in electric blues soloing.
---

## Borrowing a Whole Color

Every rung so far added a note *within* minor. This one borrows from the
parallel major: **A major pentatonic** — A B C# E F#. You met the shapes in
the Pentatonic track's major-versus-minor lesson; what that lesson deliberately
left for later is the move that makes them famous: using **both scales in the
same solo**, alternating phrase by phrase.

One honest caveat before the fun: this rung lives in the **blues**. Over a
strictly minor backing, the major scale's C# collides with the key's C
natural. But a blues in A is built on dominant chords (A7–D7–E7) that blur the
major/minor boundary on purpose — the form practically *asks* for both colors.
B.B. King's entire vocabulary switches between them; so does almost every
blues solo you have ever admired.

## The Relocation Trick

You do not need a new pattern. A major pentatonic is **the minor pentatonic
box you already know, moved down three frets** — the same shape at frets 2–5
now yields A B C# E F#, with the roots in new places inside the shape:

```diagram
type: scale
title: A Major Pentatonic — Frets 2–5 (the familiar shape, relocated)
root: A
fret_range: [2, 5]
positions:
  - {string: 6, fret: 2, degree: "6"}
  - {string: 6, fret: 5, degree: "1",  root: true}
  - {string: 5, fret: 2, degree: "2"}
  - {string: 5, fret: 4, degree: "3"}
  - {string: 4, fret: 2, degree: "5"}
  - {string: 4, fret: 4, degree: "6"}
  - {string: 3, fret: 2, degree: "1",  root: true}
  - {string: 3, fret: 4, degree: "2"}
  - {string: 2, fret: 2, degree: "3"}
  - {string: 2, fret: 5, degree: "5"}
  - {string: 1, fret: 2, degree: "6"}
  - {string: 1, fret: 5, degree: "1",  root: true}
```

Careful with the roots: in the minor box the root sat under your first finger
on the low E string; here the low E string's fret 5 note is still A, but it is
now the *top* of the shape. Spend a minute finding the three roots (low E
fret 5, G string fret 2, high E fret 5) before improvising — losing the root
is how the relocation trick goes wrong.

## The Switch

The two scales carry opposite moods over the same chord: major pentatonic is
bright, sweet, almost country; minor pentatonic is tough and vocal. The craft
rule that organizes them:

> **Switch at phrase boundaries, not mid-phrase.** Complete a thought in one
> color, breathe, answer it in the other.

```diagram
type: tab
title: A phrase pair — major statement, minor answer
caption: "Bar one, A major pentatonic: A – B – C# up to a held E — bright and open. Bar two, A minor pentatonic: C – A – G falling to the same E — the tough answer. Same key, same final note, opposite characters."
lines:
  - measures:
      - beats:
          - notes: [null, null, null, 2, null, null]
          - notes: [null, null, null, 4, null, null]
          - notes: [null, null, null, null, 2, null]
          - notes: [null, null, null, null, 5, null]
            duration: 1
      - beats:
          - notes: [null, null, null, null, null, 8]
          - notes: [null, null, null, null, null, 5]
          - notes: [null, null, null, null, 8, null]
          - notes: [null, null, null, null, 5, null]
            duration: 1
```

A useful starting map for the 12-bar form: favor **major over the I chord**
(A7 — the C# is the chord's 3rd, maximally sweet) and **minor over the IV**
(D7 — the C natural is the chord's b7, maximally bluesy). That one guideline
already produces the classic sound; refine from there by ear.

## Practice

1. Loop a slow **12-bar blues in A** (A7 – D7 – E7; Track 3's 12-bar lesson
   has the form). Solo one full chorus in major pentatonic only, one in minor
   only. Learn each color pure before mixing.
2. Now alternate by phrase: statement in major, answer in minor. Force the
   switch every phrase for a chorus — mechanical first, musical later.
3. Apply the map: major over A7, minor over D7, your choice over E7. Hear how
   the switch lands hardest at the bar 5 arrival of the IV chord.
4. **Major–Minor Phrase Pair** in [4] Practice is the switch as a lick;
   **The B.B. King Box** shows the master's favorite neighborhood for it.

## What's Next

The switch borrowed a parallel scale for a whole phrase. The next rung is
sharper: one borrowed note, for exactly one chord — the most dramatic single
half step in minor-key music.
