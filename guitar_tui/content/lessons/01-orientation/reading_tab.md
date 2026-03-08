---
title: Reading Guitar Tab
slug: reading_tab
difficulty: beginner
tags: [orientation, tab]
prerequisites: [reading_chord_diagrams]
module: orientation
position: 2
summary: Learn how to read guitar tablature — the six-line notation used for melodies, riffs, and progressions.
---

## What Is Tab?

Guitar tab (*tablature*) is a simple notation that tells you where to place your fingers without requiring you to read music. It uses six horizontal lines — one per string — with numbers that show which fret to press.

## The Six Lines

The six lines represent the six strings. **The top line is the high `e` (thinnest); the bottom line is the low `E` (thickest).** This is the reverse of how the guitar sits in your lap — imagine the neck tilted up to face you.

```diagram
type: tab
title: Open Strings
lines:
  - beats:
      - notes: [0, 0, 0, 0, 0, 0]
        label: "strum"
```

Each line is labelled on the left: `e  B  G  D  A  E` from top to bottom.

## Numbers Mean Frets

A number tells you which fret to press on that string. **`0` means play the string open — no finger on the fret.**

```diagram
type: tab
title: Low E String — Open to 4th Fret
lines:
  - beats:
      - notes: [0, null, null, null, null, null]
        label: "0"
      - notes: [1, null, null, null, null, null]
        label: "1"
      - notes: [2, null, null, null, null, null]
        label: "2"
      - notes: [3, null, null, null, null, null]
        label: "3"
      - notes: [4, null, null, null, null, null]
        label: "4"
```

A string with no number at a given position is silent for that beat — the `─` dashes are just the staff lines, not instructions to play.

## Reading Chords

When numbers stack vertically, play all of them at the same time. This is a G major chord written in tab — strum straight across all six strings:

```diagram
type: tab
title: G Major
lines:
  - beats:
      - notes: [3, 2, 0, 0, 0, 3]
        label: "G"
```

## Bar Lines and Measures

Vertical `|` lines divide the music into **measures**. Read left to right, one measure at a time. In 4/4 time, each measure holds four beats. A label below the staff can name the chord or beat number:

```diagram
type: tab
title: Four Chords — One Per Measure
time: "4/4"
lines:
  - measures:
      - beats:
          - notes: [3, 2, 0, 0, 0, 3]
            label: "G"
            duration: 4
      - beats:
          - notes: [0, 2, 2, 0, 0, 0]
            label: "Em"
            duration: 4
      - beats:
          - notes: [null, 3, 2, 0, 1, 0]
            label: "C"
            duration: 4
      - beats:
          - notes: [null, null, 0, 2, 3, 2]
            label: "D"
            duration: 4
```

## What Tab Does Not Show

Tab tells you *where* to play but not exactly *how long* each note rings. A `3` on the low E could be a quick pluck or a long sustain. Labels, tempo markings, and your ear fill in the rhythm. When a lesson includes a time signature or tempo, use that context to judge timing.

## What's Next

Now that you can read chord diagrams and tab, the orientation track closes with scale diagrams — the horizontal fretboard notation used throughout the scale and mode lessons. After that, Track 02 begins with the open chords you will strum using the rhythms tab notation describes.
