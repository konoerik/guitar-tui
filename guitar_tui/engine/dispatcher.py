"""Diagram dispatcher — validates a raw dict and routes to the correct renderer.

Usage::

    from guitar_tui.engine import dispatch

    text = dispatch({"type": "chord", "frets": [3, 2, 0, 0, 0, 3]})
    print(text.plain)

Raises ``pydantic.ValidationError`` for invalid or unknown diagram types.
The content layer (M3) is responsible for deciding how to surface that error.
"""

from pydantic import TypeAdapter
from rich.text import Text

from guitar_tui.engine.chord_renderer import render_chord
from guitar_tui.engine.fretboard_renderer import render_fretboard
from guitar_tui.engine.models import (
    ChordSpec,
    DiagramSpec,
    FretboardSpec,
    ScaleSpec,
    TabSpec,
)
from guitar_tui.engine.scale_renderer import render_scale
from guitar_tui.engine.tab_renderer import render_tab

_adapter: TypeAdapter[DiagramSpec] = TypeAdapter(DiagramSpec)


def dispatch(data: dict) -> Text:
    """Validate *data* against DiagramSpec and render it to a Rich Text.

    Parameters
    ----------
    data:
        Raw dict (e.g. parsed from a lesson YAML block).

    Returns
    -------
    rich.text.Text
        Rendered diagram as unstyled text (styling added in M4).

    Raises
    ------
    pydantic.ValidationError
        If *data* does not conform to any known DiagramSpec type.
    """
    spec = _adapter.validate_python(data)
    match spec:
        case ChordSpec():
            return render_chord(spec)
        case ScaleSpec():
            return render_scale(spec)
        case TabSpec():
            return render_tab(spec)
        case FretboardSpec():
            return render_fretboard(spec)
