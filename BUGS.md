# Known Bugs

## Priority: High

_(none)_

## Priority: Medium

### BUG-001 — Barre notation right-aligned in chord diagram cells

**Component**: `guitar_tui/engine/chord_renderer.py`
**Discovered**: M4 manual testing, after M4 dot-centering fix

**Symptom**
In a 3-char cell, the barre character `▬` appears at columns [1, 2] (0-based) instead
of being centered at column 1. The cell reads visually as right-aligned.

**Root cause**
`▬` (U+25AC BLACK RECTANGLE) is a wide Unicode character — 2 terminal columns wide.
The cell content `" ▬ "` is 3 bytes but 4 terminal columns (1 + 2 + 1), overflowing
the 3-column cell. The trailing space is dropped, leaving `▬` flush against the right
wall.

By contrast, `●` (U+25CF BLACK CIRCLE) is narrow (1 column), so `" ● "` = 3 columns
and centers correctly.

**Fix direction**
Either replace `▬` with a narrow character that still reads as "barre bar"
(e.g., a sequence of `─` chars, or a different single-wide block character),
or handle wide characters explicitly using `wcwidth`. Rich's `cell_len()` utility
can measure terminal width of a string. Revisit as part of a wider chord renderer
review once real lesson content exercises the diagrams in context.

**Workaround**
None. Barre chords still render and the affected strings are identifiable;
it is a cosmetic issue only.

## Priority: Low

_(none)_

---

# Feature Requests

## ~~FEAT-001~~ — Tab diagram: measure grouping with bar lines ✓ DONE

**Implemented**: M4 follow-up — `TabMeasure` model, `measures` field on `TabLine`, inter-measure bar lines in renderer.
**Requested by**: Instructor
**Component**: `schemas/diagram_spec.md`, `guitar_tui/engine/tab_renderer.py`, `guitar_tui/engine/models.py`
**Discovered need**: First real lesson (`g_d_em_c_progression`) — chord progression notation

---

### Problem

The current `tab` diagram type has a flat list of beats inside each `TabLine`. There is no
concept of a *measure* (bar). The renderer opens with `|`, adds all beats left-to-right,
and closes with `|` — it cannot insert a bar line between beats.

This makes it impossible to write standard notation for a chord progression where each
chord occupies one measure. The Instructor needs to express:

```
e |─3─|─2─|─0─|─0─|
B |─0─|─3─|─0─|─1─|
G |─0─|─2─|─0─|─0─|
D |─0─|─0─|─2─|─2─|
A |─2─|───|─2─|─3─|
E |─3─|───|─0─|───|
      G    D   Em   C
```

Without this, the only alternatives are:

- One beat per chord in a single line — all four chords crammed together with no bar lines,
  and no way to indicate duration
- One `TabLine` per chord — visually separated by blank lines, which implies line breaks in
  standard tab, not measure boundaries

Neither is correct notation.

---

### Proposed Schema Change

Replace the flat `beats` list in `TabLine` with a `measures` list, where each measure
contains its own `beats` list. The renderer inserts a `|` bar line between measures.

**New `TabLine` structure:**

```yaml
lines:
  - measures:
      - beats:
          - notes: [3, 2, 0, 0, 0, 3]
            label: "G"
      - beats:
          - notes: [null, null, 0, 2, 3, 2]
            label: "D"
      - beats:
          - notes: [0, 2, 2, 0, 0, 0]
            label: "Em"
      - beats:
          - notes: [null, 3, 2, 0, 1, 0]
            label: "C"
```

Each measure can hold one or more beats (one beat = one strum or note event). The renderer
inserts `|` between measures within the same staff line.

---

### Backwards Compatibility

Existing lessons use the current flat `beats` structure. A clean migration path would be:

- Accept both `beats` (flat, legacy) and `measures` (new, nested) on `TabLine`
- Flat `beats` is treated as a single measure — rendered identically to today
- New `measures` field enables multi-measure lines

This keeps the two stub lessons (`open_g_chord`, `minor_pentatonic_intro`) valid without
any content changes.

---

### Rendering Output

For the four-chord example above, the rendered output should be:

```
G – D – Em – C  (4/4)

e |─3─|─2─|─0─|─0─|
B |─0─|─3─|─0─|─1─|
G |─0─|─2─|─0─|─0─|
D |─0─|─0─|─2──2─|   ← beat label row below
A |─2─|───|─2─|─3─|
E |─3─|───|─0─|───|
      G    D   Em   C
```

Beat labels appear below the staff, centred under their measure's beats as today.

---

### Priority

