"""Tests for the Theory Web layer: chord memberships, progression realization,
transposition helpers, progressions data, and theory_refs lesson indexing."""

from pathlib import Path

import pytest

from guitar_tui.loaders.data_loader import DataLoader, DataLoadError
from guitar_tui.loaders.lesson_loader import LessonLoader
from guitar_tui.theory.web import (
    ChordMembership,
    chord_memberships,
    fit_position_shift,
    realize_progression,
    transposition_offset,
)


# ── chord_memberships ──────────────────────────────────────────────────────────


class TestChordMemberships:
    def test_am_functions(self) -> None:
        got = set(chord_memberships("Am"))
        assert ChordMembership("C", "Major", "vi") in got
        assert ChordMembership("G", "Major", "ii") in got
        assert ChordMembership("F", "Major", "iii") in got
        assert ChordMembership("A", "Minor", "i") in got
        assert ChordMembership("E", "Minor", "iv") in got
        assert ChordMembership("D", "Minor", "v") in got
        assert len(got) == 6

    def test_major_chord_functions(self) -> None:
        got = set(chord_memberships("C"))
        # Major triad slots: I, IV, V in major; bIII, bVI, bVII in minor.
        assert ChordMembership("C", "Major", "I") in got
        assert ChordMembership("G", "Major", "IV") in got
        assert ChordMembership("F", "Major", "V") in got
        assert ChordMembership("A", "Minor", "bIII") in got
        assert ChordMembership("E", "Minor", "bVI") in got
        assert ChordMembership("D", "Minor", "bVII") in got
        assert len(got) == 6

    def test_diminished_chord_functions(self) -> None:
        got = set(chord_memberships("B°"))
        assert ChordMembership("C", "Major", "vii°") in got
        assert ChordMembership("A", "Minor", "ii°") in got
        assert len(got) == 2

    def test_enharmonic_names_agree(self) -> None:
        assert set(chord_memberships("C#m")) == set(chord_memberships("Dbm"))
        assert set(chord_memberships("Ab")) == set(chord_memberships("G#"))

    def test_non_diatonic_quality_returns_empty(self) -> None:
        assert chord_memberships("Cmaj7") == []
        assert chord_memberships("Asus4") == []

    def test_every_triad_has_six_memberships(self) -> None:
        # Any major or minor triad is diatonic to exactly 3 major + 3 minor keys.
        from guitar_tui.theory.keys import KEY_NAMES
        for root in KEY_NAMES:
            assert len(chord_memberships(root)) == 6, root
            assert len(chord_memberships(root + "m")) == 6, root


# ── realize_progression ────────────────────────────────────────────────────────


class TestRealizeProgression:
    def test_pop_progression_in_c(self) -> None:
        got = realize_progression("C", "Major", ["I", "V", "vi", "IV"])
        assert got == [("I", "C"), ("V", "G"), ("vi", "Am"), ("IV", "F")]

    def test_minor_pop_in_a(self) -> None:
        got = realize_progression("A", "Minor", ["i", "bVI", "bIII", "bVII"])
        assert [c for _, c in got] == ["Am", "F", "C", "G"]

    def test_blues_in_e(self) -> None:
        got = realize_progression("E", "Blues", ["I7", "IV7", "V7"])
        assert [c for _, c in got] == ["E7", "A7", "B7"]

    def test_dorian_vamp_in_d(self) -> None:
        got = realize_progression("D", "Dorian", ["i", "IV"])
        assert [c for _, c in got] == ["Dm", "G"]

    def test_unknown_numeral_raises(self) -> None:
        with pytest.raises(ValueError, match="not diatonic"):
            realize_progression("C", "Major", ["I", "bII"])


# ── transposition helpers ──────────────────────────────────────────────────────


class TestTransposition:
    def test_offset_basics(self) -> None:
        assert transposition_offset("C", "C") == 0
        assert transposition_offset("A", "C") == 9
        assert transposition_offset("C", "A") == 3
        assert transposition_offset("Bb", "A#") == 0  # enharmonic

    def test_fit_shift_in_range_stays(self) -> None:
        assert fit_position_shift(7, 10, 15) == 0

    def test_fit_shift_above_range_drops_octave(self) -> None:
        assert fit_position_shift(16, 19, 15) == -12

    def test_fit_shift_below_range_raises_octave(self) -> None:
        assert fit_position_shift(-3, 1, 15) == 12

    def test_fit_shift_prefers_lowest_playable(self) -> None:
        # [12, 15] fits as-is, but [0, 3] is the preferred lower placement.
        assert fit_position_shift(12, 15, 15) == -12


# ── progressions data (packaged) ───────────────────────────────────────────────


@pytest.fixture(scope="module")
def data_loader() -> DataLoader:
    loader = DataLoader()
    loader.load()
    return loader


class TestPackagedProgressions:
    def test_packaged_file_exists_and_loads(self, data_loader: DataLoader) -> None:
        assert len(data_loader.progressions) >= 14

    def test_known_entries(self, data_loader: DataLoader) -> None:
        assert "pop_four_chord" in data_loader.progressions
        assert data_loader.progressions["twelve_bar"].quality == "Blues"

    def test_progressions_for_quality(self, data_loader: DataLoader) -> None:
        majors = data_loader.progressions_for("Major")
        assert len(majors) >= 5
        assert all(p.quality == "Major" for p in majors)
        assert data_loader.progressions_for("Klezmer") == []

    def test_all_progressions_realize_in_all_keys(self, data_loader: DataLoader) -> None:
        from guitar_tui.theory.keys import KEY_NAMES
        for prog in data_loader.progressions.values():
            for key in KEY_NAMES:
                realized = realize_progression(key, prog.quality, prog.numerals)
                assert len(realized) == len(prog.numerals)

    def test_lesson_slugs_exist(self, data_loader: DataLoader) -> None:
        lessons = LessonLoader()
        lessons.load()
        for prog in data_loader.progressions.values():
            for slug in prog.lessons:
                assert slug in lessons.lessons, (
                    f"progression '{prog.id}' references missing lesson '{slug}'"
                )


