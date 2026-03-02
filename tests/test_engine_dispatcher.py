"""Tests for the diagram dispatcher (M2)."""

import pytest
from pydantic import ValidationError
from rich.text import Text

from guitar_tui.engine.dispatcher import dispatch
from guitar_tui.engine.models import ChordSpec, FretboardSpec, ScaleSpec, TabSpec


# ── helpers ───────────────────────────────────────────────────────────────────


VALID_CHORD = {
    "type": "chord",
    "frets": [3, 2, 0, 0, 0, 3],
}

VALID_SCALE = {
    "type": "scale",
    "root": "A",
    "positions": [
        {"string": 6, "fret": 5, "root": True},
        {"string": 6, "fret": 7},
    ],
}

VALID_TAB = {
    "type": "tab",
    "lines": [
        {"beats": [{"notes": [0, 0, 0, 0, 0, 0]}]}
    ],
}

VALID_FRETBOARD = {
    "type": "fretboard",
    "highlights": [{"string": 6, "fret": 5, "style": "root"}],
}


# ── Routing ───────────────────────────────────────────────────────────────────


class TestRouting:
    def test_chord_returns_text(self) -> None:
        result = dispatch(VALID_CHORD)
        assert isinstance(result, Text)

    def test_scale_returns_text(self) -> None:
        result = dispatch(VALID_SCALE)
        assert isinstance(result, Text)

    def test_tab_returns_text(self) -> None:
        result = dispatch(VALID_TAB)
        assert isinstance(result, Text)

    def test_fretboard_returns_text(self) -> None:
        result = dispatch(VALID_FRETBOARD)
        assert isinstance(result, Text)

    def test_chord_output_has_grid_chars(self) -> None:
        result = dispatch(VALID_CHORD)
        assert "│" in result.plain

    def test_scale_output_has_string_rows(self) -> None:
        result = dispatch(VALID_SCALE)
        lines = result.plain.splitlines()
        string_rows = [l for l in lines if l and l[0] in "eBGDAE"]
        assert len(string_rows) == 6

    def test_tab_output_has_bar_chars(self) -> None:
        result = dispatch(VALID_TAB)
        assert "|" in result.plain

    def test_fretboard_output_has_string_rows(self) -> None:
        result = dispatch(VALID_FRETBOARD)
        lines = result.plain.splitlines()
        string_rows = [l for l in lines if l and l[0] in "eBGDAE"]
        assert len(string_rows) == 6


# ── Validation errors ──────────────────────────────────────────────────────────


class TestValidationErrors:
    def test_unknown_type_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({"type": "unknown", "frets": [0, 0, 0, 0, 0, 0]})

    def test_missing_type_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({"frets": [0, 0, 0, 0, 0, 0]})

    def test_chord_missing_frets_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({"type": "chord"})

    def test_chord_wrong_fret_count_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({"type": "chord", "frets": [0, 1, 2]})

    def test_scale_missing_root_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({"type": "scale", "positions": []})

    def test_tab_missing_lines_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({"type": "tab"})

    def test_fretboard_missing_highlights_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({"type": "fretboard"})

    def test_empty_dict_raises(self) -> None:
        with pytest.raises(ValidationError):
            dispatch({})

    def test_validation_error_not_wrapped(self) -> None:
        """Dispatcher must not swallow or re-wrap ValidationError."""
        with pytest.raises(ValidationError):
            dispatch({"type": "chord", "frets": "not-a-list"})


# ── Barre alias compatibility ──────────────────────────────────────────────────


class TestBarreAlias:
    def test_barre_with_from_to_aliases_parsed(self) -> None:
        """'from' and 'to' are Python keywords; aliases must work in dicts."""
        data = {
            "type": "chord",
            "frets": [1, 1, 2, 3, 3, 1],
            "barre": {"fret": 1, "from": 1, "to": 6},
        }
        result = dispatch(data)
        # Barre row (row 1) should contain ▬
        assert "▬" in result.plain
