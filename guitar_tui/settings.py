"""Persistent user settings for Guitar TUI.

Settings are stored as JSON in the platform-appropriate config directory:
  macOS:   ~/Library/Application Support/guitar-tui/settings.json
  Linux:   ~/.config/guitar-tui/settings.json
  Windows: %APPDATA%/guitar-tui/settings.json

Override the directory for testing via the GUITAR_TUI_CONFIG_DIR env var.
"""

import json
import os
from pathlib import Path

from platformdirs import user_config_dir
from pydantic import BaseModel, ValidationError


def _config_path() -> Path:
    override = os.environ.get("GUITAR_TUI_CONFIG_DIR")
    if override:
        return Path(override) / "settings.json"
    return Path(user_config_dir("guitar-tui")) / "settings.json"


class AppSettings(BaseModel):
    """All persisted user preferences. Unknown keys are ignored on load."""

    # Navigation
    last_lesson: str | None = None

    # Metronome
    metronome_bpm: int = 80
    metronome_time_sig: list[int] = [4, 4]  # [numerator, denominator]

    # Reference screen
    reference_key: str = "C"
    reference_scale: str = "major"


def load() -> AppSettings:
    """Load settings from disk. Returns defaults on missing or corrupt file."""
    path = _config_path()
    if not path.exists():
        return AppSettings()
    try:
        return AppSettings.model_validate_json(path.read_text(encoding="utf-8"))
    except (ValidationError, ValueError, OSError):
        return AppSettings()


def save(settings: AppSettings) -> None:
    """Write settings to disk, creating the directory if needed."""
    path = _config_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            settings.model_dump_json(indent=2),
            encoding="utf-8",
        )
    except OSError:
        pass  # never crash the app over a settings write failure