**Medium** — not blocking current content, but needed before any lesson that teaches
chord progressions, rhythm patterns, or multi-measure musical phrases. This covers a large
portion of the planned curriculum.

---

## ~~FEAT-002~~ — Tab diagram: beat duration ✓ DONE

**Implemented**: M4 follow-up — `duration` field on `TabBeat`; column expands by `col_width × duration`.
**Requested by**: Instructor
**Component**: `schemas/diagram_spec.md`, `guitar_tui/engine/tab_renderer.py`, `guitar_tui/engine/models.py`
**Depends on**: FEAT-001 (measure grouping) — both features are needed together for correct chord progression notation

---

### Problem

The current `TabBeat` model has no concept of duration. Every beat occupies exactly one
column in the rendered output regardless of how long the note rings. In a 4/4 measure with
one chord strum, there is no way to represent the three remaining beats of silence/sustain.
The result looks identical to a one-beat note:

```
e |─3─|    ← looks like one beat, not four
```

What is needed:

```
e |─3──────|    ← clearly rings for four beats
```

Without duration, any tab that contains held chords or notes longer than one beat is either
unrepresentable or visually misleading.

---

### Proposed Schema Change

Add an optional `duration` field (integer, default `1`) to `TabBeat`. The value is the
number of beats the note rings for. The renderer fills `duration - 1` extra columns of
dashes after the note column.

**Example — G chord held for four beats in a 4/4 measure:**

```yaml
lines:
  - measures:
      - beats:
          - notes: [3, 2, 0, 0, 0, 3]
            label: "G"
            duration: 4
      - beats:
          - notes: [null, null, 0, 2, 3, 2]
            label: "D"
            duration: 4
```

**Rendered output:**

```
e |─3──────|─2──────|
B |─0──────|─3──────|
G |─0──────|─2──────|
D |─0──────|─0──────|
A |─2──────|────────|
E |─3──────|────────|
      G          D
```

The number of extra dash columns per duration unit is a renderer implementation detail
(e.g., `col_width * (duration - 1)` additional dashes appended to the note column).

---

### Interaction with FEAT-001

Duration and measures are complementary:

- **Measures** place bar lines at the right positions
- **Duration** fills the space *within* a measure correctly

Both are needed to accurately notate a chord progression. A chord with `duration: 4` inside
a 4/4 measure fills the full bar visually before the bar line.

---

### Backwards Compatibility

`duration` defaults to `1` — all existing content renders identically. No lesson files
need to change.

---

### Priority

**Medium** — same as FEAT-001. The two features should be designed and implemented
together.

---

## FEAT-003 — Cross-reference system: `see_also` field and typed inline links

**Requested by**: Instructor
**Component**: `schemas/lesson_format.md`, `guitar_tui/loaders/lesson_loader.py`, UI navigation layer
**Depends on**: nothing — can be implemented incrementally

---

### Problem

Lessons are self-contained, but they exist within a web of related content. Currently the
only relationship between pieces of content is `prerequisites` (sequential dependency).
There is no way to express:

- "Once you know this, the logical next step is…" (forward navigation)
- "This lesson uses the G chord — see the reference entry" (mention without diagram)
- "This progression works well with the minor pentatonic scale" (horizontal connection)
- "This technique appears in the Knopfler artist profile" (cross-area link)

The inline `[lesson:slug]` syntax exists in the spec but is not yet implemented in the
loader, and it only covers lesson-to-lesson links. Reference items (chords, scales),
artist profiles, and songbook entries cannot be referenced at all.

---

### Proposed Changes

#### 1. `see_also` frontmatter field

An optional unordered list of typed references. Displayed as a "See also" section at the
bottom of the lesson in the UI. Does not affect prerequisites or ordering.

```yaml
see_also:
  - lesson:minor_pentatonic_intro
  - chord:Am
  - scale:minor_pentatonic
  - artist:mark_knopfler
  - song:sultans_of_swing
```

Each entry is a string with the format `type:identifier`. Valid types:

| Type | Resolves to | Identifier |
|------|-------------|------------|
| `lesson` | Lesson by slug | lesson slug |
| `chord` | Reference chord entry | chord name (e.g. `Am`, `G`) |
| `scale` | Reference scale entry | scale name (e.g. `minor_pentatonic`) |
| `artist` | Artist profile | artist slug |
| `song` | Songbook entry | song slug |

Unresolvable references emit a warning at startup (same behaviour as missing
`prerequisites`) — they are never hard errors.

#### 2. Typed inline links in lesson body

Extend the existing `[lesson:slug]` syntax to all content types:

```markdown
The [chord:Am] chord works well here.
Try soloing with the [scale:minor_pentatonic] over this progression.
See [lesson:g_d_em_c_progression] for a practical application.
This is a hallmark of [artist:mark_knopfler]'s style.
```

The loader should extract these as structured references (not just pass them through as
raw text). The UI renders them as navigable links.

---

### Usage Principle

Cross-references are for content that is **mentioned but not shown**. If a chord diagram
is already displayed in the lesson, no link is needed — the reader can see it. Links are
for concepts referred to in prose that the reader might want to explore without leaving
the current lesson.

---

### Backwards Compatibility

`see_also` is optional and defaults to an empty list. Existing lessons without it are
unaffected. The inline link syntax is additive — plain text that happens to match
`[lesson:slug]` is already legal Markdown (it renders as bracketed text), so existing
content degrades gracefully if the feature is not yet implemented.

---

### UI Implications

- The lesson viewer needs a "See also" panel or footer section to render `see_also` entries
- Inline typed links need to be rendered as interactive elements, not plain text
- Each link type routes to a different screen (lesson viewer, chord reference, scale
  reference, artist profile, songbook entry)
- This feature is closely tied to the overall navigation design — coordinate with the
  UI/UX design session before implementing

---

### Priority

**Medium** — not blocking early content, but required before Songbook and Artist areas
are useful. Also needed before the curriculum grows large enough that discoverability
becomes a problem.

---

## ~~FEAT-004~~ — Multiple voicings per chord name ✓ DONE

**Implemented**: M4 follow-up — `ChordEntry` model, `ChordVoicing` gains `id`/`label`, `DataLoader.chords` is `dict[str, ChordEntry]`, voicing selector added to Reference tab.
**Requested by**: Instructor
**Component**: `guitar_tui/loaders/models.py`, `guitar_tui/loaders/data_loader.py`, `schemas/diagram_spec.md`, Reference UI
**Discovered**: Schema review — directly answers whether Am barre is accessible from reference

---

### Problem

`DataLoader.chords` is a `dict[str, ChordVoicing]` keyed by `name`. Loading two voicings
with the same name (e.g. Am open and Am barre) causes the second to silently overwrite
the first. The Reference tab's chord `Select` shows exactly one entry per name.

Consequence: alternate voicings of the same chord — open vs. barre, different positions,
different inversions — are unreachable from the reference UI. They can be written inline
in a lesson as `diagram` blocks (the diagram schema supports `base_fret` and `barre`
fully), but cannot be browsed or compared in reference.

This directly blocks Track 5 (Barre Chords) reference content and any lesson that wants
to compare voicings of the same chord side by side.

---

### Proposed Change

Replace `ChordVoicing` as the top-level data entry with a `ChordEntry` that groups
multiple voicings under one name:

```yaml
# chords/a_minor.yaml
name: Am
full_name: A minor
voicings:
  - id: open
    label: Open
    frets: [null, 0, 2, 2, 1, 0]
    fingers: [null, null, 2, 3, 1, null]
  - id: barre_5
    label: Barre (5th fret)
    frets: [0, 0, 2, 2, 1, 0]
    base_fret: 5
    fingers: [1, 1, 3, 4, 2, 1]
    barre: {fret: 5, from: 1, to: 6, finger: 1}
```

The Reference UI then shows a chord selector followed by a voicing selector (or a
cycle/tab control). The Instructor references a specific voicing in a `see_also` entry
using `chord:Am/barre_5`.

---

### Backwards Compatibility

Existing YAML files use a flat list of `ChordVoicing` objects. A migration option:
treat any file that lacks the `voicings` key as legacy — wrap the voicing in a single-
element voicings list with `id: default`. No lesson content changes required.

---

### Priority

**High** — blocks the entire barre chord reference area and any content that teaches
multiple voicings of the same chord. Should be resolved before Track 5 content is written.

---

## FEAT-005 — Chord diagram: note labels and root distinction on dots

**Requested by**: Instructor
**Component**: `schemas/diagram_spec.md`, `guitar_tui/engine/models.py`, `guitar_tui/engine/chord_renderer.py`
**Discovered**: Schema review — comparison with scale diagram capabilities

---

### Problem

`ChordSpec.fingers` accepts only integers 1–4 (finger numbers) or `null`. There is no
way to:

1. Label a dot with a note name (`G`, `B`, `D`) or scale degree (`1`, `3`, `5`)
2. Visually distinguish the root note from other chord tones

Scale diagrams have both: `ScaleNote.degree: str | None` for labels, and
`ScaleNote.root: bool` for root highlighting (■ vs ●). Chord diagrams have neither.

