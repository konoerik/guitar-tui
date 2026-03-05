"""Tests for the M3 lesson loader — LessonLoader, LessonMeta, body parsing."""

import textwrap
import warnings
from pathlib import Path

import pytest
from rich.text import Text

from guitar_tui.loaders.lesson_loader import (
    DiagramBlock,
    LessonLoadError,
    LessonLoader,
    ParsedLesson,
    TextBlock,
)


# ── helpers ────────────────────────────────────────────────────────────────────


def write_lesson(directory: Path, slug: str, content: str) -> Path:
    """Write a lesson .md file to *directory* and return the path."""
    path = directory / f"{slug}.md"
    path.write_text(content, encoding="utf-8")
    return path


def minimal_lesson(
    slug: str,
    *,
    title: str = "Test Lesson",
    difficulty: str = "beginner",
    tags: list[str] | None = None,
    body: str = "Body text.",
) -> str:
    tags_line = str(tags or ["chords"])
    # Build without textwrap.dedent — body may contain lines starting at col 0
    # (e.g. diagram blocks) which would prevent dedent from finding a common prefix
    # and leave the frontmatter '---' markers indented, breaking python-frontmatter.
    return (
        f"---\n"
        f"title: {title}\n"
        f"slug: {slug}\n"
        f"difficulty: {difficulty}\n"
        f"tags: {tags_line}\n"
        f"---\n"
        f"\n"
        f"{body}\n"
    )


# ── loading real lesson files ──────────────────────────────────────────────────


class TestLoadRealLessons:
    def test_load_succeeds(self) -> None:
        loader = LessonLoader()
        loader.load()

    def test_lessons_populated(self) -> None:
        loader = LessonLoader()
        loader.load()
        assert len(loader.lessons) >= 2

    def test_open_g_chord_present(self) -> None:
        loader = LessonLoader()
        loader.load()
        assert "open_g_chord" in loader.lessons

    def test_minor_pentatonic_intro_present(self) -> None:
        loader = LessonLoader()
        loader.load()
        assert "minor_pentatonic_intro" in loader.lessons

    def test_open_g_chord_meta(self) -> None:
        loader = LessonLoader()
        loader.load()
        meta = loader.lessons["open_g_chord"].meta
        assert meta.title == "The Open G Major Chord"
        assert meta.difficulty == "beginner"
        assert "chords" in meta.tags

    def test_minor_pentatonic_meta(self) -> None:
        loader = LessonLoader()
        loader.load()
        meta = loader.lessons["minor_pentatonic_intro"].meta
        assert meta.difficulty == "intermediate"
        assert meta.prerequisites == ["reading_scale_diagrams", "open_g_chord"]

    def test_lesson_has_text_block(self) -> None:
        loader = LessonLoader()
        loader.load()
        lesson = loader.lessons["open_g_chord"]
        text_blocks = [s for s in lesson.body if isinstance(s, TextBlock)]
        assert len(text_blocks) >= 1

    def test_lesson_has_diagram_block(self) -> None:
        loader = LessonLoader()
        loader.load()
        lesson = loader.lessons["open_g_chord"]
        diagram_blocks = [s for s in lesson.body if isinstance(s, DiagramBlock)]
        assert len(diagram_blocks) >= 1

    def test_diagram_rendered_is_rich_text(self) -> None:
        loader = LessonLoader()
        loader.load()
        lesson = loader.lessons["open_g_chord"]
        diagram = next(s for s in lesson.body if isinstance(s, DiagramBlock))
        assert isinstance(diagram.rendered, Text)

    def test_source_path_set(self) -> None:
        loader = LessonLoader()
        loader.load()
        lesson = loader.lessons["open_g_chord"]
        assert lesson.source_path.name == "open_g_chord.md"
        assert lesson.source_path.exists()

    def test_parsed_lesson_type(self) -> None:
        loader = LessonLoader()
        loader.load()
        lesson = loader.lessons["open_g_chord"]
        assert isinstance(lesson, ParsedLesson)


# ── empty lessons directory ────────────────────────────────────────────────────


class TestEmptyLessonsDir:
    def test_empty_dir_is_not_error(self, tmp_path: Path) -> None:
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()  # must not raise
        assert loader.lessons == {}


# ── body parsing ───────────────────────────────────────────────────────────────


