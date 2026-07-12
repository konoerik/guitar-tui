"""Pilot tests for the Key View: context line, characteristic note, voicing cycling."""

from rich.text import Text
from textual.widgets import Select, Static

from guitar_tui.app import GuitarTUI
from guitar_tui.ui.screens.tools import ToolsMode
from guitar_tui.ui.widgets.full_neck import FullNeckWidget


def _plain(widget: Static) -> str:
    content = widget.content
    return content.plain if isinstance(content, Text) else str(content)


async def _goto_tools(pilot) -> ToolsMode:
    await pilot.press("3")
    await pilot.pause()
    screen = pilot.app.screen
    assert isinstance(screen, ToolsMode)
    return screen


# ── Context line ───────────────────────────────────────────────────────────────


async def test_context_line_default_a_minor():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        line = _plain(screen.query_one("#key-context", Static))
        assert "A Minor" in line
        assert "relative major C" in line
        assert "0♯" in line


async def test_context_line_updates_on_key_change():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        screen.query_one("#key-select", Select).value = "E"
        await pilot.pause()
        line = _plain(screen.query_one("#key-context", Static))
        assert "E Minor" in line
        assert "relative major G" in line
        assert "1♯" in line


async def test_context_line_mode_shows_parent_major():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        screen.query_one("#key-select", Select).value = "D"
        screen.query_one("#quality-select", Select).value = "Dorian"
        await pilot.pause()
        line = _plain(screen.query_one("#key-context", Static))
        assert "D Dorian" in line
        assert "parent major C" in line


# ── Characteristic note on the neck ────────────────────────────────────────────


async def test_dorian_shows_characteristic_note():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        screen.query_one("#key-select", Select).value = "D"
        screen.query_one("#quality-select", Select).value = "Dorian"
        await pilot.pause()
        neck = screen.query_one("#full-neck", FullNeckWidget)
        assert neck.characteristic == (9, "6")
        rendered = neck._build().plain
        assert "◆" in rendered
        assert "6 (B)" in rendered  # D Dorian's natural 6 is B


async def test_minor_has_no_characteristic_note():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        neck = screen.query_one("#full-neck", FullNeckWidget)
        assert neck.characteristic is None
        assert "◆" not in neck._build().plain


async def test_blues_highlights_flat_five():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        screen.query_one("#quality-select", Select).value = "Blues"
        await pilot.pause()
        neck = screen.query_one("#full-neck", FullNeckWidget)
        assert neck.characteristic == (6, "b5")
        assert "b5 (Eb)" in neck._build().plain  # A blues: b5 = Eb


# ── Voicing cycling ────────────────────────────────────────────────────────────


def _select_chord_with_voicings(screen: ToolsMode, min_voicings: int) -> int:
    """Move the chord strip to the first chord with >= min_voicings; return count."""
    chords = screen.app.data_loader.chords
    for i, (_, name) in enumerate(screen._chords):
        entry = chords.get(name)
        if entry is not None and len(entry.voicings) >= min_voicings:
            screen._chord_idx = i
            screen._voicing_idx = 0
            screen._update_chord_detail()
            return len(entry.voicings)
    raise AssertionError(f"No chord with >= {min_voicings} voicings in strip")


async def test_v_cycles_voicings_and_wraps():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        n = _select_chord_with_voicings(screen, 2)
        detail = screen.query_one("#chord-detail", Static)
        first = _plain(detail)
        assert f"voicing 1/{n}" in first

        await pilot.press("v")
        second = _plain(detail)
        assert f"voicing 2/{n}" in second
        assert second != first

        # Cycling through all voicings wraps back to the first.
        for _ in range(n - 1):
            await pilot.press("v")
        assert f"voicing 1/{n}" in _plain(detail)


async def test_single_voicing_chord_shows_no_cycle_hint():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        chords = screen.app.data_loader.chords
        single = next(
            (i for i, (_, name) in enumerate(screen._chords)
             if (e := chords.get(name)) is not None and len(e.voicings) == 1),
            None,
        )
        if single is None:
            return  # no single-voicing chord in this key — nothing to check
        screen._chord_idx = single
        screen._voicing_idx = 0
        screen._update_chord_detail()
        detail = screen.query_one("#chord-detail", Static)
        before = _plain(detail)
        assert "voicing" not in before
        await pilot.press("v")
        assert _plain(detail) == before


