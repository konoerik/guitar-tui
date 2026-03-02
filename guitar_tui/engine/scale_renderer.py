"""Scale position diagram renderer.

Renders a ScaleSpec into a Rich Text object.  Output is a horizontal fretboard
slice with strings running top-to-bottom (e → E) and frets left-to-right.

Column format (5 chars each):
    ──●──   note present (non-root)
    ──■──   root note (when highlight_root=True)
    ──┼──   empty fret position

Row format:
    fret header:  '  ' + 5-char fret number per column
    string row:   '{label} ' + 5-char column per fret
"""

from rich.text import Text

from guitar_tui.engine.models import ScaleNote, ScaleSpec

# Strings displayed top-to-bottom: string 1 (high e) → string 6 (low E)
_STRING_DISPLAY: list[tuple[int, str]] = [
    (1, "e"),
    (2, "B"),
    (3, "G"),
    (4, "D"),
    (5, "A"),
    (6, "E"),
]

_COL_NOTE  = "──●──"
_COL_ROOT  = "──■──"
_COL_EMPTY = "──┼──"


def render_scale(spec: ScaleSpec) -> Text:
    """Render a ScaleSpec into a Rich Text object."""
    lines: list[str] = []

    if spec.title:
        lines.append(spec.title)
        lines.append("")

    # Determine fret range
    if spec.fret_range is not None:
        lo, hi = spec.fret_range
    else:
        frets = [p.fret for p in spec.positions]
        lo, hi = min(frets), max(frets)

    frets_in_range = list(range(lo, hi + 1))

    # Fret number header: '  ' prefix + 5-char per fret
    header = "  " + "".join(f"{f:^5}" for f in frets_in_range)
    lines.append(header)

    # Build note lookup: (string, fret) → ScaleNote
    note_map: dict[tuple[int, int], ScaleNote] = {
        (n.string, n.fret): n for n in spec.positions
    }

    # One row per string (top to bottom)
    for str_num, label in _STRING_DISPLAY:
        row = f"{label} "
        for fret in frets_in_range:
            note = note_map.get((str_num, fret))
            if note is None:
                row += _COL_EMPTY
            elif note.root and spec.highlight_root:
                row += _COL_ROOT
            else:
                row += _COL_NOTE
        lines.append(row)

    if spec.caption:
        lines.append("")
        lines.append(spec.caption)

    return Text("\n".join(lines))