class TestBodyParsing:
    def test_text_only_lesson(self, tmp_path: Path) -> None:
        write_lesson(tmp_path, "text_only", minimal_lesson("text_only"))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        lesson = loader.lessons["text_only"]
        assert all(isinstance(s, TextBlock) for s in lesson.body)
        assert len(lesson.body) == 1

    def test_text_block_content(self, tmp_path: Path) -> None:
        write_lesson(
            tmp_path, "text_content", minimal_lesson("text_content", body="## Heading\n\nParagraph.")
        )
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        block = loader.lessons["text_content"].body[0]
        assert isinstance(block, TextBlock)
        assert "Heading" in block.content

    def test_single_diagram_parsed(self, tmp_path: Path) -> None:
        body = textwrap.dedent("""\
            Intro.

            ```diagram
            type: chord
            title: G Major
            frets: [3, 2, 0, 0, 0, 3]
            fingers: [2, 1, null, null, null, 3]
            ```

            Outro.
        """)
        write_lesson(tmp_path, "with_diagram", minimal_lesson("with_diagram", body=body))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        lesson = loader.lessons["with_diagram"]
        diagrams = [s for s in lesson.body if isinstance(s, DiagramBlock)]
        assert len(diagrams) == 1

    def test_diagram_has_spec_dict(self, tmp_path: Path) -> None:
        body = textwrap.dedent("""\
            ```diagram
            type: chord
            title: G Major
            frets: [3, 2, 0, 0, 0, 3]
            ```
        """)
        write_lesson(tmp_path, "chord_lesson", minimal_lesson("chord_lesson", body=body))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        diagram = next(
            s for s in loader.lessons["chord_lesson"].body if isinstance(s, DiagramBlock)
        )
        assert diagram.spec["type"] == "chord"

    def test_diagram_has_raw_yaml(self, tmp_path: Path) -> None:
        body = textwrap.dedent("""\
            ```diagram
            type: chord
            title: G Major
            frets: [3, 2, 0, 0, 0, 3]
            ```
        """)
        write_lesson(tmp_path, "raw_yaml_test", minimal_lesson("raw_yaml_test", body=body))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        diagram = next(
            s for s in loader.lessons["raw_yaml_test"].body if isinstance(s, DiagramBlock)
        )
        assert "type: chord" in diagram.raw_yaml

    def test_diagram_rendered_is_text(self, tmp_path: Path) -> None:
        body = textwrap.dedent("""\
            ```diagram
            type: chord
            title: G Major
            frets: [3, 2, 0, 0, 0, 3]
            ```
        """)
        write_lesson(tmp_path, "render_test", minimal_lesson("render_test", body=body))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        diagram = next(
            s for s in loader.lessons["render_test"].body if isinstance(s, DiagramBlock)
        )
        assert isinstance(diagram.rendered, Text)

    def test_multiple_diagrams(self, tmp_path: Path) -> None:
        body = textwrap.dedent("""\
            First diagram:

            ```diagram
            type: chord
            title: G Major
            frets: [3, 2, 0, 0, 0, 3]
            ```

            Second diagram:

            ```diagram
            type: chord
            title: A minor
            frets: [null, 0, 2, 2, 1, 0]
            ```
        """)
        write_lesson(tmp_path, "two_diagrams", minimal_lesson("two_diagrams", body=body))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        lesson = loader.lessons["two_diagrams"]
        diagrams = [s for s in lesson.body if isinstance(s, DiagramBlock)]
        assert len(diagrams) == 2

    def test_interleaved_text_and_diagrams(self, tmp_path: Path) -> None:
        body = textwrap.dedent("""\
            Intro.

            ```diagram
            type: chord
            title: G Major
            frets: [3, 2, 0, 0, 0, 3]
            ```

            Middle text.

            ```diagram
            type: chord
            title: A minor
            frets: [null, 0, 2, 2, 1, 0]
            ```

            Outro.
        """)
        write_lesson(tmp_path, "interleaved", minimal_lesson("interleaved", body=body))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        lesson = loader.lessons["interleaved"]
        texts = [s for s in lesson.body if isinstance(s, TextBlock)]
        diagrams = [s for s in lesson.body if isinstance(s, DiagramBlock)]
        assert len(texts) == 3
        assert len(diagrams) == 2

    def test_scale_diagram_parsed(self, tmp_path: Path) -> None:
        body = textwrap.dedent("""\
            ```diagram
            type: scale
            title: A Minor Pentatonic
            root: A
            fret_range: [5, 8]
            positions:
              - {string: 6, fret: 5, degree: "1", root: true}
              - {string: 6, fret: 8, degree: "b3"}
            ```
        """)
        write_lesson(tmp_path, "scale_lesson", minimal_lesson("scale_lesson", body=body))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        diagram = next(
            s for s in loader.lessons["scale_lesson"].body if isinstance(s, DiagramBlock)
        )
        assert diagram.spec["type"] == "scale"
        assert isinstance(diagram.rendered, Text)


