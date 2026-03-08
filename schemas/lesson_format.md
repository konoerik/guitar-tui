# Lesson Format Specification

**Version**: 0.1
**Contract between**: Instructor (content author) and Developer (loader implementor)

This document defines the structure of lesson Markdown files. The content loader parses these files and feeds them to the TUI. All lesson files must conform to this spec.

---

## File Location

Lessons live in `guitar_tui/content/lessons/`. Each lesson is one `.md` file.

**Naming convention**: `{slug}.md` where slug matches the `slug` frontmatter field.

Example: `open_g_chord.md`

---

## File Structure

Every lesson file has two parts:

1. **YAML frontmatter** — delimited by `---` fences at the top of the file
2. **Markdown body** — the lesson content, after the second `---`

```
---
<frontmatter fields>
---

<lesson body>
```

---

## Frontmatter Fields

### Required

| Field           | Type         | Description |
|-----------------|--------------|-------------|
| `title`         | string       | Human-readable lesson title. Used in navigation and lesson header. |
| `slug`          | string       | URL-safe identifier. Must be unique across all lessons. Pattern: `[a-z0-9_]+` |
| `difficulty`    | string       | One of: `beginner`, `intermediate`, `advanced` |
| `tags`          | list[string] | Topic tags for filtering. Use kebab-case. Minimum 1 tag. |

### Optional

| Field           | Type         | Default | Description |
|-----------------|--------------|---------|-------------|
| `prerequisites` | list[string] | `[]`    | List of lesson slugs that should be completed first. |
| `see_also`      | list[string] | `[]`    | Related lesson slugs. Shown as a "See Also" line at the bottom of the lesson view. Missing slugs emit a warning. |
| `module`        | string       | `null`  | Module this lesson belongs to (e.g., `"open-chords"`). |
| `position`      | int          | `null`  | Ordering within module (lower = earlier). |
| `summary`       | string       | `null`  | One-sentence summary shown in lesson list. |
| `version`       | int          | `1`     | Lesson content version. Increment when content changes significantly. |

### Example Frontmatter

```yaml
---
title: The G Major Chord
slug: g_major_chord
difficulty: beginner
tags: [chords, open-chords, major-chords]
prerequisites: [holding_the_pick, fretting_hand_basics]
module: open-chords
position: 3
summary: Learn the open G major chord — one of the most-used chords in guitar.
---
```

---

## Lesson Body

The body is standard GitHub-flavored Markdown with two extensions:

1. **Diagram blocks** — fenced code blocks with language `diagram`
2. **Cross-references** — inline links to other lessons

### Headings

- Use `##` for major sections within a lesson (e.g., "Finger Placement", "Practice Tips")
- Use `###` for subsections
- Do not use `#` (H1) — the lesson title is rendered by the TUI from frontmatter

### Paragraphs and Lists

Standard Markdown. Ordered lists (`1.`, `2.`) for step-by-step instructions; unordered (`-`) for tips and notes.

### Emphasis

- `**bold**` for technical terms on first use and critical instructions
- `*italic*` for musical terms (e.g., *tonic*, *barre*)
- `` `code` `` for note names inline (e.g., `G`, `Bb`)

---

## Diagram Blocks

Embed diagrams using fenced code blocks with language `diagram`. The block body is YAML conforming to `schemas/diagram_spec.md`.

~~~markdown
```diagram
type: chord
title: G Major
frets: [3, 2, 0, 0, 0, 3]
fingers: [2, 1, null, null, null, 3]
```
~~~

- Multiple diagram blocks are allowed per lesson
- Diagrams render inline at the position they appear in the body
- The `title` field overrides the diagram's heading; omit it to show no heading

---

## Cross-References

Reference another lesson using the `[lesson:slug]` syntax:

```markdown
Before continuing, review [lesson:fretting_hand_basics].
```

The loader resolves this to a TUI-navigable link. If the slug does not exist, the loader logs a warning at startup (not a hard error).

Reference a section within the same lesson:

```markdown
See the [Practice Tips](#practice-tips) section below.
```

Standard Markdown anchors — section headings become anchors using the same rules as GitHub.

---

## Complete Example

```markdown
---
title: The G Major Chord
slug: g_major_chord
difficulty: beginner
tags: [chords, open-chords, major-chords]
prerequisites: [fretting_hand_basics]
module: open-chords
position: 3
summary: Learn the open G major chord — one of the most-used chords in guitar.
---

## Finger Placement

The G major chord uses three fingers and all six strings.

```diagram
type: chord
title: G Major
frets: [3, 2, 0, 0, 0, 3]
fingers: [2, 1, null, null, null, 3]
```

Place your **index finger** on the 2nd fret of the low `A` string (string 5).
Place your **middle finger** on the 3rd fret of the low `E` string (string 6).
Place your **ring finger** on the 3rd fret of the high `e` string (string 1).

## Common Mistakes

- Muting string 2 (B) with the ring finger — make sure it arches cleanly
- Not pressing close enough to the fret wire — causes buzzing

## Practice Tips

1. Place fingers one at a time before strumming
2. Strum slowly, checking each string rings clearly
3. Practice the [lesson:c_to_g_transition] chord change once comfortable
```

---

## Validation Rules

The loader enforces these rules at startup:

1. Frontmatter must parse as valid YAML
2. All required fields must be present and non-empty
3. `difficulty` must be one of the allowed values
4. `slug` must match the filename (without `.md`)
5. `slug` must be unique across all lessons
6. `prerequisites` slugs must exist (warning only, not error)
7. `tags` must have at least one entry

Violations of rules 1–6 are hard errors; the loader will not start.

---

## Versioning

When this spec changes in a breaking way, bump the version number in the header and update the loader validation and this document together.
