"""Guitar tablature renderer.

Renders a TabSpec into a Rich Text object.  Output is a 6-line staff with
strings running top-to-bottom (e → E) and beats left-to-right.

Column width is computed **per beat** so that plain fret columns stay compact
while bend/vibrato/technique columns expand only as much as their content requires.

Per-beat widths:
    fret_width     = max digit count of any non-null fret in the beat (default 1)
    note_str_width = max len(_build_note_str) for any non-null note in the beat
    col_width      = note_str_width + 2   (1 leading char + note str + 1 trailing dash)

Note column:   leading + note_str.ljust(note_str_width) + '─' + '─' * col_width * (duration - 1)
               leading = beat.technique if set, else '─'
Null column:   '─' * col_width * duration

String row:    '{label} |' + columns ['|' between measures] + '|'

Beat label rows (if any beat has a label):
    Labels are placed using collision detection into two rows (row A and row B).
    Each label is left-aligned starting at position 1 within its beat column
    (directly under the fret digit, after the leading technique/dash character).
    Row A is tried first; if the new label would overlap the previous row-A label,
    it goes to row B.  Only rows that contain at least one label are appended.
    Label text is written at absolute character positions into pre-allocated
    character arrays — no per-slot padding math, labels may visually extend past
    their beat boundary without affecting row widths.

Multiple TabLine objects are separated by blank lines.
"""

from rich.text import Text

from guitar_tui.engine.models import TabBeat, TabLine, TabSpec

# Notes array indices displayed top-to-bottom (index 5 = high e, index 0 = low E)
_STRING_DISPLAY: list[tuple[int, str]] = [
    (5, "e"),
    (4, "B"),
    (3, "G"),
    (2, "D"),
    (1, "A"),
    (0, "E"),
]

_PREFIX_LEN = 3  # len("x |")


def _build_note_str(note: int, beat: TabBeat) -> str:
    """Build the fret string for a note, including bend/vibrato suffixes."""
    s = str(note)
    if beat.bend:
        s += f"b{beat.bend_target}" if beat.bend_target is not None else "b"
    if beat.vibrato:
        s += "~"
    return s


def _beat_widths(beat: TabBeat) -> tuple[int, int, int]:
    """Return (col_width, note_str_width, fret_width) for a single beat.

    col_width      = note_str_width + 2
    note_str_width = max len(_build_note_str) across all non-null notes (default 1)
    fret_width     = max digit count across all non-null fret numbers (default 1)
    """
    if beat.rest:
        return (3, 1, 1)  # 'r' is 1 char
    active = [n for n in beat.notes if n is not None]
    if not active:
        return (3, 1, 1)
    fw = max(len(str(n)) for n in active)
    nsw = max(len(_build_note_str(n, beat)) for n in active)
    return (nsw + 2, nsw, fw)


def _render_tab_line(tab_line: TabLine) -> str:
    """Render a single TabLine into a multi-line string."""
    measures = tab_line.get_measures()

    # One row per string, initialised with the string label prefix
    rows: list[str] = [f"{lbl} |" for _, lbl in _STRING_DISPLAY]

    has_labels = any(beat.label for m in measures for beat in m.beats)

    # Pre-pass: compute content_offset and beat_width for each beat.
    # content_offset is 0-based from the start of the content area (after "x |" prefix).
    flat_beats: list[TabBeat] = []
    beat_offsets: list[int] = []
    beat_widths_cache: list[int] = []
    content_pos = 0
    for m_idx, measure in enumerate(measures):
        for beat in measure.beats:
            flat_beats.append(beat)
            beat_offsets.append(content_pos)
            col_width, _, _ = _beat_widths(beat)
            bw = col_width * beat.duration
            beat_widths_cache.append(bw)
            content_pos += bw
        if m_idx < len(measures) - 1:
            content_pos += 1  # inter-measure bar line "|"
    total_row_width = _PREFIX_LEN + content_pos + 1  # +1 for closing bar line "|"

    # Build label rows using collision-detection placement.
    # Each label is written at absolute position (PREFIX_LEN + content_offset + 1),
    # i.e. one position after the beat's leading dash/technique char = under the fret digit.
    if has_labels:
        label_a: list[str] = [" "] * total_row_width
        label_b: list[str] = [" "] * total_row_width
        row_a_end = -1  # rightmost position occupied on row A
        row_b_end = -1  # rightmost position occupied on row B

        for beat, b_offset, b_width in zip(flat_beats, beat_offsets, beat_widths_cache):
            if not beat.label:
                continue
            label = beat.label
            label_start = _PREFIX_LEN + b_offset + 1
            label_end = label_start + len(label) - 1

            if label_start > row_a_end:
                target: list[str] = label_a
                row_a_end = label_end
            elif label_start > row_b_end:
                target = label_b
                row_b_end = label_end
            else:
                # Both rows occupied at this position — use the row ending sooner
                if row_a_end <= row_b_end:
                    target = label_a
                    row_a_end = label_end
                else:
                    target = label_b
                    row_b_end = label_end

            for i, ch in enumerate(label):
                pos = label_start + i
                if pos < total_row_width:
                    target[pos] = ch

    # Main render loop
    for m_idx, measure in enumerate(measures):
        for beat in measure.beats:
            col_width, note_str_width, _ = _beat_widths(beat)
            beat_width = col_width * beat.duration

            if beat.rest:
                rest_col = "─" + "r".ljust(note_str_width) + "─"
                sustain = "─" * (col_width * (beat.duration - 1))
                for row_idx in range(len(rows)):
                    rows[row_idx] += rest_col + sustain
                continue

            leading = beat.technique or "─"
            for row_idx, (notes_idx, _) in enumerate(_STRING_DISPLAY):
                note = beat.notes[notes_idx]
                if note is not None:
                    note_str = _build_note_str(note, beat)
                    note_col = leading + note_str.ljust(note_str_width) + "─"
                    sustain = "─" * (col_width * (beat.duration - 1))
                    rows[row_idx] += note_col + sustain
                else:
                    rows[row_idx] += "─" * beat_width

        if m_idx < len(measures) - 1:
            for row_idx in range(len(rows)):
                rows[row_idx] += "|"

    # Closing bar line
    for row_idx in range(len(rows)):
        rows[row_idx] += "|"

    result = rows[:]
    if has_labels:
        label_a_str = "".join(label_a)
        label_b_str = "".join(label_b)
        if any(c != " " for c in label_a_str):
            result.append(label_a_str)
        if any(c != " " for c in label_b_str):
            result.append(label_b_str)

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

    # Column widths are computed per beat inside _render_tab_line so each beat
    # is only as wide as its own content requires (plain fret columns stay compact).
    blocks = [_render_tab_line(tab_line) for tab_line in spec.lines]
    parts.append("\n\n".join(blocks))

    if spec.caption:
        parts.append("")
        parts.append(spec.caption)

    return Text("\n".join(parts))
