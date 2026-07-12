"""Pilot tests for the Chord View: voicings, key functions, Theory Web navigation."""

from rich.text import Text
from textual.widgets import ContentSwitcher, OptionList, Select, Static

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


def _current_pane(screen: ToolsMode) -> str:
    return screen.query_one("#tools-switcher", ContentSwitcher).current or ""


def _open_chord_view(screen: ToolsMode, chord: str) -> None:
    screen._switch_pane("content-chord-view")
    screen.query_one("#chord-select", Select).value = chord


# ── Content ────────────────────────────────────────────────────────────────────


async def test_chord_view_shows_all_voicings():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _open_chord_view(screen, "F")
        await pilot.pause()
        voicings = _plain(screen.query_one("#chord-voicings", Static))
        # F has 3 voicings, rendered side by side with their labels
        assert "E-shape barre (1st fret)" in voicings
        assert "A-shape barre (8th fret)" in voicings
        assert "Default" in voicings
        # Three diagrams side by side: nut/grid rows are wider than one diagram
        grid_rows = [l for l in voicings.split("\n") if "┌" in l or "├" in l]
        assert grid_rows and all(len(r) > 60 for r in grid_rows)


async def test_chord_view_header_spells_tones():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _open_chord_view(screen, "Cmaj7")
        await pilot.pause()
        header = _plain(screen.query_one("#chord-header", Static))
        assert "Cmaj7" in header
        assert "C · E · G · B" in header


async def test_chord_view_lists_key_functions():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _open_chord_view(screen, "Am")
        await pilot.pause()
        assert ("C", "Major", "vi") in screen._membership_targets
        assert ("A", "Minor", "i") in screen._membership_targets
        assert len(screen._membership_targets) == 6
        options = screen.query_one("#chord-memberships", OptionList)
        assert options.option_count == 6


async def test_non_diatonic_chord_shows_no_functions():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _open_chord_view(screen, "Asus4")
        await pilot.pause()
        title = _plain(screen.query_one("#chord-functions-title", Static))
        assert "not a diatonic triad" in title
        assert screen._membership_targets == []


async def test_chord_view_shows_tagged_lessons():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _open_chord_view(screen, "Am")
        await pilot.pause()
        lessons = _plain(screen.query_one("#chord-lessons", Static))
        assert "Lessons:" in lessons  # open_am_chord is tagged chord:Am


# ── Theory Web navigation ──────────────────────────────────────────────────────


async def test_membership_enter_jumps_to_key_view():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _open_chord_view(screen, "Am")
        await pilot.pause()
        options = screen.query_one("#chord-memberships", OptionList)
        options.focus()
        await pilot.pause()
        # First membership is vi in C Major (Major keys listed first)
        target = screen._membership_targets[0]
        await pilot.press("enter")
        await pilot.pause()
        assert _current_pane(screen) == "content-key-view"
        assert screen._key() == target[0]
        assert screen._quality() == target[1]
        # Chord strip lands on Am's slot
        roman, chord = screen._chords[screen._chord_idx]
        assert chord == "Am"
        assert roman == target[2]


async def test_backspace_returns_to_chord_view():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _open_chord_view(screen, "Dm")
        await pilot.pause()
        options = screen.query_one("#chord-memberships", OptionList)
        options.focus()
        await pilot.press("enter")
        await pilot.pause()
        assert _current_pane(screen) == "content-key-view"
        await pilot.press("backspace")
        await pilot.pause()
        assert _current_pane(screen) == "content-chord-view"
        assert screen._chord_view_name() == "Dm"
        assert screen._history == []


async def test_g_opens_key_view_chord_in_chord_view():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        # Default Key View: A Minor, chord idx 0 = Am
        assert _current_pane(screen) == "content-key-view"
        await pilot.press("g")
        await pilot.pause()
        assert _current_pane(screen) == "content-chord-view"
        assert screen._chord_view_name() == "Am"


async def test_back_restores_key_view_state():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        # Set up a non-default Key View state
        screen.query_one("#key-select", Select).value = "E"
        screen.query_one("#quality-select", Select).value = "Major"
        await pilot.pause()
        await pilot.press("full_stop")  # chord idx 1
        await pilot.press("]")          # position 2
        await pilot.press("g")          # jump to chord view
        await pilot.pause()
        assert _current_pane(screen) == "content-chord-view"
        await pilot.press("backspace")
        await pilot.pause()
        assert _current_pane(screen) == "content-key-view"
        assert screen._key() == "E"
        assert screen._quality() == "Major"
        assert screen._chord_idx == 1
        assert screen._position == 2


async def test_back_with_empty_history_is_noop():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        pane_before = _current_pane(screen)
        await pilot.press("backspace")
        await pilot.pause()
        assert _current_pane(screen) == pane_before