This gap blocks all chord construction and chord theory lessons (Tracks 4 and 9), where
understanding *which notes* are in a chord and *which is the root* is the entire point.

---

### Proposed Change

Add two optional fields to `ChordSpec`, parallel to the scale diagram:

```yaml
type: chord
title: G Major — notes
frets: [3, 2, 0, 0, 0, 3]
dot_labels: ["G", "B", "D", "G", "B", "G"]   # note names inside dots
root_strings: [0, 2, 5]                         # indices of root note dots (■ vs ●)
```

`dot_labels` is a 6-element list (matching `frets`). A label is only shown on fretted
strings (ignored for open strings and muted strings). `root_strings` is a list of
fret-array indices where the root marker style should be applied.

Alternatively, these could be merged into a richer `dots` field replacing `fingers`:

```yaml
dots:
  - string: 6, fret: 3, label: "G", root: true
  - string: 5, fret: 2, label: "B"
  - string: 4, fret: 0, label: "D"   # open string — label shown above nut, not in dot
```

The Developer should decide which approach fits the renderer architecture better.

---

### Priority

**Medium** — not blocking basic chord lessons, but required before any chord theory or
chord construction lesson can be written. Needed for Tracks 4 and 9.

---

## FEAT-006 — Tab: rest notation

**Requested by**: Instructor
**Component**: `schemas/diagram_spec.md`, `guitar_tui/engine/models.py`, `guitar_tui/engine/tab_renderer.py`
**Discovered**: Schema review

---

### Problem

`notes: [null, null, null, null, null, null]` (all strings silent) renders identically
to a sustained note — a column of dashes. There is no semantic distinction between
"this note is still ringing" and "deliberate silence (rest)". Rhythm exercises, call-
and-response phrasing, and any lesson on timing require rests.

---

### Proposed Change

Add an optional `rest: bool` field to `TabBeat` (default `false`). When `true`, the
renderer draws a rest symbol or a visually distinct column (e.g. a single `𝄽` character
centred on the staff, or a column of spaces instead of dashes) rather than dashes.

```yaml
beats:
  - notes: [0, 2, 2, 0, 0, 0]
    label: "1"
  - rest: true
    label: "2"
  - notes: [0, 2, 2, 0, 0, 0]
    label: "3"
  - rest: true
    label: "4"
```

The exact visual representation is a Developer decision. The semantic requirement is that
a rest is distinguishable from a held note at a glance.

---

### Priority

**Medium** — needed before rhythm and phrasing lessons can be written accurately.

---

## FEAT-007 — Chord diagram: tuning-aware string labels

**Requested by**: Instructor
**Component**: `schemas/diagram_spec.md`, `guitar_tui/engine/chord_renderer.py`
**Discovered**: Schema review — comparison with fretboard diagram

---

### Problem

The chord renderer has `_STRING_LABELS = ["E", "A", "D", "G", "B", "e"]` hardcoded.
`FretboardSpec` has a `tuning` field that allows alternate string labels; `ChordSpec`
does not. Any chord diagram shown in an alternate tuning lesson (Drop D, Open G, DADGAD)
will display incorrect string names in the header row.

---

### Proposed Change

Add an optional `tuning` field to `ChordSpec`, identical in behaviour to `FretboardSpec`:

```yaml
type: chord
title: G Major (Open G tuning)
tuning: open_g
frets: [0, 0, 0, 0, 0, 0]
```

The renderer looks up the tuning's string names from the tunings data (or a passed-in
list) and uses them in the header row instead of the hardcoded EADGBE labels. Default
behaviour (standard tuning) is unchanged.

---

### Priority

**Low** — not needed until alternate tuning lessons are written. Standard tuning covers
the entire beginner and intermediate curriculum.

---

## Minor gaps (no separate FEAT entry required)

### Thumb notation in `fingers` field

`fingers` accepts integers 1–4 only. Classical and fingerstyle technique uses the thumb
(T) on bass strings. A string value `"T"` or a dedicated sentinel would be needed for
fingerstyle lessons. **Priority: Low** — does not affect beginner or intermediate content.

### Single barre only per chord

`ChordSpec.barre` is a single `BarreDef`, not a list. Some advanced jazz voicings use
two independent partial barres. Extend to `list[BarreDef]` when needed.
**Priority: Low** — no planned lesson requires this in the near term.

### Key transposition in reference

Scale data is stored at a fixed reference key. The Reference tab can only show a scale
in that one key. Already deferred in DECISIONS.md (D5). Noting here for completeness.
**Priority: Medium** — needed before the reference becomes musically useful across keys.
