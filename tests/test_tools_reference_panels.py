"""Pilot tests for the overhauled reference panels and tree sections."""

from rich.text import Text
from textual.widgets import Static, Tree

from guitar_tui.app import GuitarTUI
from guitar_tui.ui.screens.tools import ToolsMode


def _plain(widget: Static) -> str:
    content = widget.content
    return content.plain if isinstance(content, Text) else str(content)


async def _goto_tools(pilot) -> ToolsMode:
    await pilot.press("3")
    await pilot.pause()
    screen = pilot.app.screen
    assert isinstance(screen, ToolsMode)
    return screen


async def test_tree_has_interactive_and_reference_sections():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        tree = screen.query_one("#tools-tree", Tree)
        sections = [str(n.label) for n in tree.root.children]
        assert sections == ["Interactive", "Reference"]
        interactive = [str(n.label) for n in tree.root.children[0].children]
        assert interactive == ["Key View", "Chord View", "Song Analysis", "Metronome"]
        reference = [str(n.label) for n in tree.root.children[1].children]
        assert "Circle of Fifths" in reference
        assert len(reference) == 10


async def test_circle_of_fifths_content():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        circle = _plain(screen.query_one("#circle-panel", Static))
        # All 12 majors and all 12 relative minors appear
        for major in ("C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"):
            assert f" {major} " in f" {circle} " or f" {major}\n" in circle, major
        for minor in ("Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m", "Bbm", "Fm", "Cm", "Gm", "Dm"):
            assert minor in circle, minor
        assert "clockwise adds a sharp" in circle
        # C sits at 12 o'clock: first key row contains only C
        rows = [r for r in circle.split("\n") if r.strip()]
        top_key_row = next(r for r in rows if r.strip() not in ("Circle of Fifths",) and "─" not in r)
        assert top_key_row.strip() == "C"


async def test_intervals_panel_uses_lesson_symbols():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        intervals = _plain(screen.query_one("#intervals-panel", Static))
        assert "P4" not in intervals and "P5" not in intervals and "P8" not in intervals
        assert "Perfect 4th" in intervals
        assert "Tritone" in intervals
        assert "Symbols match the Intervals lesson" in intervals


async def test_formulas_panel_grouped():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        formulas = _plain(screen.query_one("#formulas-panel", Static))
        for group in ("Triads", "Sevenths", "Sus / Add", "Power"):
            assert group in formulas, group
        assert "1 – b3 – b5" in formulas  # dim formula intact
        assert formulas.index("Triads") < formulas.index("Sevenths") < formulas.index("Power")


async def test_diatonic_panel_has_legend_and_all_keys():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        diatonic = _plain(screen.query_one("#diatonic-all-keys-panel", Static))
        assert "major · minor · diminished" in diatonic
        for key in ("C", "G", "F#", "Db"):
            assert f"\n  {key} " in diatonic, key


async def test_notes_panel_has_legend():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        notes = _plain(screen.query_one("#notes-panel", Static))
        assert "inlay frets" in notes
        assert "accidentals dimmed" in notes


async def test_theme_toggle_rebuilds_panels():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        before = _plain(screen.query_one("#circle-panel", Static))
        dark = pilot.app.current_theme.dark
        pilot.app.theme = "textual-light" if dark else "textual-dark"
        await pilot.pause()
        after = _plain(screen.query_one("#circle-panel", Static))
        # Same content, restyled — the rebuild must not corrupt the panel
        assert after == before
