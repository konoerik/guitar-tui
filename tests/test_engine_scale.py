"""Tests for the scale position renderer (M2)."""

import pytest
from pydantic import ValidationError

from guitar_tui.engine.models import ScaleSpec
from guitar_tui.engine.scale_renderer import render_scale


# ── helpers ───────────────────────────────────────────────────────────────────


def a_minor_pentatonic_pos1() -> ScaleSpec:
    """A minor pentatonic position 1, fret range 5–8 (12 notes)."""
    return ScaleSpec.model_validate({
        "type": "scale",
        "title": "A Minor Pentatonic — Position 1",
        "root": "A",
        "fret_range": [5, 8],
        "positions": [
            {"string": 6, "fret": 5, "degree": "1", "root": True},
            {"string": 6, "fret": 8, "degree": "b3"},
            {"string": 5, "fret": 5, "degree": "4"},
            {"string": 5, "fret": 7, "degree": "5"},
            {"string": 4, "fret": 5, "degree": "b7"},
            {"string": 4, "fret": 7, "degree": "1", "root": True},
            {"string": 3, "fret": 5, "degree": "b3"},
            {"string": 3, "fret": 7, "degree": "4"},
            {"string": 2, "fret": 5, "degree": "5"},
            {"string": 2, "fret": 8, "degree": "b7"},
            {"string": 1, "fret": 5, "degree": "1", "root": True},
            {"string": 1, "fret": 8, "degree": "b3"},
        ],
    })


# ── A minor pentatonic position 1 ─────────────────────────────────────────────


class TestAMinorPentatonicPos1:
    spec = a_minor_pentatonic_pos1()

    def test_title_in_output(self) -> None:
        text = render_scale(self.spec)
        assert "A Minor Pentatonic" in text.plain

    def test_fret_numbers_in_header(self) -> None:
        text = render_scale(self.spec)
        lines = text.plain.splitlines()
        header = lines[2]  # title, blank, header
        for fret in ("5", "6", "7", "8"):
            assert fret in header

    def test_six_string_rows_present(self) -> None:
        text = render_scale(self.spec)
        lines = text.plain.splitlines()
        # String rows start with "{label} " and contain "──" (grid dashes)
        string_rows = [l for l in lines if len(l) >= 2 and l[0] in "eBGDAE" and l[1] == " " and "──" in l]
        # Each of the 6 string labels starts a row
        assert len(string_rows) == 6

    def test_string_order_top_to_bottom(self) -> None:
        text = render_scale(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if len(l) >= 2 and l[0] in "eBGDAE" and l[1] == " " and "──" in l]
        labels = [r[0] for r in string_rows]
        assert labels == ["e", "B", "G", "D", "A", "E"]

    def test_root_marker_used_for_roots(self) -> None:
        # Roots at string 6 fret 5, string 4 fret 7, string 1 fret 5
        text = render_scale(self.spec)
        assert "■" in text.plain

    def test_non_root_marker_used(self) -> None:
        text = render_scale(self.spec)
        assert "●" in text.plain

    def test_empty_frets_use_grid_marker(self) -> None:
        text = render_scale(self.spec)
        assert "┼" in text.plain

    def test_e_string_has_root_at_fret5(self) -> None:
        # E string (string 6) has root at fret 5 → ■ in E row at col for fret 5
        text = render_scale(self.spec)
        lines = text.plain.splitlines()
        e_row = next(l for l in lines if l.startswith("E "))
        # The first note column (fret 5) should be ──■──
        assert "──■──" in e_row

    def test_e_string_non_root_at_fret8(self) -> None:
        text = render_scale(self.spec)
        lines = text.plain.splitlines()
        e_row = next(l for l in lines if l.startswith("E "))
        assert "──●──" in e_row

    def test_column_width_consistent(self) -> None:
        text = render_scale(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if len(l) >= 2 and l[0] in "eBGDAE" and l[1] == " " and "──" in l]
        widths = {len(r) for r in string_rows}
        assert len(widths) == 1, f"Inconsistent row widths: {widths}"

    def test_header_width_matches_string_rows(self) -> None:
        text = render_scale(self.spec)
        lines = text.plain.splitlines()
        header = lines[2]
        string_rows = [l for l in lines if len(l) >= 2 and l[0] in "eBGDAE" and l[1] == " " and "──" in l]
        assert len(header) == len(string_rows[0])


# ── Auto fret_range computation ────────────────────────────────────────────────


class TestFretRangeAutoComputed:
    def test_fret_range_derived_from_positions(self) -> None:
        spec = ScaleSpec.model_validate({
            "type": "scale",
            "root": "C",
            "positions": [
                {"string": 6, "fret": 3},
                {"string": 5, "fret": 5},
            ],
        })
        text = render_scale(spec)
        lines = text.plain.splitlines()
        header = lines[0]  # no title, so header is first line
        assert "3" in header
        assert "5" in header

    def test_all_frets_between_min_and_max_shown(self) -> None:
        spec = ScaleSpec.model_validate({
            "type": "scale",
            "root": "C",
            "positions": [
                {"string": 6, "fret": 2},
                {"string": 5, "fret": 4},
            ],
        })
        text = render_scale(spec)
        header = text.plain.splitlines()[0]
        # Frets 2, 3, 4 should all appear in header
        for fret in ("2", "3", "4"):
            assert fret in header


# ── highlight_root=False ───────────────────────────────────────────────────────


class TestHighlightRootDisabled:
    def test_no_root_marker_when_disabled(self) -> None:
        spec = ScaleSpec.model_validate({
            "type": "scale",
            "root": "A",
            "highlight_root": False,
            "positions": [
                {"string": 6, "fret": 5, "root": True},
                {"string": 6, "fret": 7},
            ],
        })
        text = render_scale(spec)
        assert "■" not in text.plain
        assert "●" in text.plain
