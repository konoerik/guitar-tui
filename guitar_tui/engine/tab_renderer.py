"""Guitar tablature renderer.

Renders a TabSpec into a Rich Text object.  Output is a 6-line staff with
strings running top-to-bottom (e → E) and beats left-to-right.

Column width:
    max_fret_width = max digit width across all non-null notes (default 1)
    col_width      = max_fret_width + 2   (1 leading dash + number + 1 trailing dash)

Note column:   '─' + str(n).rjust(max_fret_width) + '─' + '─' * col_width * (duration - 1)
Null column:   '─' * col_width * duration

String row:    '{label} |' + columns ['|' between measures] + '|'
Beat label row (if any beat has a label):
               '   ' + label.center(col_width * duration) per beat [' ' for bar lines]

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
    measures = tab_line.get_measures()

    # One row per string, initialised with the string label prefix
    rows: list[str] = [f"{lbl} |" for _, lbl in _STRING_DISPLAY]

    has_labels = any(beat.label for m in measures for beat in m.beats)
    label_row = "   "

    for m_idx, measure in enumerate(measures):
        for beat in measure.beats:
            beat_width = col_width * beat.duration
            if beat.rest:
                rest_col = "─" + "r".rjust(max_fret_width) + "─"
                sustain = "─" * (col_width * (beat.duration - 1))
                for row_idx in range(len(rows)):
                    rows[row_idx] += rest_col + sustain
                if has_labels:
                    label_row += (beat.label or "rest").center(beat_width)
                continue
            for row_idx, (notes_idx, _) in enumerate(_STRING_DISPLAY):
                note = beat.notes[notes_idx]
                if note is not None:
                    note_col = "─" + str(note).rjust(max_fret_width) + "─"
                    sustain = "─" * (col_width * (beat.duration - 1))
                    rows[row_idx] += note_col + sustain
                else:
                    rows[row_idx] += "─" * beat_width
            if has_labels:
                label_row += (beat.label or "").center(beat_width)

        # Insert a bar line between measures (not after the last one)
        if m_idx < len(measures) - 1:
            for row_idx in range(len(rows)):
                rows[row_idx] += "|"
            if has_labels:
                label_row += " "  # keeps label row aligned with the bar character

    # Closing bar line
    for row_idx in range(len(rows)):
        rows[row_idx] += "|"

    result = rows[:]
    if has_labels:
        result.append(label_row)

    return "\n".join(result)


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

    # Compute column width from all notes across all lines (handles both formats)
    all_notes = [
        n
        for tab_line in spec.lines
        for measure in tab_line.get_measures()
        for beat in measure.beats
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