async def test_chord_change_resets_voicing():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        n = _select_chord_with_voicings(screen, 2)
        await pilot.press("v")
        assert f"voicing 2/{n}" in _plain(screen.query_one("#chord-detail", Static))
        await pilot.press("full_stop")  # next chord
        assert screen._voicing_idx == 0


async def test_key_change_resets_voicing():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        _select_chord_with_voicings(screen, 2)
        await pilot.press("v")
        assert screen._voicing_idx == 1
        screen.query_one("#key-select", Select).value = "C"
        await pilot.pause()
        assert screen._voicing_idx == 0


# ── Theory Web: related panel + world scales ───────────────────────────────────


async def test_related_panel_shows_progressions_and_lessons():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        # Default A Minor
        related = _plain(screen.query_one("#key-related", Static))
        assert "Progressions in A Minor" in related
        assert "i–bVI–bIII–bVII" in related
        assert "Am  F  C  G" in related
        assert "Lessons:" in related  # natural minor lessons are tagged


async def test_related_panel_realizes_in_selected_key():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        screen.query_one("#key-select", Select).value = "C"
        screen.query_one("#quality-select", Select).value = "Major"
        await pilot.pause()
        related = _plain(screen.query_one("#key-related", Static))
        assert "Progressions in C Major" in related
        assert "C  G  Am  F" in related  # I–V–vi–IV realized in C


async def test_harmonic_minor_full_wiring():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        screen.query_one("#quality-select", Select).value = "Harmonic Minor"
        await pilot.pause()
        # Chord strip has the raised-7th dominant V
        strip = _plain(screen.query_one("#chord-strip", Static))
        assert "V: E" in strip
        # Neck renders the scale with the characteristic natural 7 marked
        neck = screen.query_one("#full-neck", FullNeckWidget)
        rendered = neck._build().plain
        assert "(scale" not in rendered  # not the "scale not loaded" message
        assert "7 (Ab)" in rendered      # A harmonic minor's 7 is G# (spelled Ab)
        # Related panel realizes the i–V–i cadence
        related = _plain(screen.query_one("#key-related", Static))
        assert "Am  E  Am" in related


async def test_whole_tone_has_no_chord_set():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        screen.query_one("#quality-select", Select).value = "Whole Tone"
        await pilot.pause()
        strip = _plain(screen.query_one("#chord-strip", Static))
        assert "no diatonic chord set" in strip
        assert _plain(screen.query_one("#chord-detail", Static)) == ""
        # Neck still renders (2 symmetric positions)
        neck = screen.query_one("#full-neck", FullNeckWidget)
        assert "position 1 of 2" in neck._build().plain


async def test_all_world_scales_render():
    async with GuitarTUI().run_test(size=(120, 40)) as pilot:
        screen = await _goto_tools(pilot)
        neck = screen.query_one("#full-neck", FullNeckWidget)
        for quality in (
            "Harmonic Minor", "Phrygian Dominant", "Hungarian Minor",
            "Whole Tone", "Diminished (W–H)", "Hirajoshi",
        ):
            screen.query_one("#quality-select", Select).value = quality
            await pilot.pause()
            rendered = neck._build().plain
            assert "not loaded" not in rendered, quality
            assert "■" in rendered, quality  # roots plotted


# ── Layout regression: neck must fit without scrolling ─────────────────────────


async def test_neck_fully_visible_at_minimum_size():
    """Regression: the chord row must never starve the neck viewport.

    The full-neck diagram (header + 6 strings + bracket + legend) has to be
    fully visible without scrolling, down to the app's minimum supported
    terminal size (MIN_COLS x MIN_ROWS).
    """
    from guitar_tui.app import MIN_COLS, MIN_ROWS

    for size in [(MIN_COLS, MIN_ROWS), (120, 40), (140, 50)]:
        async with GuitarTUI().run_test(size=size) as pilot:
            screen = await _goto_tools(pilot)
            key_content = screen.query_one("#key-content")
            assert key_content.max_scroll_y == 0, (
                f"neck viewport scrolls at terminal size {size}: "
                f"container={key_content.size.height} "
                f"virtual={key_content.virtual_size.height}"
            )
