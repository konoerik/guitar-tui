---
title: The Relative Minor
slug: relative_minor
difficulty: intermediate
tags: [music-theory, minor-scales, major-scales, fundamentals]
prerequisites: [major_scale_construction, roman_numerals]
module: theory-basics
position: 8
summary: Understand the relationship between every major key and its relative minor — and why they share the same scale.
---

## Every Major Key Has a Relative Minor

The **relative minor** of any major key is built on the 6th degree of that major scale. It uses the exact same notes — no sharps or flats added or removed — but treats a different note as the tonic (home).

- C major: C D E F G A B → relative minor starts on **A** → A natural minor
- G major: G A B C D E F# → relative minor starts on **E** → E natural minor
- A major: A B C# D E F# G# → relative minor starts on **F#** → F# natural minor

The formula for the natural minor scale — **1 – 2 – b3 – 4 – 5 – b6 – b7** — is exactly what you get when you start the major scale formula from its 6th degree.

## The A Minor — C Major Relationship

The most guitar-friendly example: C major and A minor share every note. The difference is emotional emphasis — which note feels like home.

```diagram
type: scale
title: A Natural Minor — Position 1 (key of A)
root: A
fret_range: [5, 8]
positions:
  - {string: 6, fret: 5,  degree: "1",  root: true}
  - {string: 6, fret: 7,  degree: "2"}
  - {string: 6, fret: 8,  degree: "b3"}
  - {string: 5, fret: 5,  degree: "4"}
  - {string: 5, fret: 7,  degree: "5"}
  - {string: 4, fret: 5,  degree: "b7"}
  - {string: 4, fret: 7,  degree: "1",  root: true}
  - {string: 3, fret: 5,  degree: "b3"}
  - {string: 3, fret: 7,  degree: "4"}
  - {string: 2, fret: 5,  degree: "5"}
  - {string: 2, fret: 6,  degree: "b6"}
  - {string: 2, fret: 8,  degree: "b7"}
  - {string: 1, fret: 5,  degree: "1",  root: true}
  - {string: 1, fret: 7,  degree: "2"}
  - {string: 1, fret: 8,  degree: "b3"}
```

```diagram
type: scale
title: C Major — Position 5 (same frets, same notes, different home)
root: C
fret_range: [5, 8]
positions:
  - {string: 6, fret: 5,  degree: "6"}
  - {string: 6, fret: 7,  degree: "7"}
  - {string: 6, fret: 8,  degree: "1",  root: true}
  - {string: 5, fret: 5,  degree: "2"}
  - {string: 5, fret: 7,  degree: "3"}
  - {string: 4, fret: 5,  degree: "5"}
  - {string: 4, fret: 7,  degree: "6"}
  - {string: 3, fret: 5,  degree: "1",  root: true}
  - {string: 3, fret: 7,  degree: "2"}
  - {string: 2, fret: 5,  degree: "3"}
  - {string: 2, fret: 6,  degree: "4"}
  - {string: 2, fret: 8,  degree: "5"}
  - {string: 1, fret: 5,  degree: "6"}
  - {string: 1, fret: 7,  degree: "7"}
  - {string: 1, fret: 8,  degree: "1",  root: true}
```

The physical fingering is identical. The degree labels differ because the interval reference point (the root) is different.

## Finding the Relative Minor

Given a major key, count up to its 6th degree to find the relative minor root:

| Major key | 6th degree | Relative minor |
|-----------|-----------|----------------|
| C | A | A minor |
| G | E | E minor |
| D | B | B minor |
| A | F# | F# minor |
| E | C# | C# minor |
| F | D | D minor |
| Bb | G | G minor |

To go the other direction — from minor to its relative major — count up three semitones (a minor 3rd). A minor → up 3 → C major.

## Practical Application

When you see a song in A minor (Am–F–C–G), you are looking at the vi–IV–I–V progression of C major. The C major and A minor pentatonic scales work over this progression because they share all their notes. The song *sounds* minor because Am is the tonic chord and is where phrases resolve — but the note pool is entirely drawn from the C major world.

Understanding this relationship means:
- One scale pattern covers both the major key and its relative minor
- A song that shifts between a minor tonic and a major tonic (Aeolian vs. Ionian feel) can be navigated with the same scale shapes
- You can predict which scale to use over a progression just by identifying the tonic chord

## What's Next

The relative minor relationship is the foundation for everything in Tracks 06–08. The minor pentatonic and natural minor scales introduced there are built on the Aeolian pattern described here, and the diatonic chord work in Track 08 builds directly on the Roman numeral and relative major/minor framework you now have.
