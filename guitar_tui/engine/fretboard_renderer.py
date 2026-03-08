"""Full fretboard overview renderer.

Renders a FretboardSpec into a Rich Text object.  Structure is identical to the
scale renderer (horizontal strings, fret columns) but uses FretNote highlights
instead of scale positions.

Style markers:
    ■   root
    ●   highlight (default)
    ×   muted

When show_notes=True or a FretNote.label is set, the 1-char label replaces the
style marker inside the dot position.  Multi-char label truncation is enforced
here; richer display is deferred to M4.
"""

from rich.text import Text

from guitar_tui.engine.models import FretNote, FretboardSpec

# Strings displayed top-to-bottom: string 1 (high e) → string 6 (low E)
_STRING_DISPLAY: list[tuple[int, str]] = [
    (1, "e"),
    (2, "B"),
    (3, "G"),
    (4, "D"),
    (5, "A"),
    (6, "E"),
]

_STYLE_CHARS: dict[str, str] = {
    "root":      "■",
    "highlight": "●",
    "muted":     "×",
}

_COL_EMPTY = "──┼──"


def _col(note: FretNote, show_notes: bool) -> str:
    """Return the 5-char column string for a highlighted fret note."""
    if note.label is not None:
        char = note.label[:1]
    else:
        char = _STYLE_CHARS.get(note.style, "●")
    return f"──{char}──"


def render_fretboard(spec: FretboardSpec) -> Text:
    """Render a FretboardSpec into a Rich Text object."""
    lines: list[str] = []

    if spec.title:
        lines.append(spec.title)
        lines.append("")

    lo, hi = spec.fret_range
    frets_in_range = list(range(lo, hi + 1))

    # Fret number header
    header = "  " + "".join(f"{f:^5}" for f in frets_in_range)
    lines.append(header)

    # Build note lookup: (string, fret) → FretNote
    note_map: dict[tuple[int, int], FretNote] = {
        (n.string, n.fret): n for n in spec.highlights
    }

    # One row per string (top to bottom)
    for str_num, label in _STRING_DISPLAY:
        row = f"{label} "
        for fret in frets_in_range:
            note = note_map.get((str_num, fret))
            if note is None:
                row += _COL_EMPTY
            else:
                row += _col(note, spec.show_notes)
        lines.append(row)

    if spec.caption:
        lines.append("")
        lines.append(spec.caption)

    return Text("\n".join(lines))
