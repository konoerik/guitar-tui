"""Tests for the guitar tablature renderer (M2)."""

from guitar_tui.engine.models import TabSpec
from guitar_tui.engine.tab_renderer import render_tab


# ── helpers ───────────────────────────────────────────────────────────────────


def em_arpeggio_spec() -> TabSpec:
    """E minor arpeggio — 4 beats, sparse notes, labels 1-4."""
    return TabSpec.model_validate({
        "type": "tab",
        "title": "E Minor Arpeggio",
        "tempo": 80,
        "time": "4/4",
        "lines": [
            {
                "beats": [
                    {"notes": [0, 2, 2, 0, 0, 0], "label": "1"},
                    {"notes": [None, None, None, None, 0, None], "label": "2"},
                    {"notes": [None, None, None, 0, None, None], "label": "3"},
                    {"notes": [None, None, 0, None, None, None], "label": "4"},
                ]
            }
        ],
    })


# ── E minor arpeggio ───────────────────────────────────────────────────────────


class TestEmArpeggio:
    spec = em_arpeggio_spec()

    def test_title_in_output(self) -> None:
        text = render_tab(self.spec)
        assert "E Minor Arpeggio" in text.plain

    def test_tempo_in_output(self) -> None:
        text = render_tab(self.spec)
        assert "80 BPM" in text.plain

    def test_time_signature_in_output(self) -> None:
        text = render_tab(self.spec)
        assert "4/4" in text.plain

    def test_six_string_rows(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        assert len(string_rows) == 6

    def test_string_order_top_to_bottom(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        labels = [r[0] for r in string_rows]
        assert labels == ["e", "B", "G", "D", "A", "E"]

    def test_beat_labels_present(self) -> None:
        text = render_tab(self.spec)
        assert "1" in text.plain
        assert "4" in text.plain

    def test_fret_numbers_appear_in_rows(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        # e row: beat1 has fret 0 for index 5
        e_row = string_rows[0]  # top row = e string
        assert "0" in e_row

    def test_null_beats_render_as_dashes(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        # e row has only beat1 with fret 0; beats 2-4 are null → dashes
        e_row = string_rows[0]
        # After the fret number the rest should be dashes
        assert "─" in e_row

    def test_e_string_has_fret_0_in_beat1(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        E_row = string_rows[5]  # bottom row = E string
        assert "0" in E_row

    def test_rows_start_with_bar(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        for row in string_rows:
            assert row.endswith("|"), f"Row does not end with |: {row!r}"

    def test_all_string_rows_same_width(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        widths = {len(r) for r in string_rows}
        assert len(widths) == 1, f"Inconsistent row widths: {widths}"


# ── Multi-line tab ─────────────────────────────────────────────────────────────


class TestMultiLinetab:
    spec = TabSpec.model_validate({
        "type": "tab",
        "title": "Two Measures",
        "lines": [
            {
                "beats": [
                    {"notes": [0, 0, 0, 0, 0, 0]},
                    {"notes": [None, None, None, None, None, None]},
                ]
            },
            {
                "beats": [
                    {"notes": [2, 2, 2, 2, 2, 2]},
                    {"notes": [None, None, None, None, None, None]},
                ]
            },
        ],
    })

    def test_blank_line_between_tab_lines(self) -> None:
        text = render_tab(self.spec)
        plain = text.plain
        # Two blocks of 6 string rows separated by a blank line
        assert "\n\n" in plain

    def test_both_lines_rendered(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        # 2 lines × 6 strings = 12 string rows
        assert len(string_rows) == 12


# ── All strings playing ────────────────────────────────────────────────────────


class TestAllStringsPlaying:
    """All 6 strings have notes in every beat."""

    spec = TabSpec.model_validate({
        "type": "tab",
        "lines": [
            {
                "beats": [
                    {"notes": [0, 2, 2, 0, 1, 0]},
                    {"notes": [0, 0, 0, 0, 0, 0]},
                ]
            }
        ],
    })

    def test_all_rows_contain_fret_numbers(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        for row in string_rows:
            # Each row should contain at least one digit
            assert any(c.isdigit() for c in row), f"No digit in row: {row!r}"


# ── High fret numbers (2-digit) ────────────────────────────────────────────────


class TestHighFretNumbers:
    spec = TabSpec.model_validate({
        "type": "tab",
        "lines": [
            {
                "beats": [
                    {"notes": [12, None, None, None, None, None]},
                    {"notes": [None, None, None, None, None, 0]},
                ]
            }
        ],
    })

    def test_two_digit_fret_rendered(self) -> None:
        text = render_tab(self.spec)
        assert "12" in text.plain

    def test_col_width_accommodates_two_digit_fret(self) -> None:
        text = render_tab(self.spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        # All rows must have equal width
        widths = {len(r) for r in string_rows}
        assert len(widths) == 1
