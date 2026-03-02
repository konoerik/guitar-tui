# Diagram Taxonomy

**Source**: Session 1 architecture discussion
**Purpose**: Complete catalog of diagram types identified during planning. Used to guide M2 (engine) and M5 (interactive) implementation scope. Not all types are in scope for M2 — see priority column.

---

## Rendering Primitives

Three independent rendering primitives cover the full taxonomy:

1. **Chord box grid** — vertical grid, nut at top (Groups A)
2. **Fretboard map** — horizontal strings, vertical frets (Groups B, F)
3. **Tab staff** — 6-line staff with fret numbers (Groups C, D)

Groups E are plain Rich tables/styled text — no diagram engine needed.

---

## Group A — Chord Box Diagrams

| ID | Name | Description | M2 scope |
|----|------|-------------|----------|
| A1 | Standard Chord Box | Inverted grid, X/O open/mute indicators, finger numbers, fret position marker | **Yes** |
| A2 | Barre Chord Box | A1 + horizontal barre bar spanning multiple strings | **Yes** (part of A1 via `barre` field) |
| A3 | Multi-Position Chord Strip | Same chord in 2–4 positions shown side by side (CAGED-style) | M4–M5 |

**A1 + A2** are unified in DiagramSpec as `type: chord` with optional `barre` object. A3 is a layout concern (multiple chord diagrams in a row), not a new primitive.

---

## Group B — Fretboard Maps

| ID | Name | Description | M2 scope |
|----|------|-------------|----------|
| B1 | Scale Position Window | Horizontal 4–6 fret slice, highlighted scale tones with degree labels | **Yes** (`type: scale`) |
| B2 | Full Fretboard Map | All 6 strings, frets 0–12+, note names or scale degrees | **Yes** (`type: fretboard`) |
| B3 | Interval Map | Labels intervals relative to root (R, b3, 5…) instead of note names | Yes — variant of B1/B2 via `degree` field on ScaleNote |
| B4 | CAGED Overlay | All 5 CAGED shapes marked simultaneously, distinct visual styles | M5 |
| B5 | Chord Tone Map | Highlights only chord tones across full neck | M5 |

**B1 and B2** are in DiagramSpec as `type: scale` and `type: fretboard`. B3 is already supported via the `degree` field. B4 and B5 require multi-layer highlighting — deferred to M5.

---

## Group C — Tablature Diagrams

| ID | Name | Description | M2 scope |
|----|------|-------------|----------|
| C1 | Standard Tab | 6-line staff with fret numbers, low E at bottom | **Yes** (`type: tab`) |
| C2 | Technique-Annotated Tab | Adds bend `b`, hammer-on `h`, pull-off `p`, slide `/` notation | M3–M4 (content-driven) |
| C3 | Scale Run in Tab | Scale pattern played linearly as tab | Yes — data, not a new renderer |
| C4 | Arpeggio Tab | Chord tones picked in pattern | Yes — data, not a new renderer |

**C1** is the tab renderer. C2 requires technique annotation fields on TabBeat — simple extension when needed. C3 and C4 are authoring patterns, not new diagram types.

---

## Group D — Chord Progression Diagrams

| ID | Name | Description | M2 scope |
|----|------|-------------|----------|
| D1 | Chord Progression Tab | Multiple chords in sequence within tab staff | M3–M4 |
| D2 | Roman Numeral Progression | Harmonic function display (I–IV–V), theory-focused | M4 (Rich table) |
| D3 | Strumming Pattern | Beat grid with up/down strum arrows | M4–M5 |
| D4 | Fingerpicking Pattern | Which finger plucks which string per beat | M5 |

None of these require new rendering primitives — D1 extends tab, D2/D3/D4 are Rich-based layouts.

---

## Group E — Reference Displays (no diagram engine)

| ID | Name | Description | Implementation |
|----|------|-------------|----------------|
| E1 | Capo Transposition Table | DataTable: capo position → key equivalents | Rich `Table` |
| E2 | Chord Formula Display | Interval structure: R–3–5, R–b3–5, etc. | Rich styled text |
| E3 | Single String Note Map | Chromatic note sequence on one string | Rich styled text or B2 slice |

These are pure Rich text/table — the content loader or TUI layer handles them directly.

---

## Group F — Interactive Diagrams

| ID | Name | Description | Milestone |
|----|------|-------------|-----------|
| F1 | Rolling Fretboard Window | Scrollable position window — same shape at different fret positions | M5 |
| F2 | Interactive Full Fretboard | Cursor-driven: shows note name, interval, chord membership at cursor position | M5 |

**Key insight from session 1**: F1 is nearly free once B1 (scale position window) is implemented — it's the same renderer with a position offset. F2 is the only genuinely high-complexity component.

---

## M2 Engine Scope Summary

Implement these four renderers in M2:

| DiagramSpec type | Covers |
|-----------------|--------|
| `chord`         | A1, A2 |
| `scale`         | B1, B3 |
| `fretboard`     | B2, B3, E3 |
| `tab`           | C1, C3, C4 |

Everything else builds on these primitives or is a Rich layout — no new rendering math required.
