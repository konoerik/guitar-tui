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

| Field       | Type            | Required | Description |
|-------------|-----------------|----------|-------------|
| `frets`     | list[int\|null] | yes      | 6 values (low E → high e). Integer = fret number (1-based); `0` = open string; `null` = muted (X). |
| `fingers`   | list[int\|null] | no       | 6 values. Finger number 1–4; `null` = no finger label. |
| `barre`     | object          | no       | Barre chord indicator. See below. |
| `base_fret` | int             | no       | Fret number at the top of the diagram (default: 1). Use for higher-position chords. |

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
- Fret numbers are relative to `base_fret` when provided
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
# A major (higher position, muted low strings)
type: chord
title: A Major (open)
frets: [null, 0, 2, 2, 2, 0]
fingers: [null, null, 1, 2, 3, null]
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
| `lines`  | list[TabLine]| yes      | Sequence of tab lines. Each line is one "measure" or logical group. |
| `tempo`  | int          | no       | BPM for reference (display only) |
| `time`   | string       | no       | Time signature (e.g., `"4/4"`) |

#### TabLine object

| Field    | Type          | Required | Description |
|----------|---------------|----------|-------------|
| `beats`  | list[TabBeat] | yes      | Ordered list of beats/events in this line |

#### TabBeat object

| Field    | Type            | Required | Description |
|----------|-----------------|----------|-------------|
| `notes`  | list[int\|null] | yes      | 6 values (low E → high e). Integer = fret number; `null` = string not played this beat. |
| `label`  | string          | no       | Beat label (e.g., `"1"`, `"&"`, `"2"`) |

### Examples

```yaml
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
