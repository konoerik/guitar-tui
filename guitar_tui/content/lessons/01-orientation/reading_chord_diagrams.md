---
title: Reading Chord Diagrams
slug: reading_chord_diagrams
difficulty: beginner
tags: [orientation, chord-diagrams]
module: orientation
position: 1
summary: Learn how to read the chord box diagrams used throughout this app.
---

## What Is a Chord Diagram?

A chord diagram represents a small section of the guitar neck seen head-on. It tells you exactly which strings to fret and where.

## The Grid

```diagram
type: chord
title: E Minor
frets: [0, 2, 2, 0, 0, 0]
fingers: [null, 2, 3, null, null, null]
```

The **string labels** across the top run left to right, from thickest to thinnest:

`E  A  D  G  B  e`

The **rows** below are frets. The doubled top border is the **nut** — the small bar at the top of the neck, near the headstock. Row 1 is the first fret, row 2 is the second, and so on.

A **filled dot** `●` marks where to press a string. In the E minor diagram above, you press the A string at fret 2 and the D string at fret 2. All other strings ring open.

## Open and Muted Strings

Two symbols appear above the nut:

| Symbol | Meaning |
|--------|---------|
| `○` | **Open string** — play without pressing any fret |
| `X` | **Muted string** — do not play this string |

In the E minor diagram, four strings have `○` — the low `E`, `G`, `B`, and high `e` all ring open.

Here is a chord with a muted string:

```diagram
type: chord
title: C Major
frets: [null, 3, 2, 0, 1, 0]
fingers: [null, 3, 2, null, 1, null]
```

The `X` on the low `E` means you must not strum it. Rest the edge of your picking hand lightly against it to keep it silent.

## Higher-Position Chords

When a chord sits above the 1st fret, the top border changes from the double-line nut to a plain border with a fret number label — for example, `5fr` means the first row is the 5th fret. Everything else reads the same way.

```diagram
type: chord
title: A Minor (5th position)
frets: [1, 1, 3, 3, 2, 1]
fingers: [1, 1, 3, 4, 2, 1]
base_fret: 5
barre:
  fret: 1
  from: 1
  to: 6
  finger: 1
```

## The Barre

A **barre** is when one finger — usually the index — presses all strings across an entire fret at once. It appears as a flat bar `▬` spanning several strings in the same row. Lay your finger flat at that fret and press firmly before adding the other fingers.

## Summary

| What you see | What it means |
|---|---|
| `E  A  D  G  B  e` at top | String names, low to high |
| Double top border | The nut — first-position chord |
| `5fr` label beside top border | First row = 5th fret |
| `○` above a string | Play open |
| `X` above a string | Mute — do not play |
| `●` in a cell | Press that string at that fret |
| `▬` spanning a row | Barre: one finger covers all marked strings |
