"""Tests for the chord box renderer (M2)."""

import pytest
from pydantic import ValidationError

from guitar_tui.engine.chord_renderer import render_chord
from guitar_tui.engine.models import ChordSpec


# ── helpers ───────────────────────────────────────────────────────────────────


def make_chord(
    frets: list,
    *,
    title: str | None = None,
    base_fret: int = 1,
    fingers: list | None = None,
    barre: dict | None = None,
) -> ChordSpec:
    data: dict = {"type": "chord", "frets": frets}
    if title:
        data["title"] = title
    if base_fret != 1:
        data["base_fret"] = base_fret
    if fingers:
        data["fingers"] = fingers
    if barre:
        data["barre"] = barre
    return ChordSpec.model_validate(data)


# ── G major (open chord) ───────────────────────────────────────────────────────


class TestGMajor:
    """frets=[3,2,0,0,0,3]  — open strings on D, G, B; dots at A2 and E/e3."""

    spec = make_chord([3, 2, 0, 0, 0, 3], title="G Major")

    def test_title_in_output(self) -> None:
        text = render_chord(self.spec)
        assert "G Major" in text.plain

    def test_string_header_present(self) -> None:
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        header = lines[2]  # title, blank, header
        assert "E" in header
        assert "e" in header

    def test_open_string_markers(self) -> None:
        text = render_chord(self.spec)
        marker_line = text.plain.splitlines()[3]  # above-nut row
        # D, G, B strings (indices 2, 3, 4) are open → ○
        assert marker_line.count("○") == 3

    def test_nut_line_present(self) -> None:
        text = render_chord(self.spec)
        assert "╒" in text.plain
        assert "╕" in text.plain

    def test_dot_at_a_string_row2(self) -> None:
        # A (index 1) has fret 2 → row 2 should have ● in A position
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        # rows: nut=4, content row1=5, sep=6, content row2=7
        row2 = lines[7]
        assert "●" in row2

    def test_dots_at_e_and_low_e_row3(self) -> None:
        # E (index 0) and e (index 5) both have fret 3 → row 3 has 2 dots
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        row3 = lines[9]
        assert row3.count("●") == 2

    def test_four_fret_rows_rendered(self) -> None:
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        # title + blank + header + markers + nut + (content + sep) * 3 + content + bottom
        # = 2 + 1 + 1 + 1 + (3 * 2) + 1 = 12 lines
        content_rows = [l for l in lines if l.startswith("│")]
        assert len(content_rows) == 4

    def test_bottom_border_present(self) -> None:
        text = render_chord(self.spec)
        assert "└" in text.plain
        assert "┘" in text.plain

    def test_row_width_consistent(self) -> None:
        text = render_chord(self.spec)
        grid_lines = [
            l for l in text.plain.splitlines()
            if l and l[0] in "╒╕├┼┤└┘│┌┐"
        ]
        widths = {len(l) for l in grid_lines}
        assert len(widths) == 1, f"Inconsistent row widths: {widths}"


# ── F major barre ──────────────────────────────────────────────────────────────


class TestFMajorBarre:
    """frets=[1,1,2,3,3,1] barre fret=1 from=1 to=6."""

    spec = make_chord(
        [1, 1, 2, 3, 3, 1],
        title="F Major",
        fingers=[1, 1, 2, 3, 4, 1],
        barre={"fret": 1, "from": 1, "to": 6, "finger": 1},
    )

    def test_barre_row_has_barre_char(self) -> None:
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        # row 1 is the first content row after the nut (index 5 in 0-based lines)
        row1 = lines[5]
        assert "▬" in row1

    def test_barre_covers_all_six_strings(self) -> None:
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        row1 = lines[5]
        assert row1.count("▬") == 6

    def test_dots_in_higher_rows(self) -> None:
        # frets 2 and 3 have individual dots (D=2, G=3, B=3)
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        row2 = lines[7]
        row3 = lines[9]
        assert "●" in row2
        assert "●" in row3

    def test_no_barre_char_in_row2(self) -> None:
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        row2 = lines[7]
        assert "▬" not in row2


# ── A major (muted low E) ──────────────────────────────────────────────────────


class TestAMajorMuted:
    """frets=[null,0,2,2,2,0]  — muted low E, open A and e."""

    spec = make_chord([None, 0, 2, 2, 2, 0], title="A Major")

    def test_muted_marker_for_low_e(self) -> None:
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        marker_line = lines[3]
        assert "X" in marker_line

    def test_open_markers_for_a_and_e(self) -> None:
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        marker_line = lines[3]
        assert marker_line.count("○") == 2

    def test_dots_at_row2(self) -> None:
        # D, G, B strings all have fret 2
        text = render_chord(self.spec)
        lines = text.plain.splitlines()
        row2 = lines[7]
        assert row2.count("●") == 3


# ── High-position chord (base_fret > 1) ───────────────────────────────────────


class TestHighPosition:
    """base_fret=5 → top border shows '5fr', no nut double line."""

    spec = make_chord([1, 3, 3, 2, 1, 1], base_fret=5, title="Bm")

    def test_fret_label_in_top_border(self) -> None:
        text = render_chord(self.spec)
        assert "5fr" in text.plain

    def test_no_nut_double_line(self) -> None:
        text = render_chord(self.spec)
        assert "╒" not in text.plain

    def test_open_top_border_present(self) -> None:
        text = render_chord(self.spec)
        assert "┌" in text.plain


# ── Validation errors ──────────────────────────────────────────────────────────


class TestValidation:
    def test_frets_not_six_elements_raises(self) -> None:
        with pytest.raises(ValidationError, match="6 elements"):
            ChordSpec.model_validate({"type": "chord", "frets": [0, 1, 2]})

    def test_fingers_not_six_elements_raises(self) -> None:
        with pytest.raises(ValidationError, match="6 elements"):
            ChordSpec.model_validate({
                "type": "chord",
                "frets": [0, 0, 0, 0, 0, 0],
                "fingers": [1, 2, 3],
            })

    def test_missing_frets_raises(self) -> None:
        with pytest.raises(ValidationError):
            ChordSpec.model_validate({"type": "chord"})
