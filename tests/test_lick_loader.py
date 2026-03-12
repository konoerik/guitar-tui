"""Tests for the lick loader."""

import textwrap
from pathlib import Path

import pytest

from guitar_tui.loaders.lick_loader import (
    LickLoadError,
    LickLoader,
    LickMeta,
    ParsedLick,
)
from guitar_tui.loaders.lesson_loader import DiagramBlock, TextBlock


# ── Helpers ────────────────────────────────────────────────────────────────────

_REQUIRED = {
    "title": "Test Lick",
    "slug": "test_lick",
    "difficulty": "beginner",
    "tags": ["rock"],
    "key": "A",
    "scale": "minor_pentatonic",
    "backing_chords": ["Am", "G"],
    "category": "pentatonic",
}


def _write_lick(tmp_path: Path, name: str, frontmatter: dict, body: str = "") -> Path:
    import yaml

    fm = yaml.dump(frontmatter, allow_unicode=True)
    content = f"---\n{fm}---\n\n{body}"
    p = tmp_path / f"{name}.md"
    p.write_text(content, encoding="utf-8")
    return p


def _make_loader(tmp_path: Path) -> LickLoader:
    loader = LickLoader(licks_dir=tmp_path)
    loader.load()
    return loader


# ── Basic loading ──────────────────────────────────────────────────────────────


def test_loads_real_licks():
    loader = LickLoader()
    loader.load()
    assert len(loader.licks) > 0


def test_real_lick_slugs_match_filenames():
    loader = LickLoader()
    loader.load()
    for slug, lick in loader.licks.items():
        assert slug == lick.meta.slug
        assert slug == lick.source_path.stem


def test_lick_meta_fields_present():
    loader = LickLoader()
    loader.load()
    for lick in loader.licks.values():
        assert lick.meta.title
        assert lick.meta.slug
        assert lick.meta.key
        assert lick.meta.scale
        assert lick.meta.backing_chords
        assert lick.meta.category
        assert lick.meta.tags


# ── Body parsing ───────────────────────────────────────────────────────────────


def test_plain_text_body(tmp_path):
    _write_lick(tmp_path, "test_lick", _REQUIRED, body="Some lick description.")
    loader = _make_loader(tmp_path)
    lick = loader.licks["test_lick"]
    assert len(lick.body) == 1
    assert isinstance(lick.body[0], TextBlock)
    assert "Some lick description" in lick.body[0].content


def test_diagram_block_in_body(tmp_path):
    body = textwrap.dedent("""\
        Intro text.

        ```diagram
        type: scale
        title: Test Scale
        root: A
        fret_range: [5, 8]
        positions:
          - {string: 6, fret: 5, degree: "1", root: true}
        ```

        Outro text.
    """)
    _write_lick(tmp_path, "test_lick", _REQUIRED, body=body)
    loader = _make_loader(tmp_path)
    lick = loader.licks["test_lick"]
    types = [type(b) for b in lick.body]
    assert TextBlock in types
    assert DiagramBlock in types


def test_empty_body(tmp_path):
    _write_lick(tmp_path, "test_lick", _REQUIRED, body="")
    loader = _make_loader(tmp_path)
    assert loader.licks["test_lick"].body == []


# ── Validation errors ──────────────────────────────────────────────────────────


def test_missing_required_field_raises(tmp_path):
    bad = {k: v for k, v in _REQUIRED.items() if k != "title"}
    _write_lick(tmp_path, "test_lick", bad)
    with pytest.raises(LickLoadError, match="Invalid frontmatter"):
        _make_loader(tmp_path)


def test_invalid_difficulty_raises(tmp_path):
    bad = {**_REQUIRED, "difficulty": "expert"}
    _write_lick(tmp_path, "test_lick", bad)
    with pytest.raises(LickLoadError, match="Invalid frontmatter"):
        _make_loader(tmp_path)


def test_slug_mismatch_raises(tmp_path):
    bad = {**_REQUIRED, "slug": "wrong_slug"}
    _write_lick(tmp_path, "test_lick", bad)
    with pytest.raises(LickLoadError, match="slug mismatch"):
        _make_loader(tmp_path)


def test_invalid_slug_chars_raises(tmp_path):
    bad = {**_REQUIRED, "slug": "test-lick"}
    _write_lick(tmp_path, "test-lick", bad)
    with pytest.raises(LickLoadError, match="Invalid frontmatter"):
        _make_loader(tmp_path)


def test_empty_tags_raises(tmp_path):
    bad = {**_REQUIRED, "tags": []}
    _write_lick(tmp_path, "test_lick", bad)
    with pytest.raises(LickLoadError, match="Invalid frontmatter"):
        _make_loader(tmp_path)


def test_duplicate_slug_raises(tmp_path):
    _write_lick(tmp_path, "test_lick", _REQUIRED)
    subdir = tmp_path / "sub"
    subdir.mkdir()
    _write_lick(subdir, "test_lick", _REQUIRED)
    with pytest.raises(LickLoadError, match="Duplicate slug"):
        _make_loader(tmp_path)


def test_invalid_diagram_raises(tmp_path):
    body = textwrap.dedent("""\
        ```diagram
        type: chord
        title: Bad
        frets: [not, valid, data]
        ```
    """)
    _write_lick(tmp_path, "test_lick", _REQUIRED, body=body)
    with pytest.raises(LickLoadError):
        _make_loader(tmp_path)


# ── by_category ────────────────────────────────────────────────────────────────


def test_by_category_groups_correctly():
    loader = LickLoader()
    loader.load()
    grouped = loader.by_category()
    assert len(grouped) > 0
    for label, licks in grouped:
        assert isinstance(label, str)
        assert len(licks) > 0
        # All licks in a group share the same category
        categories = {l.meta.category for l in licks}
        assert len(categories) == 1


def test_by_category_respects_position_order():
    loader = LickLoader()
    loader.load()
    for _label, licks in loader.by_category():
        positions = [
            l.meta.position if l.meta.position is not None else 9999
            for l in licks
        ]
        assert positions == sorted(positions)


def test_missing_licks_dir_loads_empty(tmp_path):
    loader = LickLoader(licks_dir=tmp_path / "nonexistent")
    loader.load()
    assert loader.licks == {}
