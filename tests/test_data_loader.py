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
        assert len(am.voicings) >= 1
        # Find the open voicing by id (load order may vary across files)
        open_v = next((v for v in am.voicings if v.id == "default"), None)
        assert open_v is not None, "Am should have a 'default' (open) voicing"
        assert open_v.frets == [None, 0, 2, 2, 1, 0]
        assert open_v.fingers == [None, None, 2, 3, 1, None]

    def test_f_barre(self) -> None:
        loader = DataLoader()
        loader.load()
        f = loader.chords["F"]
        assert len(f.voicings) >= 1
        assert f.voicings[0].barre is not None
        assert f.voicings[0].barre.fret == 1

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

    # ── barre chords ──────────────────────────────────────────────────────────

    def test_barre_chords_e_shape_present(self) -> None:
        loader = DataLoader()
        loader.load()
        # G major has a default open voicing AND an e_shape barre voicing
        g = loader.chords["G"]
        ids = [v.id for v in g.voicings]
        assert "e_shape" in ids, "G should have an e_shape barre voicing"
        e_shape = next(v for v in g.voicings if v.id == "e_shape")
        assert e_shape.base_fret == 3
        assert e_shape.barre is not None

    def test_barre_chords_a_shape_present(self) -> None:
        loader = DataLoader()
        loader.load()
        # C major should have an a_shape barre voicing (3rd fret)
        c = loader.chords["C"]
        ids = [v.id for v in c.voicings]
        assert "a_shape" in ids, "C should have an a_shape barre voicing"
        a_shape = next(v for v in c.voicings if v.id == "a_shape")
        assert a_shape.base_fret == 3

    def test_voicing_merge_preserves_default(self) -> None:
        loader = DataLoader()
        loader.load()
        # Am must have BOTH its original open 'default' voicing and the barre voicings
        am = loader.chords["Am"]
        ids = [v.id for v in am.voicings]
        assert "default" in ids
        assert "e_shape" in ids
        assert "a_shape" in ids

    # ── seventh chords ────────────────────────────────────────────────────────

    def test_dominant7_chords_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        for name in ["E7", "A7", "D7", "G7"]:
            assert name in loader.chords, f"Missing dominant 7th chord: {name}"

    def test_major7_chords_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        for name in ["Emaj7", "Amaj7", "Dmaj7", "Gmaj7"]:
            assert name in loader.chords, f"Missing major 7th chord: {name}"

    def test_minor7_chords_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        for name in ["Em7", "Am7", "Dm7", "Bm7"]:
            assert name in loader.chords, f"Missing minor 7th chord: {name}"

    def test_e7_voicing(self) -> None:
        loader = DataLoader()
        loader.load()
        e7 = loader.chords["E7"]
        assert e7.full_name == "E dominant 7th"
        assert e7.voicings[0].frets == [0, 2, 0, 1, 0, 0]

    # ── extended chords ───────────────────────────────────────────────────────

    def test_sus_chords_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        for name in ["Dsus2", "Asus2", "Dsus4", "Asus4", "Esus4", "Gsus4"]:
            assert name in loader.chords, f"Missing sus chord: {name}"

    def test_add_chords_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        for name in ["Cadd9", "Gadd9"]:
            assert name in loader.chords, f"Missing add chord: {name}"

    def test_power_chords_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        for name in ["E5", "A5", "D5", "G5", "C5"]:
            assert name in loader.chords, f"Missing power chord: {name}"

    # ── additional scales ─────────────────────────────────────────────────────

    def test_natural_minor_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        assert "natural_minor" in loader.scales
        scale = loader.scales["natural_minor"]
        assert scale.intervals == ["1", "2", "b3", "4", "5", "b6", "b7"]
        assert len(scale.positions) == 5

    def test_major_scale_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        assert "major" in loader.scales
        scale = loader.scales["major"]
        assert scale.intervals == ["1", "2", "3", "4", "5", "6", "7"]
        assert len(scale.positions) == 5

    def test_major_pentatonic_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        assert "major_pentatonic" in loader.scales
        scale = loader.scales["major_pentatonic"]
        assert scale.intervals == ["1", "2", "3", "5", "6"]
        assert len(scale.positions) == 5

    def test_blues_scale_loaded(self) -> None:
        loader = DataLoader()
        loader.load()
        assert "blues_scale" in loader.scales
        scale = loader.scales["blues_scale"]
        assert scale.intervals == ["1", "b3", "4", "b5", "5", "b7"]
        assert len(scale.positions) == 5


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


# ── ChordEntry / multi-voicing (FEAT-004) ─────────────────────────────────────


class TestChordEntry:
    """Legacy and new-format YAML both produce correct ChordEntry objects."""

    def _loader_with_chords(self, chord_yaml: str, tmp_path: Path) -> DataLoader:
        chords_dir = tmp_path / "chords"
        chords_dir.mkdir(parents=True)
        (tmp_path / "scales").mkdir()
        (tmp_path / "tunings.yaml").write_text(
            "standard:\n  name: Standard\n  strings: [E2, A2, D3, G3, B3, E4]\n"
        )
        (chords_dir / "test.yaml").write_text(chord_yaml)
        loader = DataLoader(data_dir=tmp_path)
        loader.load()
        return loader

    def test_legacy_format_produces_one_voicing(self, tmp_path: Path) -> None:
        chord_yaml = make_chord_yaml([
            {"name": "Am", "full_name": "A minor", "frets": [None, 0, 2, 2, 1, 0]}
        ])
        loader = self._loader_with_chords(chord_yaml, tmp_path)
        entry = loader.chords["Am"]
        assert entry.name == "Am"
        assert entry.full_name == "A minor"
        assert len(entry.voicings) == 1
        assert entry.voicings[0].frets == [None, 0, 2, 2, 1, 0]
        assert entry.voicings[0].id == "default"

    def test_new_format_produces_multiple_voicings(self, tmp_path: Path) -> None:
        chord_yaml = yaml.dump({
            "chords": [{
                "name": "Am",
                "full_name": "A minor",
                "voicings": [
                    {"id": "open", "label": "Open", "frets": [None, 0, 2, 2, 1, 0]},
                    {
                        "id": "barre_5", "label": "Barre (5th fret)",
                        "frets": [0, 0, 2, 2, 1, 0], "base_fret": 5,
                    },
                ],
            }]
        })
        loader = self._loader_with_chords(chord_yaml, tmp_path)
        entry = loader.chords["Am"]
        assert len(entry.voicings) == 2
        assert entry.voicings[0].id == "open"
        assert entry.voicings[1].id == "barre_5"
        assert entry.voicings[1].base_fret == 5

    def test_chords_keyed_by_name(self, tmp_path: Path) -> None:
        chord_yaml = make_chord_yaml([
            {"name": "G", "full_name": "G major", "frets": [3, 2, 0, 0, 0, 3]},
            {"name": "C", "full_name": "C major", "frets": [None, 3, 2, 0, 1, 0]},
        ])
        loader = self._loader_with_chords(chord_yaml, tmp_path)
        assert "G" in loader.chords
        assert "C" in loader.chords
