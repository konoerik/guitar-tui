"""Diagram rendering engine — music-agnostic, pure rendering logic."""

from guitar_tui.engine.dispatcher import dispatch
from guitar_tui.engine.models import (
    ChordSpec,
    DiagramSpec,
    FretboardSpec,
    ScaleSpec,
    TabSpec,
)

__all__ = [
    "dispatch",
    "ChordSpec",
    "DiagramSpec",
    "FretboardSpec",
    "ScaleSpec",
    "TabSpec",
]
