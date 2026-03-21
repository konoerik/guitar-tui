"""Tests for the guitar tablature renderer (M2)."""

import pytest
from pydantic import ValidationError

from guitar_tui.engine.models import TabSpec
from guitar_tui.engine.tab_renderer import _build_note_str, render_tab


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


# ── Bend notation ──────────────────────────────────────────────────────────────


class TestBendNotation:
    """bend: true appends 'b'; bend_target appends 'b{n}'."""

    def test_bend_suffix_in_staff(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [None, None, None, None, 8, None], "bend": True}]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]  # B string (index 4)
        assert "8b" in b_row

    def test_bend_with_target_in_staff(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [None, None, None, None, 7, None], "bend": True, "bend_target": 9}]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]  # B string
        assert "7b9" in b_row

    def test_bend_false_no_suffix(self) -> None:
        """Without bend=True, no 'b' appears after the fret number."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [None, None, None, None, 8, None]}]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]
        assert "8b" not in b_row

    def test_bend_does_not_affect_null_strings(self) -> None:
        """Bend suffix only appears on strings with a note, not on null strings."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [None, None, None, None, 8, None], "bend": True}]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        # All rows except B string should contain only dashes (no 'b')
        for i, row in enumerate(lines):
            if i != 1:  # skip B string row
                assert "b" not in row, f"Unexpected 'b' in string row {i}: {row!r}"

    def test_col_width_expands_for_bend_suffix(self) -> None:
        """A bend beat (e.g. '8b') widens all columns so rows stay equal width."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 8, None], "bend": True},
                {"notes": [None, None, None, None, 7, None]},
            ]}],
        })
        lines = [l for l in render_tab(spec).plain.splitlines() if "|" in l]
        widths = {len(r) for r in lines}
        assert len(widths) == 1

    def test_bend_target_col_width_expands(self) -> None:
        """bend_target (e.g. '7b9') may be wider than bare frets; all rows equal."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 7, None], "bend": True, "bend_target": 9},
                {"notes": [None, None, None, None, 5, None]},
            ]}],
        })
        lines = [l for l in render_tab(spec).plain.splitlines() if "|" in l]
        widths = {len(r) for r in lines}
        assert len(widths) == 1

    def test_build_note_str_bend(self) -> None:
        from guitar_tui.engine.models import TabBeat
        beat = TabBeat.model_validate({"notes": [None] * 6, "bend": True})
        assert _build_note_str(8, beat) == "8b"

    def test_build_note_str_bend_with_target(self) -> None:
        from guitar_tui.engine.models import TabBeat
        beat = TabBeat.model_validate({"notes": [None] * 6, "bend": True, "bend_target": 10})
        assert _build_note_str(8, beat) == "8b10"


# ── Vibrato notation ───────────────────────────────────────────────────────────


class TestVibratoNotation:
    """vibrato: true appends '~' suffix."""

    def test_vibrato_suffix_in_staff(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [None, None, None, None, 7, None], "vibrato": True}]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]  # B string
        assert "7~" in b_row

    def test_vibrato_false_no_tilde(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [None, None, None, None, 7, None]}]}],
        })
        plain = render_tab(spec).plain
        assert "~" not in plain

    def test_col_width_expands_for_vibrato(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 7, None], "vibrato": True},
                {"notes": [None, None, None, None, 5, None]},
            ]}],
        })
        lines = [l for l in render_tab(spec).plain.splitlines() if "|" in l]
        widths = {len(r) for r in lines}
        assert len(widths) == 1

    def test_build_note_str_vibrato(self) -> None:
        from guitar_tui.engine.models import TabBeat
        beat = TabBeat.model_validate({"notes": [None] * 6, "vibrato": True})
        assert _build_note_str(7, beat) == "7~"


# ── Bend + vibrato combined ────────────────────────────────────────────────────


