---
title: Vibrato
slug: vibrato_technique
difficulty: intermediate
tags: [technique, expressive, vibrato]
prerequisites: [string_bending]
module: expressive-techniques
position: 2
summary: Vibrato makes sustained notes sing by oscillating the pitch slightly — the mark of a developed lead guitar voice.
licks: [blues_bb_king_box]
---

## What Is Vibrato?

**Vibrato** oscillates a sustained note's pitch slightly above and below center. Done well, it makes a note feel alive and singing rather than static. In tab, `7~` means apply vibrato to the note at fret 7.

## Two Styles

**Blues/rock vibrato** pushes and releases the string rapidly — the same physical motion as a bend, but smaller and repeated. The note stays roughly in tune while fluctuating expressively. This is the style used by B.B. King, Clapton, Hendrix, and virtually all blues and rock players.

**Classical vibrato** rolls the fingertip forward and back along the string's length, producing a narrower, more controlled pitch variation. Used in fingerstyle and classical playing.

For blues and rock, use blues/rock vibrato.

## Reading Vibrato in Tab

```diagram
type: tab
title: Sustained Note with Vibrato — B string
lines:
  - beats:
      - notes: [null, null, null, null, 7, null]
        label: "pick"
        duration: 2
      - notes: [null, null, null, null, 7, null]
        label: "vib"
        vibrato: true
        duration: 4
```

Pick the note, let it sustain, then begin the vibrato motion. Do not re-pick — let the string keep ringing while your hand oscillates.

## Vibrato After a Bend

The most expressive combination in blues: bend to the target pitch, then apply vibrato while holding the bend. The pitch wavers *around* the bent pitch, not back down to the starting fret.

```diagram
type: tab
title: Bend and Hold with Vibrato — B string
lines:
  - beats:
      - notes: [null, null, null, null, 8, null]
        bend: true
        bend_target: 10
        duration: 1
      - notes: [null, null, null, null, 8, null]
        label: "vib"
        bend: true
        bend_target: 10
        vibrato: true
        duration: 3
```

The `8b10~` notation tells you: fret 8, bent to fret 10 pitch, with vibrato. The bend must be fully at pitch before the vibrato starts — wobbling during the rise sounds uncontrolled.

## Developing Vibrato

Consistent vibrato takes months of deliberate repetition:

1. Fret any note and pick it firmly
2. Begin small, slow oscillations — push slightly, release slightly, repeat
3. Gradually increase speed until the motion feels natural
4. Keep the hand relaxed — tension kills vibrato

Listen to B.B. King and David Gilmour. Notice how vibrato width and speed vary phrase to phrase — sometimes narrow and tight, sometimes wide and slow. Varying the character of your vibrato is itself a form of expression.

## Common Mistakes

- **Stopping the vibrato too soon** — let it continue for the full value of the note
- **Vibrato during the bend rise** — reach the pitch first, then add vibrato
- **Too fast at the start** — slow, wide vibrato has more weight than frantic oscillation
- **Re-picking the note** — vibrato sustains the note; picking again resets the phrase
