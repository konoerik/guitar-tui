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
