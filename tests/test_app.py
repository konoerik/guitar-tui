"""Smoke tests for the TUI application."""

from guitar_tui.app import GuitarTUI
from guitar_tui.ui.screens.welcome import WelcomeScreen
from guitar_tui.ui.screens.lesson import LessonMode


async def test_app_mounts_without_crash():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        assert isinstance(pilot.app.screen, WelcomeScreen)


async def test_mode_switching():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        await pilot.press("2")
        assert isinstance(pilot.app.screen, LessonMode)
        await pilot.press("1")
        assert isinstance(pilot.app.screen, WelcomeScreen)


async def test_lesson_loads_into_body():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        from textual.containers import ScrollableContainer

        await pilot.press("2")
        assert isinstance(pilot.app.screen, LessonMode)

        lessons = list(pilot.app.lesson_loader.lessons.values())
        assert lessons, "No lessons loaded"

        lesson_mode: LessonMode = pilot.app.screen  # type: ignore[assignment]
        await lesson_mode._load_lesson(lessons[0])
        await pilot.pause()

        body = lesson_mode.query_one("#lesson-body", ScrollableContainer)
        assert body.children, "Lesson body should be populated after _load_lesson"


async def test_first_run_shows_introduction(tmp_path, monkeypatch):
    """With no settings file, the Lessons screen opens on the overview."""
    monkeypatch.setenv("GUITAR_TUI_CONFIG_DIR", str(tmp_path))
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        await pilot.press("2")
        screen: LessonMode = pilot.app.screen  # type: ignore[assignment]
        assert screen._current_slug is None
        assert str(screen.query_one("#lessons-content").border_title) == "Lessons"


async def test_restored_lesson_syncs_tree(tmp_path, monkeypatch):
    """Resuming a saved lesson expands its track and puts the cursor on it."""
    from textual.widgets import Tree

    monkeypatch.setenv("GUITAR_TUI_CONFIG_DIR", str(tmp_path))
    (tmp_path / "settings.json").write_text('{"last_lesson": "minor_pentatonic_intro"}')
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        await pilot.press("2")
        screen: LessonMode = pilot.app.screen  # type: ignore[assignment]
        assert screen._current_slug == "minor_pentatonic_intro"
        tree = screen.query_one("#lessons-tree", Tree)
        node = tree.cursor_node
        assert node is not None and node.data == "minor_pentatonic_intro"
        assert node.parent is not None and node.parent.is_expanded


async def test_reference_track_unnumbered_in_tree():
    """Equipment renders under a Reference header, not as a numbered track."""
    from textual.widgets import Tree

    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        await pilot.press("2")
        screen: LessonMode = pilot.app.screen  # type: ignore[assignment]
        tree = screen.query_one("#lessons-tree", Tree)
        labels = [str(node.label) for node in tree.root.children]
        assert "Reference" in labels
        assert "Your Equipment" in labels
        numbered = [l for l in labels if l[:2].isdigit()]
        assert numbered, "Curriculum tracks should be numbered"
        assert not any("Equipment" in l for l in numbered)
        # Reference section comes after the numbered tracks
        assert labels.index("Reference") > labels.index(numbered[-1])


async def test_reference_lesson_hides_practice_tabs_and_progress():
    """Reference lessons show no [pos / total] and no Exercises/Licks tabs."""
    from textual.widgets import TabbedContent

    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        await pilot.press("2")
        screen: LessonMode = pilot.app.screen  # type: ignore[assignment]
        lesson = pilot.app.lesson_loader.lessons["amp_basics"]
        await screen._load_lesson(lesson)
        await pilot.pause()
        assert str(screen.query_one("#lessons-content").border_title) == "Amplifier Basics"
        tabs = screen.query_one("#lesson-tabs", TabbedContent)
        assert not tabs.get_tab("tab-drills").display
        assert not tabs.get_tab("tab-licks").display
