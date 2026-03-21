# DiagramSpec — Diagram Specification

**Version**: 0.1
**Contract between**: Instructor (content author) and Developer (engine implementor)

This document defines every diagram type the engine can render. Instructors use these specs to write diagram directives inside lesson Markdown files. The engine renders them; it does not interpret music theory.

---

## How to Embed a Diagram in a Lesson

Use a fenced code block with the language tag `diagram`. The block body is YAML.

~~~markdown
```diagram
type: chord
...fields...
```
~~~

---

## Common Fields (all diagram types)

| Field     | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| `type`    | string | yes      | Diagram type: `chord`, `scale`, `tab`, `fretboard` |
| `title`   | string | no       | Display title above the diagram                  |
| `caption` | string | no       | Caption displayed below the diagram              |

---

## type: chord

Renders a chord box diagram (vertical grid, nut at top).

### Fields

| Field          | Type              | Required | Description |
|----------------|-------------------|----------|-------------|
| `frets`        | list[int\|null]   | yes      | 6 values (low E → high e). Integer = fret number (1-based); `0` = open string; `null` = muted (X). |
| `fingers`      | list[int\|null]   | no       | 6 values. Finger number 1–4; `null` = no finger label. |
| `barre`        | object            | no       | Barre chord indicator. See below. |
| `base_fret`    | int               | no       | Fret number at the top of the diagram (default: 1). Use for higher-position chords. |
| `dot_labels`   | list[str\|null]   | no       | 6 values (low E → high e). Label shown inside the dot cell instead of the default dot (≤2 chars; e.g., `"1"`, `"b3"`, `"5"`). Use `null` for strings with no dot or where default dot should show. |
| `root_strings` | list[int]         | no       | 0-based string indices (0 = low E) where the root note sits. Those dots render as `◉` instead of `●`. Ignored on strings that have a `dot_labels` entry. |

#### barre object

| Field    | Type | Required | Description |
|----------|------|----------|-------------|
| `fret`   | int  | yes      | Which fret the barre covers |
| `from`   | int  | yes      | Starting string (1 = low E) |
| `to`     | int  | yes      | Ending string (6 = high e) |
| `finger` | int  | no       | Finger number for the barre (usually 1) |

### Valid Values

- `frets` must have exactly 6 elements
- `fingers` must have exactly 6 elements if provided
- **Fret numbers are row numbers, not absolute fret numbers.** Row 1 = the first visible fret row (= `base_fret` on the real neck). Row 2 = `base_fret + 1`, etc. When `base_fret: 1` (default), row numbers equal absolute fret numbers. When `base_fret: 5`, row 1 = 5th fret, row 2 = 6th fret, etc.
- `0` = open string (shown with ○ above nut); `null` = muted (shown with X above nut)
- `barre.fret` is also a row number (same convention as `frets`)
- String order: index 0 = low E (string 6), index 5 = high e (string 1)

### Examples

```yaml
# Open G major
type: chord
title: G Major
frets: [3, 2, 0, 0, 0, 3]
fingers: [2, 1, null, null, null, 3]
```

```yaml
# F major (barre)
type: chord
title: F Major
frets: [1, 1, 2, 3, 3, 1]
fingers: [1, 1, 2, 3, 4, 1]
barre:
  fret: 1
  from: 1
  to: 6
  finger: 1
```

```yaml
# A major (open position)
type: chord
title: A Major
frets: [null, 0, 2, 2, 2, 0]
fingers: [null, null, 1, 2, 3, null]
```

```yaml
# Am barre at 5th fret — row numbers relative to base_fret: 5
# Row 1 = 5th fret, row 2 = 6th fret, row 3 = 7th fret
type: chord
title: A Minor (barre, 5th fret)
frets: [1, 1, 3, 3, 2, 1]
fingers: [1, 1, 3, 4, 2, 1]
base_fret: 5
barre:
  fret: 1       # row 1 = 5th fret
  from: 1
  to: 6
  finger: 1
```

---

## type: scale

Renders a scale pattern on a fretboard grid (horizontal strings, vertical frets).

### Fields

