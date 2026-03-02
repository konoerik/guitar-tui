"""Tests for the M1 data loader and Pydantic models."""

import textwrap
from pathlib import Path

import pytest
import yaml

from guitar_tui.loaders.data_loader import DataLoadError, DataLoader


# ── helpers ───────────────────────────────────────────────────────────────────

def make_chord_yaml(chords: list[dict]) -> str:
    return yaml.dump({"chords": chords})


def make_scale_yaml(overrides: dict | None = None) -> str:
    base = {
        "name": "test_scale",
        "full_name": "Test Scale",
        "key": "A",
        "intervals": ["1", "5"],
        "positions": [
            {
                "id": 1,
                "name": "Position 1",
                "fret_range": [5, 7],
                "notes": [
                    {"string": 6, "fret": 5, "degree": "1", "root": True},
                    {"string": 6, "fret": 7, "degree": "5"},
                ],
            }
        ],
    }
    if overrides:
        base.update(overrides)
    return yaml.dump(base)


# ── loading real data files ───────────────────────────────────────────────────

class TestLoadRealData:
    def test_load_succeeds(self) -> None:
        loader = DataLoader()
        loader.load()  # must not raise

    def test_chords_populated(self) -> None:
        loader = DataLoader()
        loader.load()
        assert len(loader.chords) > 0

    def test_scales_populated(self) -> None:
        loader = DataLoader()
        loader.load()
        assert len(loader.scales) > 0

    def test_tunings_populated(self) -> None:
        loader = DataLoader()
        loader.load()
        assert len(loader.tunings) > 0

    def test_open_chords_present(self) -> None:
        loader = DataLoader()
        loader.load()
        for name in ["Am", "A", "Bm", "C", "D", "Dm", "E", "Em", "F", "G"]:
            assert name in loader.chords, f"Missing chord: {name}"

    def test_am_voicing(self) -> None:
        loader = DataLoader()
        loader.load()
        am = loader.chords["Am"]
        assert am.full_name == "A minor"
        assert am.frets == [None, 0, 2, 2, 1, 0]
        assert am.fingers == [None, None, 2, 3, 1, None]

    def test_f_barre(self) -> None:
        loader = DataLoader()
        loader.load()
        f = loader.chords["F"]
        assert f.barre is not None
        assert f.barre.fret == 1

    def test_pentatonic_minor_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        assert "minor_pentatonic" in loader.scales

    def test_pentatonic_has_five_positions(self) -> None:
        loader = DataLoader()
        loader.load()
        scale = loader.scales["minor_pentatonic"]
        assert len(scale.positions) == 5

    def test_pentatonic_intervals(self) -> None:
        loader = DataLoader()
        loader.load()
        scale = loader.scales["minor_pentatonic"]
        assert scale.intervals == ["1", "b3", "4", "5", "b7"]

    def test_pentatonic_positions_have_twelve_notes(self) -> None:
        loader = DataLoader()
        loader.load()
        scale = loader.scales["minor_pentatonic"]
        for pos in scale.positions:
            assert len(pos.notes) == 12, (
                f"Position {pos.id} has {len(pos.notes)} notes, expected 12"
            )

    def test_standard_tuning(self) -> None:
        loader = DataLoader()
        loader.load()
        assert "standard" in loader.tunings
        assert loader.tunings["standard"].strings == [
            "E2", "A2", "D3", "G3", "B3", "E4"
        ]


# ── validation errors ─────────────────────────────────────────────────────────

class TestValidationErrors:
    def test_chord_frets_wrong_count(self, tmp_path: Path) -> None:
        chords_dir = tmp_path / "chords"
        chords_dir.mkdir(parents=True)
        (tmp_path / "scales").mkdir()
        (tmp_path / "tunings.yaml").write_text(
            "standard:\n  name: Standard\n  strings: [E2, A2, D3, G3, B3, E4]\n"
        )
        bad_chord = {"name": "X", "full_name": "Bad", "frets": [0, 1, 2]}  # only 3
        (chords_dir / "bad.yaml").write_text(make_chord_yaml([bad_chord]))

        loader = DataLoader(data_dir=tmp_path)
        with pytest.raises(DataLoadError, match="frets must have exactly 6"):
            loader.load()

    def test_chord_missing_required_field(self, tmp_path: Path) -> None:
        chords_dir = tmp_path / "chords"
        chords_dir.mkdir(parents=True)
        (tmp_path / "scales").mkdir()
        (tmp_path / "tunings.yaml").write_text(
            "standard:\n  name: Standard\n  strings: [E2, A2, D3, G3, B3, E4]\n"
        )
        # missing 'full_name'
        bad_chord = {"name": "X", "frets": [0, 0, 0, 0, 0, 0]}
        (chords_dir / "bad.yaml").write_text(make_chord_yaml([bad_chord]))

        loader = DataLoader(data_dir=tmp_path)
        with pytest.raises(DataLoadError):
            loader.load()

    def test_malformed_yaml(self, tmp_path: Path) -> None:
        chords_dir = tmp_path / "chords"
        chords_dir.mkdir(parents=True)
        (tmp_path / "scales").mkdir()
        (tmp_path / "tunings.yaml").write_text(
            "standard:\n  name: Standard\n  strings: [E2, A2, D3, G3, B3, E4]\n"
        )
        (chords_dir / "bad.yaml").write_text("chords: [\nnot valid yaml {{{{")

        loader = DataLoader(data_dir=tmp_path)
        with pytest.raises(DataLoadError, match="YAML parse error"):
            loader.load()

    def test_missing_data_file(self, tmp_path: Path) -> None:
        # tunings.yaml does not exist
        (tmp_path / "chords").mkdir()
        (tmp_path / "scales").mkdir()

        loader = DataLoader(data_dir=tmp_path)
        with pytest.raises(DataLoadError, match="not found"):
            loader.load()

    def test_scale_missing_required_field(self, tmp_path: Path) -> None:
        (tmp_path / "chords").mkdir()
        scales_dir = tmp_path / "scales"
        scales_dir.mkdir()
        (tmp_path / "tunings.yaml").write_text(
            "standard:\n  name: Standard\n  strings: [E2, A2, D3, G3, B3, E4]\n"
        )
        # missing 'key' field
        bad_scale = textwrap.dedent("""\
            name: bad_scale
            full_name: Bad Scale
            intervals: ["1", "5"]
            positions: []
        """)
        (scales_dir / "bad.yaml").write_text(bad_scale)

        loader = DataLoader(data_dir=tmp_path)
        with pytest.raises(DataLoadError):
            loader.load()

    def test_tuning_wrong_string_count(self, tmp_path: Path) -> None:
        (tmp_path / "chords").mkdir()
        (tmp_path / "scales").mkdir()
        (tmp_path / "tunings.yaml").write_text(
            "bad:\n  name: Bad\n  strings: [E2, A2, D3]\n"  # only 3 strings
        )

        loader = DataLoader(data_dir=tmp_path)
        with pytest.raises(DataLoadError, match="strings must have exactly 6"):
            loader.load()
