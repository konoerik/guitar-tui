# Physical Electronic Metronome — Behavior Reference

This document describes how a physical electronic metronome with LED indicators
behaves across regular and irregular time signatures. It serves as the reference
model for the Guitar TUI metronome widget implementation.

---

## The Physical Device

A typical two-LED electronic metronome (e.g. Korg MA-1, Boss DB-30) has:

- **One accent LED** — distinct color (red, orange, or bright white)
- **One beat LED** — secondary color (green or amber)

Some devices have a single LED that changes color. Some have a row of LEDs.
The two-LED model is the most common and the one this app targets.

The core principle: **one flash per beat, every beat**. The accent LED marks
beat 1. The beat LED marks every other beat. The player locks onto the
alternating rhythm and stops consciously watching — the flash becomes
peripheral background.

---

## Regular Time Signatures

### 2/4 — Two beats per bar

```
Beat:   |  1  |  2  |  1  |  2  |  1  |  2  |
Left:   | [R] |     | [R] |     | [R] |     |
Right:  |     | [G] |     | [G] |     | [G] |

[R] = red    [G] = green
```

Simple alternation. Left always red (every bar is only 2 beats, so left never
gets a green flash). The red flash marks every bar start.

---

### 3/4 — Three beats per bar (waltz)

```
Beat:   |  1  |  2  |  3  |  1  |  2  |  3  |
Left:   | [R] |     | [G] | [R] |     | [G] |
Right:  |     | [G] |     |     | [G] |     |
```

One accent, two regular beats. Left flashes red on beat 1, green on beat 3.
Right flashes green on beat 2. The player feels ONE-two-three as
red-right-green, repeating.

---

### 4/4 — Four beats per bar (common time)

The two LEDs bounce back and forth — left on odd beats, right on even beats.
Left flashes red on beat 1, green on beat 3. Right flashes green on beats 2 and 4.

```
Beat:   |  1  |  2  |  3  |  4  |  1  |  2  |  3  |  4  |
Left:   | [R] |     | [G] |     | [R] |     | [G] |     |
Right:  |     | [G] |     | [G] |     | [G] |     | [G] |
```

The bounce is the visual pendulum equivalent. The player tracks left-right-left-right
and the red interruption marks the bar start. Beat 3 (left, green) tells the player
"same side as the downbeat, but not the downbeat" — positional memory reinforces
the feel of the bar without counting.

---

### 6/8 — Six beats per bar (compound duple)

6/8 is felt in **two** main pulses, each subdivided into three:

```
Bar:    |  1  |  2  |  3  |  4  |  5  |  6  |
Feel:   |  ONE      |           |  TWO      |
LED:    | [R] | [G] | [G] | [Y] | [G] | [G] |

[Y] = secondary accent (yellow/orange) — beat 4 is the second strong pulse
```

At slow tempos: six distinct flashes. At performance tempo: the player feels
two pulses, not six. The secondary accent on beat 4 communicates the compound
structure. Without it, 6/8 is indistinguishable from 6 beats of straight time.

---

## Irregular Time Signatures

Irregular meters group beats asymmetrically. The accent LED alone is
insufficient — the player needs to know *where the groups fall*.

### 5/4 — Two common groupings

**3+2 feel** (most common — e.g. Dave Brubeck "Take Five"):

```
Bar:    |  1  |  2  |  3  |  4  |  5  |
Groups: |  ONE      |     |  TWO|
LED:    | [R] | [G] | [G] | [Y] | [G] |
```

**2+3 feel**:

```
Bar:    |  1  |  2  |  3  |  4  |  5  |
Groups: |  ONE|     |  TWO      |
LED:    | [R] | [G] | [Y] | [G] | [G] |
```

The secondary accent marks the second group start. Without it, the player
cannot feel the grouping from the LED alone.

---

### 7/8 — Three common groupings

**2+2+3**:

```
Bar:    |  1  |  2  |  3  |  4  |  5  |  6  |  7  |
Groups: | ONE |     | TWO |     |THREE      |
LED:    | [R] | [G] | [Y] | [G] | [Y] | [G] | [G] |
```

**3+2+2**:

```
Bar:    |  1  |  2  |  3  |  4  |  5  |  6  |  7  |
Groups: | ONE       |     |TWO  |     |THREE|
LED:    | [R] | [G] | [G] | [Y] | [G] | [Y] | [G] |
```

**2+3+2**:

```
Bar:    |  1  |  2  |  3  |  4  |  5  |  6  |  7  |
Groups: | ONE |     |TWO        |     |THREE|
LED:    | [R] | [G] | [Y] | [G] | [G] | [Y] | [G] |
```

---

## Summary: LED Color Roles

| Color | Role | Beats |
|-------|------|-------|
| Red | Primary accent | Beat 1 always |
| Yellow / Orange | Secondary accent | Group starts in compound/irregular meters |
| Green | Regular beat | All other beats |
| Off / dim | Silent | Between beats |

---

## Implementation Scope for Guitar TUI

### Phase 1 — to implement
- Two visual indicators (left and right), bouncing on every beat
- Left LED: odd beats — red on beat 1, green on beat 3, 5…
- Right LED: even beats — green always
- Beat count controls timing only, not visual count

### Phase 2 — next
- Secondary accent (yellow) for compound meters (6/8, 9/8, 12/8)
- Requires either: auto-detection of compound meter, or a grouping input

### Phase 3 — future
- Full irregular meter support with user-defined groupings (e.g. `2+3` for 5/4)
- Beat 3 secondary accent in 4/4 (optional, low priority)

---

## Key Implementation Principle

The visual display communicates **bar structure**, not beat count. A player
mid-practice should be able to glance at the screen and immediately know
"that's beat 1" from the red flash without counting. Everything else is secondary.
