"""Chord box diagram renderer.

Renders a ChordSpec into a Rich Text object.  The output is a vertical grid
(nut at top) with string labels, open/muted markers, fret dots, and optional
barre indicators.

Grid geometry (all rows are 25 chars wide):
    Header row:   ' E  A  D  G  B  e  '  (string labels)
    Marker row:   ' ○     ○  ○        '  (○ open, X muted, ' ' fretted)
    Nut row:      '╒══╤══╤══╤══╤══╕'    (when base_fret == 1)
    Content row:  '│● │  │  │  │  │  │'  (dots, barres, or empty)
    Separator:    '├──┼──┼──┼──┼──┤'
    Bottom row:   '└──┴──┴──┴──┴──┘'
"""

from rich.text import Text

from guitar_tui.engine.models import ChordSpec

# String labels displayed left-to-right (index 0 = low E, index 5 = high e)
_STRING_LABELS = ["E", "A", "D", "G", "B", "e"]

_NUT      = "╒═══╤═══╤═══╤═══╤═══╤═══╕"   # 6 cells, 25 chars
_SEP      = "├───┼───┼───┼───┼───┼───┤"   # 6 cells, 25 chars (5 inner ┼)
_BOTTOM   = "└───┴───┴───┴───┴───┴───┘"   # 6 cells, 25 chars
_TOP_OPEN = "┌───┬───┬───┬───┬───┬───┐"   # used when base_fret > 1 (no nut line)


def _header_row(items: list[str]) -> str:
    """Build a 25-char display row aligned with grid cells.

    Each item is 1 char (label or marker), centered in a 3-char cell.
    Border positions are at 0, 4, 8, 12, 16, 20, 24; cell centers at 2, 6,
    10, 14, 18, 22.
    """
    return " " + " ".join(f" {c} " for c in items) + " "


def _content_row(cells: list[str]) -> str:
    """Build a 25-char content row: │cell│cell│...│  (each cell is 3 chars)."""
    return "│" + "│".join(cells) + "│"


def render_chord(spec: ChordSpec) -> Text:
    """Render a ChordSpec into a Rich Text object."""
    lines: list[str] = []

    if spec.title:
        lines.append(spec.title)
        lines.append("")

    # String labels header
    lines.append(_header_row(_STRING_LABELS))

    # Above-nut markers: ○ = open, X = muted, ' ' = fretted
    markers: list[str] = []
    for fret in spec.frets:
        if fret == 0:
            markers.append("○")
        elif fret is None:
            markers.append("X")
        else:
            markers.append(" ")
    lines.append(_header_row(markers))

    # Top border: double-line nut when base_fret == 1, otherwise open border + fret label
    if spec.base_fret == 1:
        lines.append(_NUT)
    else:
        lines.append(f"{_TOP_OPEN} {spec.base_fret}fr")

    # Number of fret rows to display
    fretted_values = [f for f in spec.frets if f is not None and f > 0]
    num_rows = max(4, max(fretted_values) if fretted_values else 0)

    for row in range(1, num_rows + 1):
        cells: list[str] = []
        for i, fret in enumerate(spec.frets):
            if (
                spec.barre is not None
                and spec.barre.fret == row
                and (spec.barre.from_string - 1) <= i <= (spec.barre.to_string - 1)
            ):
                cells.append(" ▬ ")
            elif fret is not None and fret == row:
                cells.append(" ● ")
            else:
                cells.append("   ")

        lines.append(_content_row(cells))
        lines.append(_SEP if row < num_rows else _BOTTOM)

    if spec.caption:
        lines.append("")
        lines.append(spec.caption)

    return Text("\n".join(lines))
