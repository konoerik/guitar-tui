"""Data loader — loads and validates all YAML data on startup.

Startup failure (DataLoadError) is intentional: silent corruption of music
data is worse than a clear error. See DECISIONS.md D1.
"""

from pathlib import Path

import yaml
from pydantic import ValidationError

from guitar_tui.loaders.models import (
    ChordLibrary,
    ChordVoicing,
    ScalePattern,
    Tuning,
)

_DEFAULT_DATA_DIR = Path(__file__).parent.parent / "data"


class DataLoadError(Exception):
    """Raised when data files are missing, malformed, or fail validation."""


class DataLoader:
    """Loads all YAML data from the data directory and validates it on startup.

    Usage:
        loader = DataLoader()
        loader.load()           # raises DataLoadError on any problem
        chord = loader.chords["Am"]
        scale = loader.scales["minor_pentatonic"]
        tuning = loader.tunings["standard"]
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or _DEFAULT_DATA_DIR
        self.chords: dict[str, ChordVoicing] = {}
        self.scales: dict[str, ScalePattern] = {}
        self.tunings: dict[str, Tuning] = {}

    def load(self) -> None:
        """Load and validate all data. Raises DataLoadError on any failure."""
        self._load_tunings()
        self._load_chords()
        self._load_scales()

    # ── private ───────────────────────────────────────────────────────────────

    def _load_tunings(self) -> None:
        path = self.data_dir / "tunings.yaml"
        raw: dict = self._read_yaml(path)
        for key, value in raw.items():
            try:
                self.tunings[key] = Tuning(**value)
            except (ValidationError, TypeError) as exc:
                raise DataLoadError(
                    f"Invalid tuning '{key}' in {path}: {exc}"
                ) from exc

    def _load_chords(self) -> None:
        chords_dir = self.data_dir / "chords"
        for path in sorted(chords_dir.glob("*.yaml")):
            raw: dict = self._read_yaml(path)
            try:
                library = ChordLibrary(**raw)
            except (ValidationError, TypeError) as exc:
                raise DataLoadError(
                    f"Invalid chord data in {path}: {exc}"
                ) from exc
            for chord in library.chords:
                self.chords[chord.name] = chord

    def _load_scales(self) -> None:
        scales_dir = self.data_dir / "scales"
        for path in sorted(scales_dir.glob("*.yaml")):
            raw: dict = self._read_yaml(path)
            try:
                scale = ScalePattern(**raw)
            except (ValidationError, TypeError) as exc:
                raise DataLoadError(
                    f"Invalid scale data in {path}: {exc}"
                ) from exc
            self.scales[scale.name] = scale

    @staticmethod
    def _read_yaml(path: Path) -> dict:
        try:
            with path.open() as f:
                data = yaml.safe_load(f)
        except FileNotFoundError as exc:
            raise DataLoadError(f"Data file not found: {path}") from exc
        except yaml.YAMLError as exc:
            raise DataLoadError(f"YAML parse error in {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise DataLoadError(f"Expected a YAML mapping in {path}, got {type(data).__name__}")
        return data
