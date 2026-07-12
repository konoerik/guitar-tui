# Progression Format Specification

**Version**: 0.1
**Contract between**: Instructor (content author) and Developer (loader implementor)

This document defines the structure of the chord-progression data file used by
the M8 Theory Web (scale view, chord view, song analysis). The data loader
validates it on startup; invalid data is a hard error.

---

## File Location

One file: `guitar_tui/data/progressions.yaml`.

The file is **optional at load time** (minimal test data dirs may omit it),
but the packaged data directory always ships it — a test guards this.

---

## Structure

```yaml
progressions:
  - id: pop_four_chord            # required — [a-z0-9_]+, unique across the file
    name: "I–V–vi–IV"             # required — display name (use en dashes)
    quality: Major                # required — degree-table family, see below
    numerals: ["I", "V", "vi", "IV"]  # required — non-empty, validated
    description: >                # optional — one short paragraph, US English
      The four-chord pop loop…
    lessons: [g_d_em_c_progression]   # optional — lesson slugs that teach it
```

## Field Rules

- **quality** must be one of the degree-table families defined in
  `guitar_tui/theory/keys.py`: `Major`, `Minor`, `Blues`, `Dorian`,
  `Phrygian`, `Lydian`, `Mixolydian`. Pentatonic qualities are *not* valid
  here — consumers map them to their parent (`QUALITY_CHORD_PARENT`).
- **numerals** must be spelled exactly as in the quality's degree table
  (e.g. `vii°`, `bVII`, `I7`). The loader rejects unknown numerals at
  startup, so a typo fails fast rather than rendering wrong chords.
- **lessons** slugs are not validated by the data loader (it does not know
  about lessons); the content-verification test suite checks them instead.

## Consumption

`DataLoader.progressions` is a `dict[str, Progression]` keyed by id;
`DataLoader.progressions_for(quality)` filters by family in file order.
`theory.web.realize_progression(root, quality, numerals)` maps numerals to
concrete chord names for display.