# ── progressions data (validation) ─────────────────────────────────────────────


def _minimal_data_dir(tmp_path: Path) -> Path:
    (tmp_path / "chords").mkdir()
    (tmp_path / "scales").mkdir()
    (tmp_path / "tunings.yaml").write_text(
        "standard:\n  name: Standard\n  strings: [E2, A2, D3, G3, B3, E4]\n"
    )
    return tmp_path


class TestProgressionValidation:
    def test_missing_file_is_not_an_error(self, tmp_path: Path) -> None:
        loader = DataLoader(data_dir=_minimal_data_dir(tmp_path))
        loader.load()
        assert loader.progressions == {}

    def test_unknown_quality_is_hard_error(self, tmp_path: Path) -> None:
        data_dir = _minimal_data_dir(tmp_path)
        (data_dir / "progressions.yaml").write_text(
            "progressions:\n"
            "  - id: bad\n    name: Bad\n    quality: Klezmer\n"
            "    numerals: [I]\n"
        )
        with pytest.raises(DataLoadError, match="unknown quality"):
            DataLoader(data_dir=data_dir).load()

    def test_unknown_numeral_is_hard_error(self, tmp_path: Path) -> None:
        data_dir = _minimal_data_dir(tmp_path)
        (data_dir / "progressions.yaml").write_text(
            "progressions:\n"
            "  - id: bad\n    name: Bad\n    quality: Major\n"
            "    numerals: [I, bII]\n"
        )
        with pytest.raises(DataLoadError, match="degree table"):
            DataLoader(data_dir=data_dir).load()

    def test_duplicate_id_is_hard_error(self, tmp_path: Path) -> None:
        data_dir = _minimal_data_dir(tmp_path)
        (data_dir / "progressions.yaml").write_text(
            "progressions:\n"
            "  - id: dup\n    name: A\n    quality: Major\n    numerals: [I]\n"
            "  - id: dup\n    name: B\n    quality: Major\n    numerals: [V]\n"
        )
        with pytest.raises(DataLoadError, match="Duplicate progression id"):
            DataLoader(data_dir=data_dir).load()

    def test_bad_id_slug_is_hard_error(self, tmp_path: Path) -> None:
        data_dir = _minimal_data_dir(tmp_path)
        (data_dir / "progressions.yaml").write_text(
            "progressions:\n"
            "  - id: Bad-Id\n    name: A\n    quality: Major\n    numerals: [I]\n"
        )
        with pytest.raises(DataLoadError, match="Invalid progression data"):
            DataLoader(data_dir=data_dir).load()

    def test_empty_numerals_is_hard_error(self, tmp_path: Path) -> None:
        data_dir = _minimal_data_dir(tmp_path)
        (data_dir / "progressions.yaml").write_text(
            "progressions:\n"
            "  - id: bad\n    name: A\n    quality: Major\n    numerals: []\n"
        )
        with pytest.raises(DataLoadError, match="Invalid progression data"):
            DataLoader(data_dir=data_dir).load()


# ── theory_refs frontmatter + reverse index ────────────────────────────────────


def _lesson_md(slug: str, position: int, theory_refs: list[str]) -> str:
    refs = "[" + ", ".join(f'"{r}"' for r in theory_refs) + "]"
    return (
        f"---\n"
        f"title: Lesson {slug}\n"
        f"slug: {slug}\n"
        f"difficulty: beginner\n"
        f"tags: [test]\n"
        f"module: test-module\n"
        f"position: {position}\n"
        f"theory_refs: {refs}\n"
        f"---\n"
        f"\nBody.\n"
    )


class TestTheoryRefs:
    def test_reverse_index_and_order(self, tmp_path: Path) -> None:
        (tmp_path / "b_lesson.md").write_text(
            _lesson_md("b_lesson", 2, ["scale:major", "chord:Am"])
        )
        (tmp_path / "a_lesson.md").write_text(
            _lesson_md("a_lesson", 1, ["scale:major"])
        )
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        # Curriculum order (position), not file order.
        assert loader.theory_ref_index["scale:major"] == ["a_lesson", "b_lesson"]
        assert loader.theory_ref_index["chord:Am"] == ["b_lesson"]
        got = loader.by_theory_ref("scale:major")
        assert [l.meta.slug for l in got] == ["a_lesson", "b_lesson"]
        assert loader.by_theory_ref("scale:nonexistent") == []

    def test_invalid_ref_format_is_hard_error(self, tmp_path: Path) -> None:
        from guitar_tui.loaders.lesson_loader import LessonLoadError

        (tmp_path / "bad_lesson.md").write_text(
            _lesson_md("bad_lesson", 1, ["riff:foo"])
        )
        loader = LessonLoader(lessons_dir=tmp_path)
        with pytest.raises(LessonLoadError):
            loader.load()

    def test_lessons_without_refs_default_empty(self, tmp_path: Path) -> None:
        (tmp_path / "plain.md").write_text(
            "---\ntitle: Plain\nslug: plain\ndifficulty: beginner\n"
            "tags: [test]\n---\n\nBody.\n"
        )
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        assert loader.lessons["plain"].meta.theory_refs == []
        assert loader.theory_ref_index == {}
