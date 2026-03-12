# Known Bugs and Feature Requests

## Open Bugs

_(none)_

---

## Open Feature Requests

### FEAT-007 — Chord diagram: tuning-aware string labels

**Component**: `guitar_tui/engine/chord_renderer.py`
**Priority**: Low — not needed until alternate tuning lessons are written

The chord renderer has `_STRING_LABELS = ["E", "A", "D", "G", "B", "e"]` hardcoded.
Any chord diagram in an alternate tuning lesson (Drop D, Open G, DADGAD) will display
incorrect string names. Add an optional `tuning` field to `ChordSpec` mirroring the
existing `FretboardSpec.tuning` field.

---

### Minor gaps (no separate entry required)

- **Thumb notation** — `fingers` accepts integers 1–4 only. Classical/fingerstyle thumb
  (T) not supported. Low priority — no planned lesson requires it.
- **Single barre per chord** — `ChordSpec.barre` is a single `BarreDef`. Advanced jazz
  voicings with two independent partial barres not supported. Low priority.

---

## Resolved

| ID | Summary | Resolution |
|----|---------|------------|
| BUG-001 | Barre `▬` right-aligned in chord cells (wide Unicode) | Resolved — renders correctly in current terminal |
| BUG-002 | Tab key cycles within active tab instead of switching | Resolved — `t` binding cycles Key View ↔ Reference tabs |
| BUG-003 | Tunings table columns misalign on accidentals | Resolved — switched to left-aligned columns |
| FEAT-001 | Tab: measure grouping with bar lines | Implemented M4 — `TabMeasure`, `measures` field, bar lines in renderer |
| FEAT-002 | Tab: beat duration | Implemented M4 — `duration` field on `TabBeat` |
| FEAT-003 | Cross-reference system: `see_also` + lick links | Phase 1 done — `see_also` frontmatter, `licks` frontmatter, "See Also" and "Practice:" footers in lesson view |
| FEAT-004 | Multiple voicings per chord | Implemented M4 — `ChordEntry` model, voicing selector in reference |
| FEAT-005 | Chord diagram: note labels and root distinction | Implemented — `dot_labels`, `root_strings` fields on `ChordSpec` |
| FEAT-006 | Tab: rest notation | Implemented — `rest: bool` on `TabBeat` renders `r` on all strings |
| FEAT-008 | Theme-aware diagram colors | Implemented — `FullNeckWidget` watches `App.dark`, switches palettes |
