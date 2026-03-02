"""Tests for the full fretboard renderer (M2)."""

from guitar_tui.engine.fretboard_renderer import render_fretboard
from guitar_tui.engine.models import FretboardSpec


# ── helpers ───────────────────────────────────────────────────────────────────


def natural_notes_low_e() -> FretboardSpec:
    """Natural notes on the low E string, fret range 0–12."""
    return FretboardSpec.model_validate({
        "type": "fretboard",
        "title": "Natural Notes — Low E String",
        "fret_range": [0, 12],
        "show_notes": True,
        "highlights": [
            {"string": 6, "fret": 0,  "label": "E", "style": "root"},
            {"string": 6, "fret": 2,  "label": "F#"},
            {"string": 6, "fret": 3,  "label": "G"},
            {"string": 6, "fret": 5,  "label": "A"},
            {"string": 6, "fret": 7,  "label": "B"},
            {"string": 6, "fret": 8,  "label": "C"},
            {"string": 6, "fret": 10, "label": "D"},
            {"string": 6, "fret": 12, "label": "E", "style": "root"},
        ],
    })


# ── Natural notes on low E ────────────────────────────────────────────────────


class TestNaturalNotesLowE:
    spec = natural_notes_low_e()

    def test_title_in_output(self) -> None:
        text = render_fretboard(self.spec)
        assert "Natural Notes" in text.plain

    def test_fret_range_0_to_12_in_header(self) -> None:
        text = render_fretboard(self.spec)
        lines = text.plain.splitlines()
        header = lines[2]  # title, blank, header
        assert "0" in header
        assert "12" in header

    def test_six_string_rows(self) -> None:
        text = render_fretboard(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if l and l[0] in "eBGDAE"]
        assert len(string_rows) == 6

    def test_string_order_top_to_bottom(self) -> None:
        text = render_fretboard(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if l and l[0] in "eBGDAE"]
        labels = [r[0] for r in string_rows]
        assert labels == ["e", "B", "G", "D", "A", "E"]

    def test_label_chars_appear_in_e_string_row(self) -> None:
        text = render_fretboard(self.spec)
        lines = text.plain.splitlines()
        e_row = next(l for l in lines if l.startswith("E "))
        # E, F, G, A, B, C, D labels (first chars) should appear
        for char in ("E", "F", "G", "A", "B", "C", "D"):
            assert char in e_row, f"Expected '{char}' in E string row"

    def test_empty_strings_use_grid_marker(self) -> None:
        # All strings other than low E have no highlights → grid markers
        text = render_fretboard(self.spec)
        assert "┼" in text.plain


# ── show_notes flag ────────────────────────────────────────────────────────────


class TestShowNotes:
    def test_label_shown_when_show_notes_false_but_label_set(self) -> None:
        # A FretNote with an explicit label is always shown regardless of show_notes
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "show_notes": False,
            "highlights": [
                {"string": 6, "fret": 5, "label": "A"},
            ],
        })
        text = render_fretboard(spec)
        lines = text.plain.splitlines()
        e_row = next(l for l in lines if l.startswith("E "))
        assert "A" in e_row

    def test_style_marker_used_when_no_label(self) -> None:
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "show_notes": False,
            "highlights": [
                {"string": 6, "fret": 5, "style": "highlight"},
            ],
        })
        text = render_fretboard(spec)
        assert "●" in text.plain

    def test_label_truncated_to_one_char(self) -> None:
        # Multi-char label → only first char shown in M2
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "highlights": [
                {"string": 6, "fret": 5, "label": "Ab"},
            ],
        })
        text = render_fretboard(spec)
        lines = text.plain.splitlines()
        e_row = next(l for l in lines if l.startswith("E "))
        # "A" should appear but not "Ab" as a substring of the column
        assert "──A──" in e_row


# ── Style markers ──────────────────────────────────────────────────────────────


class TestStyleMarkers:
    def test_root_style_shows_square(self) -> None:
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "highlights": [{"string": 6, "fret": 5, "style": "root"}],
        })
        text = render_fretboard(spec)
        assert "■" in text.plain

    def test_muted_style_shows_cross(self) -> None:
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "highlights": [{"string": 6, "fret": 5, "style": "muted"}],
        })
        text = render_fretboard(spec)
        assert "×" in text.plain

    def test_highlight_style_shows_dot(self) -> None:
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "highlights": [{"string": 6, "fret": 5, "style": "highlight"}],
        })
        text = render_fretboard(spec)
        assert "●" in text.plain

    def test_default_style_is_highlight(self) -> None:
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "highlights": [{"string": 6, "fret": 5}],  # no style field
        })
        text = render_fretboard(spec)
        assert "●" in text.plain

    def test_root_and_highlight_coexist(self) -> None:
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "highlights": [
                {"string": 6, "fret": 5, "style": "root"},
                {"string": 5, "fret": 7, "style": "highlight"},
            ],
        })
        text = render_fretboard(spec)
        assert "■" in text.plain
        assert "●" in text.plain


# ── Default fret range ─────────────────────────────────────────────────────────


class TestDefaultFretRange:
    def test_default_range_is_0_to_12(self) -> None:
        spec = FretboardSpec.model_validate({
            "type": "fretboard",
            "highlights": [],
        })
        text = render_fretboard(spec)
        header = text.plain.splitlines()[0]
        assert "0" in header
        assert "12" in header
