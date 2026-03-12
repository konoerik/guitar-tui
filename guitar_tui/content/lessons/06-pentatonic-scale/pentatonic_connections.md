---
title: Connecting the Five Positions
slug: pentatonic_connections
difficulty: intermediate
tags: [scales, pentatonic, minor-scales, fretboard]
prerequisites: [minor_pentatonic_p5]
licks: [pent_box1_run, pent_position2_run, pent_bend_release]
module: pentatonic-scale
position: 6
summary: See how all five positions of the A minor pentatonic form an unbroken chain across the entire neck.
---

## The Full Neck Picture

Each of the five positions occupies a window of roughly four frets. When arranged in sequence, they tile the neck from the open strings to the 15th fret with no gaps and no overlaps — each position's highest notes are the same pitches as the next position's lowest notes. That shared edge is the connection point.

The five positions and their root-string landmarks:

| Position | Fret range | Root sits on |
|----------|-----------|--------------|
| 5 | 2–5 | Strings 4, 1 (fret 2) |
| 1 | 5–8 | Strings 6, 4, 1 (fret 5) |
| 2 | 7–10 | Strings 4, 2 (frets 7/10) |
| 3 | 9–13 | Strings 5, 2 (frets 12/10) |
| 4 | 12–15 | Strings 5, 3 (frets 12/14) |

## Position 5 to Position 1

Position 5 (frets 2–5) ends where Position 1 (frets 5–8) begins. The high point of Position 5 is the root A at fret 5 on string 1 — which is also the low point of Position 1 (root A on the same string and fret).

```diagram
type: scale
title: A Minor Pentatonic — Position 5 (end of the chain)
root: A
fret_range: [2, 5]
positions:
  - {string: 6, fret: 3, degree: "b7"}
  - {string: 6, fret: 5, degree: "1", root: true}
  - {string: 5, fret: 3, degree: "b3"}
  - {string: 5, fret: 5, degree: "4"}
  - {string: 4, fret: 2, degree: "5"}
  - {string: 4, fret: 5, degree: "b7"}
  - {string: 3, fret: 2, degree: "1", root: true}
  - {string: 3, fret: 5, degree: "b3"}
  - {string: 2, fret: 3, degree: "4"}
  - {string: 2, fret: 4, degree: "b5"}
  - {string: 2, fret: 5, degree: "5"}
  - {string: 1, fret: 3, degree: "b7"}
  - {string: 1, fret: 5, degree: "1", root: true}
```

```diagram
type: scale
title: A Minor Pentatonic — Position 1 (beginning of the chain)
root: A
fret_range: [5, 8]
positions:
  - {string: 6, fret: 5, degree: "1", root: true}
  - {string: 6, fret: 8, degree: "b3"}
  - {string: 5, fret: 5, degree: "4"}
  - {string: 5, fret: 7, degree: "5"}
  - {string: 4, fret: 5, degree: "b7"}
  - {string: 4, fret: 7, degree: "1", root: true}
  - {string: 3, fret: 5, degree: "b3"}
  - {string: 3, fret: 7, degree: "4"}
  - {string: 2, fret: 5, degree: "5"}
  - {string: 2, fret: 8, degree: "b7"}
  - {string: 1, fret: 5, degree: "1", root: true}
  - {string: 1, fret: 8, degree: "b3"}
```

On both diagrams, find the root A at fret 5 on string 1. It is the last note you play descending through Position 5, and the first root you land on ascending through Position 1. That is the join.

## How to Practice Connections

The most effective approach is to learn one join at a time:

1. **Identify the shared edge.** Find the one or two notes that appear at the top of one position and the bottom of the next (same fret, same string, same pitch).
2. **Descend into and ascend out of the join.** Play the last four notes of position N, then the first four notes of position N+1, looping that small phrase until it feels natural.
3. **Play from the lowest root to the next root.** In Position 1, the lowest root is on string 6, fret 5. In Position 2, the next root up is on string 4, fret 7. Playing a phrase that starts on one root and ends on the other anchors both shapes in a musical context.
4. **Gradually extend.** Once you can connect positions 1–2 cleanly, connect 2–3, then 3–4, then 4–5, then 5–1. The full loop covers the entire neck.

## Putting It Into Music

The connection points are easier to hear than to describe. Three licks in [4] Practice demonstrate this directly: **Box 1 Ascending Run** stays within Position 1 and resolves to the root; **Position 2 Connector Run** crosses the 1→2 boundary and descends back; **Bend and Release** shows how expressive technique anchors you to a position even mid-phrase. Work through all three and notice where each one sits on the neck.

## The Goal

The five-position system is not five separate scales — it is one scale, described five different ways across the neck. When you can slide freely from position to position following the root notes, you have full neck access for A minor pentatonic in any key (since the shapes are moveable by key). Every note you need for an A minor blues solo exists somewhere in this continuous map.

## What's Next

With all five positions connected, the remaining lessons in this track explore the major pentatonic and the blues scale — extending the pentatonic palette with a brighter relative scale and a single added note that defines the blues sound.
