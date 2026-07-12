"""Shared theme-aware Rich style palette for widgets and reference panels.

Semantic roles, not raw colors — panels ask for "maj" or "muted" and get the
right color for the active theme. Single source of truth for both the neck
widget and the reference tables.
"""

from __future__ import annotations

_DARK: dict[str, str] = {
    "heading": "bold",
    "muted":   "dim",
    # Fretboard roles (FullNeckWidget)
    "root":    "bold red",
    "tone":    "cyan",
    "bracket": "yellow",
    "char":    "bold magenta",
    # Chord quality roles
    "maj":     "green",
    "min":     "cyan",
    "dim_q":   "magenta",
    "dom":     "yellow",
    # Emphasis
    "accent":  "yellow",
    "altered": "bold yellow",
}

_LIGHT: dict[str, str] = {
    "heading": "bold",
    "muted":   "dim",
    "root":    "bold dark_red",
    "tone":    "dark_cyan",
    "bracket": "dark_goldenrod",
    "char":    "bold dark_magenta",
    "maj":     "dark_green",
    "min":     "dark_cyan",
    "dim_q":   "dark_magenta",
    "dom":     "dark_goldenrod",
    "accent":  "dark_goldenrod",
    "altered": "bold dark_goldenrod",
}


def palette(dark: bool) -> dict[str, str]:
    """Return the style palette for the active theme."""
    return _DARK if dark else _LIGHT


def quality_style(chord_name: str, pal: dict[str, str]) -> str:
    """Style for a chord name based on its quality suffix."""
    if chord_name.endswith("°"):
        return pal["dim_q"]
    if chord_name.endswith("+"):
        return pal["dom"]
    if chord_name.endswith("7") and not chord_name.endswith(("maj7", "m7")):
        return pal["dom"]
    if "m" in chord_name[1:]:
        return pal["min"]
    return pal["maj"]