| Field       | Type              | Required | Description |
|-------------|-------------------|----------|-------------|
| `root`      | string            | yes      | Root note: `A`–`G`, optionally `#` or `b` (e.g., `"C"`, `"F#"`, `"Bb"`) |
| `positions` | list[ScaleNote]   | yes      | List of notes to highlight (see below) |
| `fret_range`| [int, int]        | no       | `[low, high]` fret range to display. Omit to auto-compute from the min/max frets in `positions`. Use `[0, 12]` for a full-neck view. |
| `highlight_root` | bool        | no       | Whether to visually distinguish root notes (default: true) |

#### ScaleNote object

| Field    | Type | Required | Description |
|----------|------|----------|-------------|
| `string` | int  | yes      | String number: 1 (high e) – 6 (low E) |
| `fret`   | int  | yes      | Fret number (0 = open) |
| `degree` | str  | no       | Scale degree label: `"1"`, `"b3"`, `"5"`, etc. |
| `root`   | bool | no       | True if this note is a root note (used for highlighting) |

### Examples

```yaml
type: scale
title: A Minor Pentatonic — Position 1
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

---

## type: tab

Renders a guitar tablature block (6-line staff with numbers).

### Fields

| Field    | Type         | Required | Description |
|----------|--------------|----------|-------------|
| `lines`  | list[TabLine]| yes      | Sequence of tab lines. Each line is a staff row rendered as a single block. |
| `tempo`  | int          | no       | BPM for reference (display only) |
| `time`   | string       | no       | Time signature (e.g., `"4/4"`) |

#### TabLine object

Exactly one of `beats` or `measures` must be provided.

| Field      | Type              | Required | Description |
|------------|-------------------|----------|-------------|
| `beats`    | list[TabBeat]     | one of   | Flat list of beats — treated as a single measure. Legacy format; no bar lines inserted. |
| `measures` | list[TabMeasure]  | one of   | List of measures; a `\|` bar line is inserted between each measure in the rendered output. |

#### TabMeasure object

| Field    | Type          | Required | Description |
|----------|---------------|----------|-------------|
| `beats`  | list[TabBeat] | yes      | Ordered list of beats/events in this measure |

#### TabBeat object

| Field        | Type                        | Required | Description |
|--------------|-----------------------------|----------|-------------|
| `notes`      | list[int\|null]             | yes      | 6 values (low E → high e). Integer = fret number; `null` = string not played this beat. Ignored when `rest: true`. |
| `label`      | string                      | no       | Beat label shown below the staff. See **Label convention** below. |
| `duration`   | int                         | no       | Number of beats the note rings for (default: `1`). Expands the column by `duration × col_width`. |
| `rest`       | bool                        | no       | If `true`, renders a rest symbol (`r`) on all strings instead of fret numbers (default: `false`). |
| `bend`       | bool                        | no       | If `true`, appends `b` to the fret number in the staff (default: `false`). |
| `bend_target`| int                         | no       | Target fret pitch for the bend. Renders as `8b10` (fret 8 bent to pitch of fret 10). Only meaningful when `bend: true`. |
| `vibrato`    | bool                        | no       | If `true`, appends `~` to the fret number in the staff (default: `false`). May combine with `bend`. |
| `technique`  | `"h"` \| `"p"` \| `"/"` \| `"\\"` \| null | no | Replaces the leading `─` of the beat's column with the technique connector on strings that have a note. `h` = hammer-on, `p` = pull-off, `/` = slide up, `\` = slide down. |

#### Label convention

Labels appear below the staff and are placed using **collision detection** into up to two rows (row A and row B). Each label is left-aligned starting directly under the fret digit of its beat. Row A is filled first; a label goes to row B only when it would overlap the previous row-A label. Only rows that contain at least one label are output.

**Labels should match what the diagram is teaching.** A label earns its place when it adds information the staff characters and surrounding prose do not already convey. Apply the following rules by context:

- **Technique-focused lessons** (hammer-ons, bends, slides, etc.) — label the teaching point: `pick`, `bend`, `rel`, `vib`, `bend~`. Technique characters (`h`, `p`, `/`, `\`) already appear as leading characters in the staff — do not echo them as labels below.
- **Note/scale-focused lessons** (fretboard geography, scale degrees) — note names or degree labels (`A`, `b3`, `5`, etc.) are appropriate when mapping fret numbers to note identity is the lesson's purpose.
- **Advanced and combining lessons** — use labels sparingly; by this point the reader has the vocabulary and clean tab is less cluttered.
- **Exercises and licks** — no labels. Drill material assumes prior knowledge; the player needs clean tab, not annotation.

| Label | Meaning |
|-------|---------|
| `pick` | Explicit pick attack — use when distinguishing a picked note from a legato continuation matters |
| `bend` | String bend — use on the beat where the bend is initiated |
| `rel`  | Release — use on the post-bend beat where the pitch returns |
| `vib`  | Vibrato |
| `bend~` | Bend held with vibrato (single beat combining both) |
| `1` `2` `3` `4` | Beat numbers |
| `rest` | Default label for `rest: true` beats |

Do not use `h`, `p`, `/`, `\` as labels — those characters already appear in the staff. In strumming exercises, `D` and `U` mean down-strum and up-strum — those are acceptable.

### Examples

```yaml
# Single measure — flat beats (legacy format)
type: tab
title: E Minor Arpeggio
tempo: 80
time: "4/4"
lines:
  - beats:
      - notes: [0, 2, 2, 0, 0, 0]
        label: "1"
      - notes: [null, null, null, null, 0, null]
        label: "2"
      - notes: [null, null, null, 0, null, null]
        label: "3"
      - notes: [null, null, 0, null, null, null]
        label: "4"
