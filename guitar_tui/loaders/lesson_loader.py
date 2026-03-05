"""Lesson loader — parses Markdown+YAML frontmatter lesson files.

Lesson files live in guitar_tui/content/lessons/*.md.  Each file has a YAML
frontmatter block (delimited by '---') followed by a Markdown body that may
contain fenced ```diagram blocks.

Startup failure (LessonLoadError) is intentional for hard rule violations.
Missing prerequisite slugs emit warnings only — see lesson_format.md rule 6.
"""

import re
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import frontmatter
import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator
from rich.text import Text

from guitar_tui.engine.dispatcher import dispatch

_DEFAULT_LESSONS_DIR = Path(__file__).parent.parent / "content" / "lessons"

# Matches a fenced ```diagram ... ``` block.  One capturing group returns the
# YAML body.  re.split() with a single capturing group interleaves text/yaml.
_DIAGRAM_BLOCK_RE = re.compile(r"```diagram\n(.*?)```", re.DOTALL)

_SLUG_RE = re.compile(r"^[a-z0-9_]+$")


# ── Exception ──────────────────────────────────────────────────────────────────


class LessonLoadError(Exception):
    """Raised when a lesson file is missing, malformed, or fails validation.

    Hard error conditions (per lesson_format.md):
      - Frontmatter fails YAML parsing
      - Required fields (title, slug, difficulty, tags) missing or invalid
      - difficulty not in allowed set
      - slug does not match filename (without .md)
      - duplicate slug across lesson files
      - tags list is empty
      - diagram block YAML is malformed or fails DiagramSpec validation
    """


# ── Frontmatter Pydantic model ─────────────────────────────────────────────────


class LessonMeta(BaseModel):
    """Validated frontmatter for a lesson file."""

    # Required
    title: str
    slug: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
    tags: list[str]

    # Optional
    prerequisites: list[str] = Field(default_factory=list)
    module: str | None = None
    position: int | None = None
    summary: str | None = None
    version: int = 1

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


# ── Body segment types ─────────────────────────────────────────────────────────


@dataclass
class TextBlock:
    """A segment of plain Markdown text from the lesson body."""

    content: str  # stripped raw Markdown


@dataclass
class DiagramBlock:
    """A parsed and engine-rendered diagram block."""

    raw_yaml: str   # original YAML source inside the fenced block
    spec: dict      # parsed dict (for M4 inspection / re-rendering)
    rendered: Text  # Rich Text output from engine.dispatch()


@dataclass
class ParsedLesson:
    """A fully parsed lesson: metadata + ordered body segments."""

    meta: LessonMeta
    body: list[TextBlock | DiagramBlock]
    source_path: Path  # absolute path to the .md file


# ── Loader ─────────────────────────────────────────────────────────────────────