# ── lesson index helpers ───────────────────────────────────────────────────────


class TestLessonIndex:
    def _write_index_fixtures(self, tmp_path: Path) -> LessonLoader:
        write_lesson(tmp_path, "lesson_a", textwrap.dedent("""\
            ---
            title: Lesson A
            slug: lesson_a
            difficulty: beginner
            tags: [chords, open-chords]
            module: basics
            position: 1
            ---
            Body A.
        """))
        write_lesson(tmp_path, "lesson_b", textwrap.dedent("""\
            ---
            title: Lesson B
            slug: lesson_b
            difficulty: intermediate
            tags: [scales]
            module: basics
            position: 2
            ---
            Body B.
        """))
        write_lesson(tmp_path, "lesson_c", textwrap.dedent("""\
            ---
            title: Lesson C
            slug: lesson_c
            difficulty: beginner
            tags: [chords]
            module: advanced_module
            position: 1
            ---
            Body C.
        """))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        return loader

    def test_by_tag_returns_matching(self, tmp_path: Path) -> None:
        loader = self._write_index_fixtures(tmp_path)
        results = loader.by_tag("chords")
        slugs = {l.meta.slug for l in results}
        assert "lesson_a" in slugs
        assert "lesson_c" in slugs
        assert "lesson_b" not in slugs

    def test_by_tag_no_match(self, tmp_path: Path) -> None:
        loader = self._write_index_fixtures(tmp_path)
        assert loader.by_tag("nonexistent") == []

    def test_by_difficulty_beginner(self, tmp_path: Path) -> None:
        loader = self._write_index_fixtures(tmp_path)
        results = loader.by_difficulty("beginner")
        slugs = {l.meta.slug for l in results}
        assert "lesson_a" in slugs
        assert "lesson_c" in slugs
        assert "lesson_b" not in slugs

    def test_by_difficulty_intermediate(self, tmp_path: Path) -> None:
        loader = self._write_index_fixtures(tmp_path)
        results = loader.by_difficulty("intermediate")
        slugs = {l.meta.slug for l in results}
        assert "lesson_b" in slugs
        assert "lesson_a" not in slugs

    def test_by_module_count(self, tmp_path: Path) -> None:
        loader = self._write_index_fixtures(tmp_path)
        results = loader.by_module("basics")
        assert len(results) == 2

    def test_by_module_sorted_by_position(self, tmp_path: Path) -> None:
        loader = self._write_index_fixtures(tmp_path)
        results = loader.by_module("basics")
        positions = [l.meta.position for l in results]
        assert positions == sorted(p for p in positions if p is not None)

    def test_by_module_no_match(self, tmp_path: Path) -> None:
        loader = self._write_index_fixtures(tmp_path)
        assert loader.by_module("nonexistent") == []

    def test_by_module_nulls_last(self, tmp_path: Path) -> None:
        """Lessons without a position sort after positioned ones."""
        self._write_index_fixtures(tmp_path)
        write_lesson(tmp_path, "no_pos", textwrap.dedent("""\
            ---
            title: No Position
            slug: no_pos
            difficulty: beginner
            tags: [chords]
            module: basics
            ---
            Body.
        """))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        results = loader.by_module("basics")
        assert results[-1].meta.slug == "no_pos"


# ── validation errors ──────────────────────────────────────────────────────────


