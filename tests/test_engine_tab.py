"""Tests for the guitar tablature renderer (M2)."""

import pytest
from pydantic import ValidationError

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

    def test_single_digit_fret_label_alignment_in_two_digit_context(self) -> None:
        """Single-digit frets in a two-digit tab must align with their labels.

        When max_fret_width=2, a single-digit fret (e.g. 7) must be left-justified
        so the digit sits at column position 1 — the same position that center()
        places a one-char label. rjust would push it to position 2, causing a
        one-character misalignment between the fret and its label.
        """
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [
                {
                    "beats": [
                        {"notes": [None, None, None, None, None, 7], "label": "E"},
                        {"notes": [None, None, None, None, None, 10], "label": "D"},
                    ]
                }
            ],
        })
        text = render_tab(spec)
        lines = text.plain.splitlines()
        # Label row is the last line (no | delimiters)
        label_row = lines[-1]
        string_rows = [l for l in lines if "|" in l]
        e_row = string_rows[0]  # high e string, top row

        # Find position of "7" in the e string row
        fret_pos = e_row.index("7")
        # Find position of "E" in the label row — must equal fret_pos
        label_pos = label_row.index("E")
        assert fret_pos == label_pos, (
            f"Fret '7' at col {fret_pos} but label 'E' at col {label_pos}; "
            f"e_row={e_row!r}, label_row={label_row!r}"
        )


# ── TabLine validation (FEAT-001) ─────────────────────────────────────────────


class TestTabLineValidation:
    def test_beats_only_valid(self) -> None:
        TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [0] * 6}]}],
        })

    def test_measures_only_valid(self) -> None:
        TabSpec.model_validate({
            "type": "tab",
            "lines": [{"measures": [{"beats": [{"notes": [0] * 6}]}]}],
        })

    def test_neither_beats_nor_measures_invalid(self) -> None:
        with pytest.raises(ValidationError):
            TabSpec.model_validate({
                "type": "tab",
                "lines": [{}],
            })

    def test_both_beats_and_measures_invalid(self) -> None:
        with pytest.raises(ValidationError):
            TabSpec.model_validate({
                "type": "tab",
                "lines": [{
                    "beats": [{"notes": [0] * 6}],
                    "measures": [{"beats": [{"notes": [0] * 6}]}],
                }],
            })


# ── Measures format rendering (FEAT-001) ──────────────────────────────────────


class TestSingleMeasureFormat:
    """measures format with one measure renders identically to flat beats."""

    beats_spec = TabSpec.model_validate({
        "type": "tab",
        "lines": [{"beats": [{"notes": [0, 2, 2, 0, 0, 0], "label": "Em"}]}],
    })
    measures_spec = TabSpec.model_validate({
        "type": "tab",
        "lines": [{"measures": [{"beats": [{"notes": [0, 2, 2, 0, 0, 0], "label": "Em"}]}]}],
    })

    def test_same_output_as_flat_beats(self) -> None:
        assert render_tab(self.beats_spec).plain == render_tab(self.measures_spec).plain


class TestMultipleMeasures:
    """Four one-beat measures produce inter-measure bar lines."""

    spec = TabSpec.model_validate({
        "type": "tab",
        "title": "G – D – Em – C",
        "time": "4/4",
        "lines": [
            {
                "measures": [
                    {"beats": [{"notes": [3, 2, 0, 0, 0, 3], "label": "G"}]},
                    {"beats": [{"notes": [None, None, 0, 2, 3, 2], "label": "D"}]},
                    {"beats": [{"notes": [0, 2, 2, 0, 0, 0], "label": "Em"}]},
                    {"beats": [{"notes": [None, 3, 2, 0, 1, 0], "label": "C"}]},
                ]
            }
        ],
    })

    def test_title_in_output(self) -> None:
        assert "G – D – Em – C" in render_tab(self.spec).plain

    def test_all_labels_present(self) -> None:
        plain = render_tab(self.spec).plain
        for label in ("G", "D", "Em", "C"):
            assert label in plain

    def test_inter_measure_bar_lines(self) -> None:
        """4 measures → opening | + 3 inter-measure | + closing | = 5 per string row."""
        lines = render_tab(self.spec).plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        for row in string_rows:
            assert row.count("|") == 5, f"Expected 5 bars, got {row.count('|')} in: {row!r}"

    def test_six_string_rows(self) -> None:
        lines = render_tab(self.spec).plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        assert len(string_rows) == 6

    def test_all_string_rows_same_width(self) -> None:
        lines = render_tab(self.spec).plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        widths = {len(r) for r in string_rows}
        assert len(widths) == 1


# ── Beat duration (FEAT-002) ───────────────────────────────────────────────────


class TestBeatDuration:
    """duration > 1 expands the column width proportionally."""

    def _single_beat_spec(self, duration: int) -> TabSpec:
        return TabSpec.model_validate({
            "type": "tab",
            "lines": [
                {"measures": [{"beats": [{"notes": [0] * 6, "duration": duration}]}]}
            ],
        })

    def test_duration_1_row_width(self) -> None:
        # "e |" (3) + col_width*1 (3) + "|" (1) = 7
        lines = render_tab(self._single_beat_spec(1)).plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        assert all(len(r) == 7 for r in string_rows)

    def test_duration_4_row_width(self) -> None:
        # "e |" (3) + col_width*4 (12) + "|" (1) = 16
        lines = render_tab(self._single_beat_spec(4)).plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        assert all(len(r) == 16 for r in string_rows)

    def test_all_rows_same_width_for_all_durations(self) -> None:
        for duration in (1, 2, 3, 4):
            lines = render_tab(self._single_beat_spec(duration)).plain.splitlines()
            string_rows = [l for l in lines if "|" in l]
            widths = {len(r) for r in string_rows}
            assert len(widths) == 1, f"Inconsistent widths for duration={duration}"

    def test_default_duration_is_1(self) -> None:
        """A beat with no duration field behaves the same as duration=1."""
        spec_no_dur = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"measures": [{"beats": [{"notes": [0] * 6}]}]}],
        })
        assert (
            render_tab(spec_no_dur).plain
            == render_tab(self._single_beat_spec(1)).plain
        )
