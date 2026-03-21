---
title: Slides
slug: slides
difficulty: intermediate
tags: [technique, expressive, slides]
prerequisites: [minor_pentatonic_intro]
module: expressive-techniques
position: 4
summary: A slide connects two fretted notes by gliding the fretting finger along the string — smoother and more vocal than jumping between positions.
licks: [slide_connector]
---

## What Is a Slide?

A **slide** keeps the string depressed while moving the fretting finger up or down the neck. The pitch glides continuously from one fret to another rather than jumping discretely.

In tab notation:

- `/` means slide up (ascending in pitch) to the next note
- `\` means slide down (descending in pitch) to the next note

## Slide Up

Fret the first note, pick it, and glide your finger up to the destination without releasing pressure:

```diagram
type: tab
title: Slide Up — G string
lines:
  - beats:
      - notes: [null, null, null, 5, null, null]
        label: "pick"
      - notes: [null, null, null, 9, null, null]
        technique: "/"
```

Maintain firm pressure throughout the slide. If you relax the string pressure, the note stops sounding before you arrive.

## Slide Down

The same motion in reverse:

```diagram
type: tab
title: Slide Down — B string
lines:
  - beats:
      - notes: [null, null, null, null, 9, null]
        label: "pick"
      - notes: [null, null, null, null, 5, null]
        technique: "\\"
```

Descending slides feel looser and more casual than ascending ones. Used frequently as a phrase ending — slide down from a peak note to let the phrase trail away.

## Position-Linking Slide

Slides are most practical for connecting pentatonic positions without an audible position shift. This phrase starts in position 1 on the D string, then slides up the B string to reach a higher area of the neck:

```diagram
type: tab
title: A Minor Pentatonic — Position Slide
lines:
  - beats:
      - notes: [null, null, null, 5, null, null]
      - notes: [null, null, null, 7, null, null]
        technique: "h"
      - notes: [null, null, null, null, 5, null]
        label: "pick"
      - notes: [null, null, null, null, 8, null]
      - notes: [null, null, null, null, 10, null]
        label: "vib"
        technique: "/"
        vibrato: true
        duration: 2
```

The slide from fret 8 to fret 10 on the B string (G to A, the b7 to the root) is the phrase's connection point — it carries the momentum of the ascending line and lands cleanly on the root with vibrato.

## Technique Points

- Use the **ring finger** for most slides — it combines strength and lateral control
- **Commit to the destination** — do not slow down at the end of the slide; the landing note carries the musical weight, not the glide itself
- **Short slides** (2–3 frets) sound bluesy and conversational; **long slides** (5+ frets) create cinematic sweeps between positions
- In ascending slides, the finger pressure naturally increases as you approach the higher fret — this is normal, not a mistake

## Practice

Start with short slides across 2–3 frets until the arrival note rings clearly and in tune. Then expand to longer slides. The **Slide Connector** lick in [4] Practice uses a slide to move between two pentatonic areas in A, with a held root note at the top.