class TestValidationErrors:
    def test_missing_title(self, tmp_path: Path) -> None:
        (tmp_path / "no_title.md").write_text(textwrap.dedent("""\
            ---
            slug: no_title
            difficulty: beginner
            tags: [chords]
            ---
            Body.
        """))
        with pytest.raises(LessonLoadError, match="no_title.md"):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_invalid_difficulty(self, tmp_path: Path) -> None:
        write_lesson(tmp_path, "bad_diff", minimal_lesson("bad_diff", difficulty="expert"))
        with pytest.raises(LessonLoadError):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_empty_tags(self, tmp_path: Path) -> None:
        (tmp_path / "empty_tags.md").write_text(textwrap.dedent("""\
            ---
            title: Empty Tags
            slug: empty_tags
            difficulty: beginner
            tags: []
            ---
            Body.
        """))
        with pytest.raises(LessonLoadError):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_slug_mismatch(self, tmp_path: Path) -> None:
        # File is 'actual_name.md' but frontmatter slug is 'wrong_slug'
        (tmp_path / "actual_name.md").write_text(textwrap.dedent("""\
            ---
            title: Slug Mismatch
            slug: wrong_slug
            difficulty: beginner
            tags: [chords]
            ---
            Body.
        """))
        with pytest.raises(LessonLoadError, match="slug mismatch"):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_invalid_slug_chars(self, tmp_path: Path) -> None:
        # Hyphen not in [a-z0-9_]; slug matches filename so rule 4 passes,
        # but LessonMeta validator rejects the slug format.
        (tmp_path / "bad_slug.md").write_text(textwrap.dedent("""\
            ---
            title: Bad Slug
            slug: bad-slug
            difficulty: beginner
            tags: [chords]
            ---
            Body.
        """))
        with pytest.raises(LessonLoadError):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_malformed_frontmatter_yaml(self, tmp_path: Path) -> None:
        # Unclosed flow sequence in frontmatter → yaml.YAMLError
        (tmp_path / "bad_yaml.md").write_text(
            "---\ntitle: [\nnot: closed\n---\nBody.\n"
        )
        with pytest.raises(LessonLoadError, match="YAML parse error"):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_malformed_diagram_yaml(self, tmp_path: Path) -> None:
        # Colon overload inside diagram block → yaml.YAMLError
        body = "```diagram\nnot: valid: yaml::::\n```\n"
        write_lesson(tmp_path, "bad_diag", minimal_lesson("bad_diag", body=body))
        with pytest.raises(LessonLoadError, match="YAML parse error"):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_invalid_diagram_spec(self, tmp_path: Path) -> None:
        # Valid YAML but fails DiagramSpec discriminated-union validation
        body = textwrap.dedent("""\
            ```diagram
            type: unknown_type
            ```
        """)
        write_lesson(tmp_path, "bad_spec", minimal_lesson("bad_spec", body=body))
        with pytest.raises(LessonLoadError, match="Invalid diagram spec"):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_diagram_not_mapping(self, tmp_path: Path) -> None:
        # Valid YAML but a list instead of a mapping
        body = "```diagram\n- item1\n- item2\n```\n"
        write_lesson(tmp_path, "list_diag", minimal_lesson("list_diag", body=body))
        with pytest.raises(LessonLoadError, match="must be a YAML mapping"):
            LessonLoader(lessons_dir=tmp_path).load()

    def test_two_distinct_lessons_load_fine(self, tmp_path: Path) -> None:
        """Sanity-check: two valid lessons with distinct slugs load without error."""
        write_lesson(tmp_path, "first_lesson", minimal_lesson("first_lesson"))
        write_lesson(tmp_path, "second_lesson", minimal_lesson("second_lesson"))
        loader = LessonLoader(lessons_dir=tmp_path)
        loader.load()
        assert len(loader.lessons) == 2


# ── prerequisite warnings ──────────────────────────────────────────────────────


class TestPrerequisiteWarnings:
    def test_missing_prereq_is_warning_not_error(self, tmp_path: Path) -> None:
        write_lesson(tmp_path, "depends_on_missing", textwrap.dedent("""\
            ---
            title: Depends On Missing
            slug: depends_on_missing
            difficulty: beginner
            tags: [chords]
            prerequisites: [nonexistent_lesson]
            ---
            Body.
        """))
        loader = LessonLoader(lessons_dir=tmp_path)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            loader.load()  # must not raise
        assert any("nonexistent_lesson" in str(warning.message) for warning in w)

    def test_known_prereq_no_warning(self, tmp_path: Path) -> None:
        write_lesson(tmp_path, "prereq_lesson", minimal_lesson("prereq_lesson"))
        write_lesson(tmp_path, "dependent_lesson", textwrap.dedent("""\
            ---
            title: Dependent Lesson
            slug: dependent_lesson
            difficulty: beginner
            tags: [chords]
            prerequisites: [prereq_lesson]
            ---
            Body.
        """))
        loader = LessonLoader(lessons_dir=tmp_path)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            loader.load()
        prereq_warnings = [x for x in w if "prereq_lesson" in str(x.message)]
        assert len(prereq_warnings) == 0

    def test_missing_prereq_lesson_still_loads(self, tmp_path: Path) -> None:
        write_lesson(tmp_path, "orphan", textwrap.dedent("""\
            ---
            title: Orphan
            slug: orphan
            difficulty: beginner
            tags: [chords]
            prerequisites: [ghost_lesson]
            ---
            Body.
        """))
        loader = LessonLoader(lessons_dir=tmp_path)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            loader.load()
        assert "orphan" in loader.lessons
