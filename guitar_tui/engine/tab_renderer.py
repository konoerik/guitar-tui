"""Guitar tablature renderer.

Renders a TabSpec into a Rich Text object.  Output is a 6-line staff with
strings running top-to-bottom (e → E) and beats left-to-right.

Column width:
    max_fret_width = max digit width across all non-null notes (default 1)
    col_width      = max_fret_width + 2   (1 leading dash + number + 1 trailing dash)

Note column:   '─' + str(n).rjust(max_fret_width) + '─'
Null column:   '─' * col_width

String row:    '{label} |' + columns + '|'
Beat label row (if any beat has a label):
               '   ' + label.center(col_width) per beat

Multiple TabLine objects are separated by blank lines.
"""

from rich.text import Text

from guitar_tui.engine.models import TabLine, TabSpec

# Notes array indices displayed top-to-bottom (index 5 = high e, index 0 = low E)
_STRING_DISPLAY: list[tuple[int, str]] = [
    (5, "e"),
    (4, "B"),
    (3, "G"),
    (2, "D"),
    (1, "A"),
    (0, "E"),
]


def _render_tab_line(tab_line: TabLine, col_width: int, max_fret_width: int) -> str:
    """Render a single TabLine into a multi-line string."""
    rows: list[str] = []

    for idx, label in _STRING_DISPLAY:
        row = f"{label} |"
        for beat in tab_line.beats:
            note = beat.notes[idx]
            if note is not None:
                row += "─" + str(note).rjust(max_fret_width) + "─"
            else:
                row += "─" * col_width
        row += "|"
        rows.append(row)

    # Beat label row (only if at least one beat has a label)
    if any(beat.label for beat in tab_line.beats):
        label_row = "   "
        for beat in tab_line.beats:
            lbl = beat.label or ""
            label_row += lbl.center(col_width)
        rows.append(label_row)

    return "\n".join(rows)


def render_tab(spec: TabSpec) -> Text:
    """Render a TabSpec into a Rich Text object."""
    parts: list[str] = []

    # Title + optional tempo/time info
    if spec.title:
        extras: list[str] = []
        if spec.tempo is not None:
            extras.append(f"{spec.tempo} BPM")
        if spec.time is not None:
            extras.append(spec.time)
        header = spec.title
        if extras:
            header = f"{spec.title}  ({', '.join(extras)})"
        parts.append(header)
        parts.append("")

    # Compute column width from all notes across all lines
    all_notes = [
        n
        for tab_line in spec.lines
        for beat in tab_line.beats
        for n in beat.notes
        if n is not None
    ]
    max_fret_width = max((len(str(n)) for n in all_notes), default=1)
    col_width = max_fret_width + 2

    # Render each TabLine block; separate multiple blocks with a blank line
    blocks = [
        _render_tab_line(tab_line, col_width, max_fret_width)
        for tab_line in spec.lines
    ]
    parts.append("\n\n".join(blocks))

    if spec.caption:
        parts.append("")
        parts.append(spec.caption)

    return Text("\n".join(parts))
