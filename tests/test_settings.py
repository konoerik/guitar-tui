"""Tests for persistent settings: load, save, defaults, round-trip."""

import json
import os
from pathlib import Path

import pytest

import guitar_tui.settings as settings_mod
from guitar_tui.settings import AppSettings, load, save


# ── Helpers ────────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Point all settings I/O at a temp directory for every test."""
    monkeypatch.setenv("GUITAR_TUI_CONFIG_DIR", str(tmp_path))
    yield tmp_path


def _settings_path(tmp_path: Path) -> Path:
    return tmp_path / "settings.json"


# ── Default values ─────────────────────────────────────────────────────────────


def test_load_returns_defaults_when_file_missing(tmp_path):
    result = load()
    assert isinstance(result, AppSettings)
    assert result.metronome_bpm == 80
    assert result.metronome_time_sig == [4, 4]
    assert result.reference_key == "C"
    assert result.reference_scale == "major"
    assert result.last_lesson is None


def test_defaults_are_sane():
    s = AppSettings()
    assert 40 <= s.metronome_bpm <= 220
    assert len(s.metronome_time_sig) == 2


# ── Save creates file ──────────────────────────────────────────────────────────


def test_save_creates_file(tmp_path):
    s = AppSettings()
    save(s)
    assert _settings_path(tmp_path).exists()


def test_save_creates_parent_directory(tmp_path, monkeypatch):
    nested = tmp_path / "a" / "b" / "c"
    monkeypatch.setenv("GUITAR_TUI_CONFIG_DIR", str(nested))
    s = AppSettings()
    save(s)
    assert (nested / "settings.json").exists()


def test_save_writes_valid_json(tmp_path):
    s = AppSettings(metronome_bpm=120)
    save(s)
    raw = _settings_path(tmp_path).read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["metronome_bpm"] == 120


# ── Round-trip ─────────────────────────────────────────────────────────────────


def test_round_trip_preserves_all_fields(tmp_path):
    original = AppSettings(
        last_lesson="minor_pentatonic_intro",
        metronome_bpm=120,
        metronome_time_sig=[3, 4],
        reference_key="G",
        reference_scale="dorian",
    )
    save(original)
    loaded = load()
    assert loaded.last_lesson == "minor_pentatonic_intro"
    assert loaded.metronome_bpm == 120
    assert loaded.metronome_time_sig == [3, 4]
    assert loaded.reference_key == "G"
    assert loaded.reference_scale == "dorian"


# ── Corrupt / invalid file ─────────────────────────────────────────────────────


def test_corrupt_json_returns_defaults(tmp_path):
    _settings_path(tmp_path).write_text("not valid json{{{", encoding="utf-8")
    result = load()
    assert isinstance(result, AppSettings)
    assert result.metronome_bpm == 80  # defaults


def test_invalid_schema_returns_defaults(tmp_path):
    _settings_path(tmp_path).write_text(
        json.dumps({"metronome_bpm": "not_an_int"}), encoding="utf-8"
    )
    result = load()
    assert isinstance(result, AppSettings)
    assert result.metronome_bpm == 80


def test_extra_unknown_keys_ignored(tmp_path):
    data = {"metronome_bpm": 100, "future_setting": "ignored"}
    _settings_path(tmp_path).write_text(json.dumps(data), encoding="utf-8")
    result = load()
    assert result.metronome_bpm == 100


# ── OSError resilience ────────────────────────────────────────────────────────


def test_save_does_not_raise_on_os_error(tmp_path, monkeypatch):
    """save() must never crash the app even if the write fails."""
    def _bad_write(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(Path, "write_text", _bad_write)
    # Should not raise
    save(AppSettings())
