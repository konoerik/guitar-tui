"""Smoke tests for the M4 TUI application."""

from guitar_tui.app import GuitarTUI
from textual.widgets import ListView


async def test_app_mounts_without_crash():
    async with GuitarTUI().run_test() as pilot:
        assert type(pilot.app.screen).__name__ == "HomeScreen"


async def test_lesson_list_has_items():
    async with GuitarTUI().run_test() as pilot:
        # query_one on the active screen (HomeScreen), not the base app screen
        lv = pilot.app.screen.query_one("#lesson-list", ListView)
        assert len(lv.children) >= 1


async def test_navigate_to_lesson_and_back():
    async with GuitarTUI().run_test() as pilot:
        # Focus lesson list via binding, navigate to first item, select it
        lv = pilot.app.screen.query_one("#lesson-list", ListView)
        lv.focus()
        await pilot.press("down")   # highlight first item
        await pilot.press("enter")  # emit ListView.Selected
        assert type(pilot.app.screen).__name__ == "LessonScreen"
        await pilot.press("escape")
        assert type(pilot.app.screen).__name__ == "HomeScreen"