```

```yaml
# Bend and release with vibrato
type: tab
title: Whole-Step Bend — B string
lines:
  - beats:
      - notes: [null, null, null, null, 8, null]
        label: "bend"
        bend: true
        bend_target: 10
        duration: 2
      - notes: [null, null, null, null, 8, null]
        label: "rel"
        duration: 2
      - notes: [null, null, null, null, 7, null]
        label: "vib"
        vibrato: true
        duration: 2
```

```yaml
# Legato run with hammer-ons and pull-offs
type: tab
title: Legato Run — A minor pentatonic
lines:
  - beats:
      - notes: [null, null, null, null, 5, null]
        label: "pick"
      - notes: [null, null, null, null, 7, null]
        technique: "h"
        label: "h"
      - notes: [null, null, null, null, 8, null]
        technique: "h"
        label: "h"
      - notes: [null, null, null, null, 5, null]
        technique: "p"
        label: "p"
```

```yaml
# Four-measure chord progression — each chord rings for 4 beats
type: tab
title: G – D – Em – C
time: "4/4"
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
      - beats:
          - notes: [0, 2, 2, 0, 0, 0]
            label: "Em"
            duration: 4
      - beats:
          - notes: [null, 3, 2, 0, 1, 0]
            label: "C"
            duration: 4
```

---

## type: fretboard

Renders a full or partial fretboard overview — horizontal strings, with note labels or dots.

### Fields

| Field        | Type           | Required | Description |
|--------------|----------------|----------|-------------|
| `highlights` | list[FretNote] | yes      | Notes to highlight on the fretboard |
| `fret_range` | [int, int]     | no       | `[low, high]` fret range (default: `[0, 12]`) |
| `tuning`     | string         | no       | Tuning key from `tunings.yaml` (default: `"standard"`) |
| `show_notes` | bool           | no       | Show note names in dots (default: false, shows dots only) |

#### FretNote object

| Field    | Type   | Required | Description |
|----------|--------|----------|-------------|
| `string` | int    | yes      | String number: 1 (high e) – 6 (low E) |
| `fret`   | int    | yes      | Fret number |
| `label`  | string | no       | Text to display inside the dot (overrides `show_notes`) |
| `style`  | string | no       | Visual style: `"root"`, `"highlight"`, `"muted"` (default: `"highlight"`) |

### Examples

```yaml
type: fretboard
title: Natural Notes — Low E String
fret_range: [0, 12]
show_notes: true
highlights:
  - {string: 6, fret: 0, label: "E", style: "root"}
  - {string: 6, fret: 2, label: "F#"}
  - {string: 6, fret: 3, label: "G"}
  - {string: 6, fret: 5, label: "A"}
  - {string: 6, fret: 7, label: "B"}
  - {string: 6, fret: 8, label: "C"}
  - {string: 6, fret: 10, label: "D"}
  - {string: 6, fret: 12, label: "E", style: "root"}
```

---

## Versioning

When this spec changes in a breaking way (fields renamed, removed, or semantics changed), bump the version number in the header and update both the engine validation and this document in the same commit.
