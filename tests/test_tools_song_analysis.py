"""Pilot tests for the Song Analysis workflow: report content + Theory Web links."""

from rich.text import Text
from textual.widgets import ContentSwitcher, OptionList, Select, Static

from guitar_tui.app import GuitarTUI
from guitar_tui.ui.screens.tools import ToolsMode


def _plain(widget: Static) -> str:
    content = widget.content
    return content.plain if isinstance(content, Text) else str(content)


async def _goto_song_analysis(pilot) -> ToolsMode:
    await pilot.press("3")
    await pilot.pause()
    screen = pilot.app.screen
    assert isinstance(screen, ToolsMode)
    screen._switch_pane("content-song-analysis")
    await pilot.pause()
    return screen


def _current_pane(screen: ToolsMode) -> str:
    return screen.query_one("#tools-switcher", ContentSwitcher).current or ""


async def test_report_covers_all_sections_default_a_minor():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_song_analysis(pilot)
        report = _plain(screen.query_one("#song-report", Static))
        assert "A song in A Minor" in report
        assert "A Natural Minor" in report
        assert "Positions" in report and "frets" in report
        assert "relative major C" in report
        assert "i: Am" in report and "bVII: G" in report
        assert "i–bVI–bIII–bVII" in report and "Am  F  C  G" in report
        assert "Lessons" in report


async def test_report_transposes_positions():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_song_analysis(pilot)
        screen.query_one("#song-key-select", Select).value = "C"
        screen.query_one("#song-quality-select", Select).value = "Major"
        await pilot.pause()
        report = _plain(screen.query_one("#song-report", Static))
        assert "A song in C Major" in report
        assert "C Major" in report
        assert "relative minor Am" in report
        assert "I: C" in report and "V: G" in report
        assert "C  G  Am  F" in report  # I–V–vi–IV realized in C


async def test_report_handles_no_chord_scale():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_song_analysis(pilot)
        screen.query_one("#song-quality-select", Select).value = "Whole Tone"
        await pilot.pause()
        report = _plain(screen.query_one("#song-report", Static))
        assert "A song in A Whole Tone" in report
        assert "Chords" not in report        # no diatonic set
        assert "Progressions" not in report  # none defined
        # Only the Key View link remains
        assert screen._song_link_targets == [("content-key-view", None)]


async def test_key_view_link_navigates_with_state():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_song_analysis(pilot)
        screen.query_one("#song-key-select", Select).value = "E"
        await pilot.pause()
        links = screen.query_one("#song-links", OptionList)
        links.focus()
        await pilot.press("enter")  # first link = Open in Key View
        await pilot.pause()
        assert _current_pane(screen) == "content-key-view"
        assert screen._key() == "E"
        assert screen._quality() == "Minor"


async def test_chord_link_navigates_to_chord_view():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_song_analysis(pilot)
        links = screen.query_one("#song-links", OptionList)
        # Second link is the first diatonic chord with a voicing (Am for A Minor)
        assert screen._song_link_targets[1] == ("content-chord-view", "Am")
        links.focus()
        links.highlighted = 1
        await pilot.press("enter")
        await pilot.pause()
        assert _current_pane(screen) == "content-chord-view"
        assert screen._chord_view_name() == "Am"


async def test_back_returns_to_song_analysis():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_song_analysis(pilot)
        screen.query_one("#song-key-select", Select).value = "D"
        await pilot.pause()
        links = screen.query_one("#song-links", OptionList)
        links.focus()
        await pilot.press("enter")
        await pilot.pause()
        assert _current_pane(screen) == "content-key-view"
        await pilot.press("backspace")
        await pilot.pause()
        assert _current_pane(screen) == "content-song-analysis"
        assert screen._song_key() == "D"
        assert screen._song_quality() == "Minor"


async def test_chain_navigation_pops_in_order():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_song_analysis(pilot)
        # Song Analysis → Chord View (Am) → Key View (via membership) → back → back
        links = screen.query_one("#song-links", OptionList)
        links.focus()
        links.highlighted = 1
        await pilot.press("enter")
        await pilot.pause()
        assert _current_pane(screen) == "content-chord-view"
        memberships = screen.query_one("#chord-memberships", OptionList)
        memberships.focus()
        await pilot.press("enter")
        await pilot.pause()
        assert _current_pane(screen) == "content-key-view"
        assert len(screen._history) == 2
        await pilot.press("backspace")
        await pilot.pause()
        assert _current_pane(screen) == "content-chord-view"
        await pilot.press("backspace")
        await pilot.pause()
        assert _current_pane(screen) == "content-song-analysis"
        assert screen._history == []