class TestBendVibratoCombined:
    """bend and vibrato may appear together: '8b~' or '7b9~'."""

    def test_bend_and_vibrato_suffix_order(self) -> None:
        from guitar_tui.engine.models import TabBeat
        beat = TabBeat.model_validate({"notes": [None] * 6, "bend": True, "vibrato": True})
        assert _build_note_str(8, beat) == "8b~"

    def test_bend_target_and_vibrato(self) -> None:
        from guitar_tui.engine.models import TabBeat
        beat = TabBeat.model_validate({"notes": [None] * 6, "bend": True, "bend_target": 9, "vibrato": True})
        assert _build_note_str(7, beat) == "7b9~"

    def test_combined_appears_in_staff(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [None, None, None, None, 8, None], "bend": True, "vibrato": True}]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]
        assert "8b~" in b_row

    def test_all_rows_equal_width_with_combined(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 8, None], "bend": True, "vibrato": True},
                {"notes": [None, None, None, None, 5, None]},
            ]}],
        })
        lines = [l for l in render_tab(spec).plain.splitlines() if "|" in l]
        widths = {len(r) for r in lines}
        assert len(widths) == 1


# ── Technique connectors ───────────────────────────────────────────────────────


class TestTechniqueConnectors:
    """technique replaces the leading '─' of the beat's column on non-null strings."""

    def _two_beat_spec(self, technique: str) -> TabSpec:
        return TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 5, None]},
                {"notes": [None, None, None, None, 7, None], "technique": technique},
            ]}],
        })

    def test_hammer_on_in_staff(self) -> None:
        plain = render_tab(self._two_beat_spec("h")).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]  # B string
        assert "h" in b_row

    def test_pull_off_in_staff(self) -> None:
        plain = render_tab(self._two_beat_spec("p")).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]
        assert "p" in b_row

    def test_slide_up_in_staff(self) -> None:
        plain = render_tab(self._two_beat_spec("/")).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]
        assert "/" in b_row

    def test_slide_down_in_staff(self) -> None:
        plain = render_tab(self._two_beat_spec("\\")).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]
        assert "\\" in b_row

    def test_technique_only_on_non_null_strings(self) -> None:
        """'h' must appear only on B string, not on null strings."""
        plain = render_tab(self._two_beat_spec("h")).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        for i, row in enumerate(lines):
            if i != 1:  # skip B string
                assert "h" not in row, f"Unexpected 'h' in row {i}: {row!r}"

    def test_all_rows_equal_width_with_technique(self) -> None:
        lines = [l for l in render_tab(self._two_beat_spec("h")).plain.splitlines() if "|" in l]
        widths = {len(r) for r in lines}
        assert len(widths) == 1

    def test_technique_with_bend(self) -> None:
        """Technique and bend may combine: slide into a bent note."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 5, None]},
                {"notes": [None, None, None, None, 7, None], "technique": "/", "bend": True},
            ]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        b_row = lines[1]
        assert "/" in b_row
        assert "7b" in b_row

    def test_multi_string_technique(self) -> None:
        """Technique appears on all non-null strings in the beat."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, 5, 5, None]},
                {"notes": [None, None, None, 7, 7, None], "technique": "h"},
            ]}],
        })
        plain = render_tab(spec).plain
        lines = [l for l in plain.splitlines() if "|" in l]
        # D string (index 2) and B string (index 1) should both contain 'h'
        assert "h" in lines[1], f"B row missing 'h': {lines[1]!r}"
        assert "h" in lines[2], f"G row missing 'h': {lines[2]!r}"


# ── Technique model validation ─────────────────────────────────────────────────


class TestTechniqueValidation:
    def test_valid_hammer_on(self) -> None:
        TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [0] * 6, "technique": "h"}]}],
        })

    def test_valid_pull_off(self) -> None:
        TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [0] * 6, "technique": "p"}]}],
        })

    def test_valid_slide_up(self) -> None:
        TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [0] * 6, "technique": "/"}]}],
        })

    def test_valid_slide_down(self) -> None:
        TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [0] * 6, "technique": "\\"}]}],
        })

    def test_invalid_technique_raises(self) -> None:
        with pytest.raises(ValidationError):
            TabSpec.model_validate({
                "type": "tab",
                "lines": [{"beats": [{"notes": [0] * 6, "technique": "x"}]}],
            })

    def test_none_technique_is_default(self) -> None:
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [{"notes": [0] * 6}]}],
        })
        assert spec.lines[0].beats[0].technique is None  # type: ignore[union-attr]


