"""Pilot tests for the song analysis worksheet in the Practice screen."""

from textual.widgets import Static, Tree

from guitar_tui.app import GuitarTUI
from guitar_tui.ui.screens.practice import PracticeMode


async def _goto_practice(pilot) -> PracticeMode:
    await pilot.press("4")
    await pilot.pause()
    screen = pilot.app.screen
    assert isinstance(screen, PracticeMode)
    return screen


async def test_practice_tree_has_worksheet_leaf():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_practice(pilot)
        tree = screen.query_one("#practice-tree", Tree)
        labels = [str(n.label) for n in tree.root.children]
        assert "Worksheet" in labels
        # Sits between Introduction and the Exercises/Licks branches
        assert labels.index("Worksheet") == labels.index("Introduction") + 1


async def test_worksheet_renders_template():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_practice(pilot)
        screen._show_worksheet()
        await pilot.pause()
        body = screen.query_one("#practice-body")
        text = str(body.children[0].content)
        assert "SONG ANALYSIS WORKSHEET" in text
        # The Four Questions, in order
        for prompt in ("TONAL CENTER", "QUALITY", "CHORDS", "SCALE"):
            assert prompt in text, prompt
        idx = [text.index(p) for p in ("TONAL CENTER", "QUALITY", "CHORDS", "SCALE")]
        assert idx == sorted(idx)
        assert "repeat the section block" in text
        # Template dominates: fill-in blanks far outnumber prose lines
        assert text.count("____") > 15