class LessonLoader:
    """Loads and parses all lesson Markdown files from the lessons directory.

    Usage::

        loader = LessonLoader()
        loader.load()           # raises LessonLoadError on hard errors
        lesson = loader.lessons["open_g_chord"]
        beginners = loader.by_difficulty("beginner")
        chords = loader.by_tag("chords")
    """

    def __init__(self, lessons_dir: Path | None = None) -> None:
        self.lessons_dir = lessons_dir or _DEFAULT_LESSONS_DIR
        self.lessons: dict[str, ParsedLesson] = {}  # keyed by slug

    def load(self) -> None:
        """Parse all .md files in lessons_dir.

        Hard errors raise LessonLoadError immediately.
        Missing prerequisite slugs emit Python warnings after all files load.
        An empty lessons_dir is not an error.
        """
        self.lessons = {}
        md_files = sorted(self.lessons_dir.rglob("*.md"))

        # Phase 1: parse all files
        for path in md_files:
            lesson = self._parse_file(path)
            slug = lesson.meta.slug
            if slug in self.lessons:
                raise LessonLoadError(
                    f"Duplicate slug {slug!r}: found in {path.name} "
                    f"and {self.lessons[slug].source_path.name}"
                )
            self.lessons[slug] = lesson

        # Phase 2: warn on missing prerequisites (all slugs now known)
        known = set(self.lessons)
        for lesson in self.lessons.values():
            for prereq in lesson.meta.prerequisites:
                if prereq not in known:
                    warnings.warn(
                        f"Lesson {lesson.meta.slug!r} lists prerequisite "
                        f"{prereq!r} which does not exist.",
                        stacklevel=2,
                    )

    # ── Index helpers ──────────────────────────────────────────────────────────

    def by_tag(self, tag: str) -> list[ParsedLesson]:
        """Return all lessons that include *tag* in their tags list."""
        return [l for l in self.lessons.values() if tag in l.meta.tags]

    def by_difficulty(self, difficulty: str) -> list[ParsedLesson]:
        """Return all lessons with the given difficulty level."""
        return [l for l in self.lessons.values() if l.meta.difficulty == difficulty]

    def by_module(self, module: str) -> list[ParsedLesson]:
        """Return all lessons in *module*, sorted by position (nulls last)."""
        matches = [l for l in self.lessons.values() if l.meta.module == module]
        return sorted(
            matches,
            key=lambda l: (l.meta.position is None, l.meta.position or 0),
        )

    # ── Private ────────────────────────────────────────────────────────────────

    def _parse_file(self, path: Path) -> ParsedLesson:
        """Parse a single lesson file into a ParsedLesson."""
        try:
            raw_text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise LessonLoadError(f"Cannot read {path}: {exc}") from exc

        # Parse frontmatter (python-frontmatter delegates to yaml.safe_load)
        try:
            post = frontmatter.loads(raw_text)
        except yaml.YAMLError as exc:
            raise LessonLoadError(
                f"YAML parse error in frontmatter of {path.name}: {exc}"
            ) from exc

        # Validate frontmatter fields
        try:
            meta = LessonMeta.model_validate(dict(post.metadata))
        except ValidationError as exc:
            raise LessonLoadError(
                f"Invalid frontmatter in {path.name}: {exc}"
            ) from exc

        # slug must match filename (rule 4)
        expected = path.stem
        if meta.slug != expected:
            raise LessonLoadError(
                f"slug mismatch in {path.name}: frontmatter slug is {meta.slug!r}, "
                f"expected {expected!r} to match filename"
            )

        body = self._parse_body(post.content, source_name=path.name)
        return ParsedLesson(meta=meta, body=body, source_path=path)

    def _parse_body(
        self, body_text: str, *, source_name: str
    ) -> list[TextBlock | DiagramBlock]:
        """Split the lesson body into alternating TextBlock / DiagramBlock segments.

        Uses re.split() with a single capturing group so even-indexed parts are
        text and odd-indexed parts are diagram YAML strings.
        """
        parts = _DIAGRAM_BLOCK_RE.split(body_text)
        result: list[TextBlock | DiagramBlock] = []

        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Text segment — skip if empty after stripping
                stripped = part.strip()
                if stripped:
                    result.append(TextBlock(content=stripped))
            else:
                # Diagram YAML
                try:
                    spec_dict = yaml.safe_load(part)
                except yaml.YAMLError as exc:
                    raise LessonLoadError(
                        f"YAML parse error in diagram block in {source_name}: {exc}"
                    ) from exc

                if not isinstance(spec_dict, dict):
                    raise LessonLoadError(
                        f"Diagram block in {source_name} must be a YAML mapping, "
                        f"got {type(spec_dict).__name__}"
                    )

                try:
                    rendered = dispatch(spec_dict)
                except ValidationError as exc:
                    raise LessonLoadError(
                        f"Invalid diagram spec in {source_name}: {exc}"
                    ) from exc

                result.append(
                    DiagramBlock(raw_yaml=part, spec=spec_dict, rendered=rendered)
                )

        return result