# ── Label alignment with suffixes ─────────────────────────────────────────────


class TestLabelAlignmentWithSuffixes:
    """Labels must align with fret digits even when bend/vibrato suffixes widen columns."""

    def test_label_aligns_with_fret_not_suffix(self) -> None:
        """A label under a bend beat must align with the fret digit, not the suffix chars.

        Without the fix, label.center(col_width) drifts right by the suffix width.
        With the fix, label.center(max_fret_width + 2) keeps the label at position 1.
        """
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 5, None], "label": "A"},
                {"notes": [None, None, None, None, 5, None],
                 "label": "F", "bend": True, "bend_target": 7, "vibrato": True},
            ]}],
        })
        text = render_tab(spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        label_row = lines[-1]

        b_row = string_rows[1]  # B string (index 4)

        # Position of first fret digit "5" in beat 1 of the B string row
        fret1_pos = b_row.index("5")

        # Position of label "A" in the label row — must match fret1_pos
        label_a_pos = label_row.index("A")
        assert fret1_pos == label_a_pos, (
            f"Label 'A' at col {label_a_pos} but fret '5' at col {fret1_pos}; "
            f"b_row={b_row!r}, label_row={label_row!r}"
        )

    def test_label_row_width_equals_string_row_width(self) -> None:
        """The label row must be the same width as string rows (including suffix padding)."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, 8, None],
                 "label": "bend", "bend": True, "bend_target": 10},
                {"notes": [None, None, None, None, 8, None], "label": "rel"},
                {"notes": [None, None, None, 7, None, None], "label": "D"},
            ]}],
        })
        lines = render_tab(spec).plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        label_row = lines[-1]
        assert len(label_row) == len(string_rows[0]), (
            f"Label row width {len(label_row)} != string row width {len(string_rows[0])}"
        )

    def test_no_suffix_label_alignment_unchanged(self) -> None:
        """Without any suffixes, label centering behaves identically to before."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{"beats": [
                {"notes": [None, None, None, None, None, 7], "label": "E"},
                {"notes": [None, None, None, None, None, 10], "label": "D"},
            ]}],
        })
        text = render_tab(spec)
        lines = text.plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        label_row = lines[-1]
        e_row = string_rows[0]

        fret_pos = e_row.index("7")
        label_pos = label_row.index("E")
        assert fret_pos == label_pos, (
            f"Fret '7' at col {fret_pos} but label 'E' at col {label_pos}"
        )


# ── Two-row label collision detection ─────────────────────────────────────────


