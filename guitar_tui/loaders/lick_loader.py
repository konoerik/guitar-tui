"""Lick loader — parses lick library Markdown files.

Lick files live in guitar_tui/content/licks/*.md.  Each file follows the same
frontmatter + diagram-block format as lessons, with additional lick-specific
fields (key, scale, backing_chords, category).

Hard errors (LickLoadError) on:
  - YAML parse failures
  - Missing or invalid required fields
  - slug does not match filename stem
  - Duplicate slugs
  - Malformed diagram blocks
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import frontmatter
import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

from guitar_tui.engine.dispatcher import dispatch
from guitar_tui.loaders.lesson_loader import DiagramBlock, TextBlock

_DEFAULT_LICKS_DIR = Path(__file__).parent.parent / "content" / "licks"
_DIAGRAM_BLOCK_RE = re.compile(r"```diagram\n(.*?)```", re.DOTALL)
_SLUG_RE = re.compile(r"^[a-z0-9_]+$")

# Display order for categories in the lick browser
CATEGORY_ORDER = [
    "pentatonic",
    "blues",
    "major",
    "natural_minor",
    "dorian",
    "phrygian",
    "lydian",
    "mixolydian",
]

CATEGORY_LABELS: dict[str, str] = {
    "pentatonic":   "Minor Pentatonic",
    "blues":        "Blues Scale",
    "major":        "Major Pentatonic",
    "natural_minor": "Natural Minor",
    "dorian":       "Dorian",
    "phrygian":     "Phrygian",
    "lydian":       "Lydian",
    "mixolydian":   "Mixolydian",
}


# ── Exception ──────────────────────────────────────────────────────────────────


class LickLoadError(Exception):
    """Hard error loading a lick file."""


# ── Frontmatter model ──────────────────────────────────────────────────────────


class LickMeta(BaseModel):
    """Validated frontmatter for a lick file."""

    # Required
    title: str
    slug: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
    tags: list[str]           # feel/style tags: rock, blues, funk, country, etc.
    key: str                  # root key: "A", "E", "G", "D", etc.
    scale: str                # scale name matching data/scales/*.yaml: "minor_pentatonic", etc.
    backing_chords: list[str] # chord names for the looper strip: ["Am", "G", "F", "E"]
    category: str             # scale family grouping: "pentatonic", "blues", "major", etc.

    # Optional
    backing_progression: str | None = None  # Roman numeral label: "i – bVII – bVI – V"
    position: int | None = None
    summary: str | None = None

    @field_validator("title")
    @classmethod
    def title_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be empty")
        return v

    @field_validator("slug")
    @classmethod
    def slug_valid(cls, v: str) -> str:
        if not _SLUG_RE.match(v):
            raise ValueError(f"slug must match [a-z0-9_]+, got {v!r}")
        return v

    @field_validator("tags")
    @classmethod
    def tags_non_empty(cls, v: list) -> list:
        if not v:
            raise ValueError("tags must have at least one entry")
        return v


# ── Parsed lick ────────────────────────────────────────────────────────────────


@dataclass
class ParsedLick:
    """A fully parsed lick: metadata + ordered body segments."""

    meta: LickMeta
    body: list[TextBlock | DiagramBlock]
    source_path: Path


# ── Loader ─────────────────────────────────────────────────────────────────────


class LickLoader:
    """Loads and parses all lick Markdown files from the licks directory."""

    def __init__(self, licks_dir: Path | None = None) -> None:
        self.licks_dir = licks_dir or _DEFAULT_LICKS_DIR
        self.licks: dict[str, ParsedLick] = {}

    def load(self) -> None:
        """Parse all .md files. Hard errors raise LickLoadError."""
        self.licks = {}
        if not self.licks_dir.exists():
            return
        for path in sorted(self.licks_dir.rglob("*.md")):
            lick = self._parse_file(path)
            slug = lick.meta.slug
            if slug in self.licks:
                raise LickLoadError(
                    f"Duplicate slug {slug!r}: {path.name} and "
                    f"{self.licks[slug].source_path.name}"
                )
            self.licks[slug] = lick

    def by_category(self) -> list[tuple[str, list[ParsedLick]]]:
        """Return licks grouped and ordered by CATEGORY_ORDER, each sorted by position."""
        grouped: dict[str, list[ParsedLick]] = {}
        for lick in self.licks.values():
            grouped.setdefault(lick.meta.category, []).append(lick)

        ordered_cats = [c for c in CATEGORY_ORDER if c in grouped]
        extra_cats = sorted(c for c in grouped if c not in CATEGORY_ORDER)

        result: list[tuple[str, list[ParsedLick]]] = []
        for cat in ordered_cats + extra_cats:
            licks = sorted(
                grouped[cat],
                key=lambda l: (l.meta.position or 9999, l.meta.title),
            )
            label = CATEGORY_LABELS.get(cat, cat.replace("_", " ").title())
            result.append((label, licks))
        return result

    def _parse_file(self, path: Path) -> ParsedLick:
        try:
            raw_text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise LickLoadError(f"Cannot read {path}: {exc}") from exc

        try:
            post = frontmatter.loads(raw_text)
        except yaml.YAMLError as exc:
            raise LickLoadError(
                f"YAML parse error in frontmatter of {path.name}: {exc}"
            ) from exc

        try:
            meta = LickMeta.model_validate(dict(post.metadata))
        except ValidationError as exc:
            raise LickLoadError(
                f"Invalid frontmatter in {path.name}: {exc}"
            ) from exc

        if meta.slug != path.stem:
            raise LickLoadError(
                f"slug mismatch in {path.name}: frontmatter slug is {meta.slug!r}, "
                f"expected {path.stem!r}"
            )

        body = self._parse_body(post.content, source_name=path.name)
        return ParsedLick(meta=meta, body=body, source_path=path)

    def _parse_body(
        self, body_text: str, *, source_name: str
    ) -> list[TextBlock | DiagramBlock]:
        parts = _DIAGRAM_BLOCK_RE.split(body_text)
        result: list[TextBlock | DiagramBlock] = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                stripped = part.strip()
                if stripped:
                    result.append(TextBlock(content=stripped))
            else:
                try:
                    spec_dict = yaml.safe_load(part)
                except yaml.YAMLError as exc:
                    raise LickLoadError(
                        f"YAML parse error in diagram block in {source_name}: {exc}"
                    ) from exc
                if not isinstance(spec_dict, dict):
                    raise LickLoadError(
                        f"Diagram block in {source_name} must be a YAML mapping"
                    )
                try:
                    rendered = dispatch(spec_dict)
                except ValidationError as exc:
                    raise LickLoadError(
                        f"Invalid diagram spec in {source_name}: {exc}"
                    ) from exc
                result.append(
                    DiagramBlock(raw_yaml=part, spec=spec_dict, rendered=rendered)
                )
        return result