class TestTwoRowLabels:
    """Collision-detection places labels on two rows when they would overlap."""

    def _spec(self, beats_data: list) -> TabSpec:
        return TabSpec.model_validate({"type": "tab", "lines": [{"beats": beats_data}]})

    def _label_rows(self, spec: TabSpec) -> list[str]:
        """Return all non-empty output lines that are not string rows."""
        lines = render_tab(spec).plain.splitlines()
        return [l for l in lines if "|" not in l and l.strip()]

    def test_non_colliding_labels_single_row(self) -> None:
        """Labels that do not overlap all appear on row A — only one label row output."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "h", "technique": "h"},
            {"notes": [None, None, None, None, 7, None], "label": "p", "technique": "p"},
        ])
        assert len(self._label_rows(spec)) == 1

    def test_colliding_labels_produce_two_rows(self) -> None:
        """A 4-char label on a 3-char column overflows into the next beat, forcing row B."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "pick"},
            {"notes": [None, None, None, None, 7, None], "label": "h", "technique": "h"},
        ])
        assert len(self._label_rows(spec)) == 2

    def test_first_label_on_row_a(self) -> None:
        """The first label always appears on row A."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "pick"},
            {"notes": [None, None, None, None, 7, None], "label": "h", "technique": "h"},
        ])
        label_rows = self._label_rows(spec)
        assert "pick" in label_rows[0]

    def test_colliding_label_on_row_b(self) -> None:
        """A label that collides with row A appears on row B."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "pick"},
            {"notes": [None, None, None, None, 7, None], "label": "h", "technique": "h"},
        ])
        label_rows = self._label_rows(spec)
        assert "h" in label_rows[1]

    def test_label_aligns_with_fret_digit(self) -> None:
        """Label first char sits at the same column as the fret digit."""
        spec = self._spec([
            {"notes": [None, None, None, None, 8, None],
             "label": "bend", "bend": True, "bend_target": 10},
        ])
        lines = render_tab(spec).plain.splitlines()
        b_row = [l for l in lines if "|" in l][1]  # B string
        label_rows = self._label_rows(spec)
        fret_pos = b_row.index("8")
        label_pos = label_rows[0].index("b")  # first char of "bend"
        assert fret_pos == label_pos, (
            f"fret '8' at col {fret_pos}, label 'b' at col {label_pos}; "
            f"b_row={b_row!r}, label={label_rows[0]!r}"
        )

    def test_label_rows_same_width_as_string_rows(self) -> None:
        """Both label rows have the same character width as string rows."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "pick"},
            {"notes": [None, None, None, None, 7, None], "label": "h", "technique": "h"},
        ])
        lines = render_tab(spec).plain.splitlines()
        string_rows = [l for l in lines if "|" in l]
        for lr in self._label_rows(spec):
            assert len(lr) == len(string_rows[0]), (
                f"Label row width {len(lr)} != string row width {len(string_rows[0])}"
            )

    def test_three_consecutive_labels_fit_on_two_rows(self) -> None:
        """Three consecutive colliding labels distribute across at most two rows."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "pick"},
            {"notes": [None, None, None, None, 7, None], "label": "h", "technique": "h"},
            {"notes": [None, None, None, None, 8, None], "label": "h", "technique": "h"},
        ])
        label_rows = self._label_rows(spec)
        assert len(label_rows) <= 2
        combined = " ".join(label_rows)
        assert "pick" in combined
        assert combined.count("h") >= 2

    def test_no_label_rows_when_no_labels(self) -> None:
        """Tabs without any labels produce no label rows."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None]},
            {"notes": [None, None, None, None, 7, None]},
        ])
        assert self._label_rows(spec) == []

    def test_label_not_truncated_when_beat_wide_enough(self) -> None:
        """A label on a wide beat (bend+duration) is not truncated."""
        spec = self._spec([
            {"notes": [None, None, None, None, 8, None],
             "label": "bend", "bend": True, "bend_target": 10, "duration": 3},
        ])
        label_rows = self._label_rows(spec)
        assert "bend" in label_rows[0]

    def test_each_label_fully_readable_on_its_row(self) -> None:
        """Both labels appear intact on their respective rows (no overwrite or truncation)."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "pick"},
            {"notes": [None, None, None, None, 7, None], "label": "h", "technique": "h"},
        ])
        label_rows = self._label_rows(spec)
        assert "pick" in label_rows[0]
        assert "h" in label_rows[1]

    def test_bar_line_offset_accounted_in_label_position(self) -> None:
        """Label in second measure aligns with fret digit after the bar line char."""
        spec = TabSpec.model_validate({
            "type": "tab",
            "lines": [{
                "measures": [
                    {"beats": [{"notes": [None, None, None, None, 5, None]}]},
                    {"beats": [{"notes": [None, None, None, None, 7, None], "label": "vib"}]},
                ]
            }],
        })
        lines = render_tab(spec).plain.splitlines()
        b_row = [l for l in lines if "|" in l][1]  # B string
        label_rows = [l for l in lines if "|" not in l and l.strip()]
        fret_pos = b_row.rindex("7")
        label_pos = label_rows[0].index("v")  # first char of "vib"
        assert fret_pos == label_pos, (
            f"fret '7' at col {fret_pos}, 'v' at col {label_pos}; "
            f"b_row={b_row!r}, label={label_rows[0]!r}"
        )

    def test_only_row_b_never_output_alone(self) -> None:
        """Row A is always tried first; a single label always lands on row A."""
        spec = self._spec([
            {"notes": [None, None, None, None, 5, None], "label": "h", "technique": "h"},
        ])
        label_rows = self._label_rows(spec)
        assert len(label_rows) == 1
        assert "h" in label_rows[0]
