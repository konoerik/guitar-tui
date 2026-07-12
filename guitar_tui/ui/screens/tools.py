"""ToolsMode — Theory Web views (Key/Chord/Song Analysis) and reference panels."""

from __future__ import annotations

import math

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import ContentSwitcher, Footer, OptionList, Select, Static, Tree

from guitar_tui.engine.chord_renderer import render_chord
from guitar_tui.engine.models import BarreDef, ChordSpec
from guitar_tui.loaders.models import ChordEntry
from guitar_tui.theory.keys import (
    CHARACTERISTIC_NOTE,
    KEY_NAMES,
    QUALITY_CHORD_PARENT,
    QUALITY_NAMES,
    QUALITY_TO_SCALE,
    capo_chart,
    chord_tones,
    diatonic_chords,
    enharmonic_name,
    key_context,
    key_signatures,
    note_to_semitone,
    semitone_to_note,
)
from guitar_tui.theory.web import (
    chord_memberships,
    fit_position_shift,
    realize_progression,
    transposition_offset,
)
from guitar_tui.ui.styles import palette, quality_style
from guitar_tui.ui.widgets.full_neck import FullNeckWidget
from guitar_tui.ui.widgets.metronome import MetronomeWidget


# Interval reference — symbols match the intervals lesson (Track 4): plain
# degree numbers, no P-prefixes. (name, semitones, symbol, altered?)
_INTERVAL_ROWS: list[tuple[str, int, str, bool]] = [
    ("Root (unison)", 0,  "1",  False),
    ("Minor 2nd",     1,  "b2", True),
    ("Major 2nd",     2,  "2",  False),
    ("Minor 3rd",     3,  "b3", True),
    ("Major 3rd",     4,  "3",  False),
    ("Perfect 4th",   5,  "4",  False),
    ("Tritone",       6,  "b5", True),
    ("Perfect 5th",   7,  "5",  False),
    ("Minor 6th",     8,  "b6", True),
    ("Major 6th",     9,  "6",  False),
    ("Minor 7th",     10, "b7", True),
    ("Major 7th",     11, "7",  False),
    ("Octave",        12, "8",  False),
]

# Chord formula reference, grouped. (group, [(name, formula_degrees)])
_FORMULA_GROUPS: list[tuple[str, list[tuple[str, list[str]]]]] = [
    ("Triads", [
        ("Major",   ["1", "3", "5"]),
        ("Minor",   ["1", "b3", "5"]),
        ("Dim",     ["1", "b3", "b5"]),
        ("Aug",     ["1", "3", "#5"]),
    ]),
    ("Sevenths", [
        ("Dom 7",   ["1", "3", "5", "b7"]),
        ("Major 7", ["1", "3", "5", "7"]),
        ("Minor 7", ["1", "b3", "5", "b7"]),
    ]),
    ("Sus / Add", [
        ("Sus2",    ["1", "2", "5"]),
        ("Sus4",    ["1", "4", "5"]),
        ("Add9",    ["1", "3", "5", "9"]),
    ]),
    ("Power", [
        ("Power (5)", ["1", "5"]),
    ]),
]

_SCALE_FORMULA = """\
  Major Scale — Interval Formula
  ─────────────────────────────────────────────
  Pattern:  W  –  W  –  H  –  W  –  W  –  W  –  H
            (W = whole step = 2 semitones)
            (H = half step  = 1 semitone)

  Example — C major:
    C    D    E    F    G    A    B    C
     2    2    1    2    2    2    1

  Apply the same pattern from any root note
  to build the major scale in that key.
  Compare: D major = D  E  F#  G  A  B  C#  D"""

# Maps tree leaf data → ContentSwitcher pane ID
_PANE_TITLES: dict[str, str] = {
    "content-key-view":      "Key View",
    "content-chord-view":    "Chord View",
    "content-song-analysis": "Song Analysis",
    "content-metronome":     "Metronome",
    "content-tunings":       "Tunings",
    "content-circle":        "Circle of Fifths",
    "content-key-sigs":      "Key Signatures",
    "content-capo":          "Capo Reference",
    "content-intervals":     "Intervals",
    "content-scale-formula": "Scale Formulas",
    "content-chord-formulas":"Chord Formulas",
    "content-notes":         "Notes on Strings",
    "content-diatonic":      "Diatonic Chords",
    "content-barre":         "Barre Positions",
}


def _strip_octave(note: str) -> str:
    return note.rstrip("0123456789")


# Chord-select ordering: by root (A-first, like KEY_NAMES) then quality.
_SUFFIX_ORDER = ["", "m", "5", "7", "m7", "maj7", "°", "sus2", "sus4", "add9", "6", "m6", "9"]


def _chord_sort_key(name: str) -> tuple[int, int, str]:
    root_len = 2 if len(name) >= 2 and name[1] in "#b" else 1
    root, suffix = name[:root_len], name[root_len:]
    try:
        root_rank = KEY_NAMES.index(semitone_to_note(note_to_semitone(root)))
    except KeyError:
        root_rank = 99
    suffix_rank = _SUFFIX_ORDER.index(suffix) if suffix in _SUFFIX_ORDER else len(_SUFFIX_ORDER)
    return (root_rank, suffix_rank, suffix)


def _hjoin(blocks: list[Text], gap: int = 3) -> Text:
    """Join Text blocks side by side, top-aligned, padded to equal width."""
    split = [block.split("\n") for block in blocks]
    widths = [max((line.cell_len for line in lines), default=0) for lines in split]
    height = max(len(lines) for lines in split)
    out = Text()
    for row in range(height):
        for i, lines in enumerate(split):
            cell = lines[row] if row < len(lines) else Text("")
            out.append_text(cell)
            if i < len(split) - 1:
                out.append(" " * (widths[i] - cell.cell_len + gap))
        out.append("\n")
    return out


class ToolsMode(Screen):
    """Card-panel tools screen: tree nav on the left, content on the right."""

    BINDINGS = [
        ("escape", "app.goto_welcome", "Back"),
        ("[", "prev_position", "◀ Pos"),
        ("]", "next_position", "Pos ▶"),
        ("comma", "prev_chord", "◀ Chord"),
        ("full_stop", "next_chord", "Chord ▶"),
        ("v", "next_voicing", "Voicing"),
        ("g", "goto_chord_view", "Chord ↗"),
        ("backspace", "back", "◀ Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._position: int = 1
        self._chord_idx: int = 0
        self._voicing_idx: int = 0
        self._chords: list[tuple[str, str]] = []
        self._chord_strip_note: str = ""
        # Theory Web navigation: (pane_id, view state) entries; backspace pops.
        self._history: list[tuple[str, dict]] = []
        self._membership_targets: list[tuple[str, str, str]] = []  # (key, quality, roman)
        self._song_link_targets: list[tuple[str, str | None]] = []  # (pane, chord|None)

    def compose(self) -> ComposeResult:
        with Horizontal(id="tools-frame"):
            with VerticalScroll(id="tools-nav"):
                yield Tree("Tools", id="tools-tree")
            with Vertical(id="tools-content"):
                with ContentSwitcher(initial="content-key-view", id="tools-switcher"):
                    # ── Key View ──────────────────────────────────────────
                    with Vertical(id="content-key-view"):
                        with Horizontal(id="key-controls"):
                            yield Select(
                                options=[(n, n) for n in KEY_NAMES],
                                value="A",
                                id="key-select",
                                prompt="Key…",
                            )
                            yield Select(
                                options=[(q, q) for q in QUALITY_NAMES],
                                value="Minor",
                                id="quality-select",
                                prompt="Scale/Mode…",
                            )
                        yield Static("", id="key-context")
                        with ScrollableContainer(id="key-content"):
                            yield FullNeckWidget(id="full-neck")
                        with ScrollableContainer(id="chord-row"):
                            yield Static("", id="chord-strip")
                            yield Static("", id="chord-detail")
                            yield Static("", id="key-related")
                    # ── Chord View (Theory Web) ───────────────────────────
                    with Vertical(id="content-chord-view"):
                        with Horizontal(id="chord-controls"):
                            chord_names = sorted(
                                self.app.data_loader.chords, key=_chord_sort_key
                            )
                            yield Select(
                                options=[(n, n) for n in chord_names],
                                value="Am",
                                id="chord-select",
                                prompt="Chord…",
                            )
                        with VerticalScroll(id="chord-view-content"):
                            yield Static("", id="chord-header")
                            yield Static("", id="chord-voicings")
                            yield Static("", id="chord-functions-title")
                            yield OptionList(id="chord-memberships")
                            yield Static("", id="chord-lessons")
                    # ── Song Analysis (Theory Web workflow) ───────────────
                    with Vertical(id="content-song-analysis"):
                        with Horizontal(id="song-controls"):
                            yield Select(
                                options=[(n, n) for n in KEY_NAMES],
                                value="A",
                                id="song-key-select",
                                prompt="Key…",
                            )
                            yield Select(
                                options=[(q, q) for q in QUALITY_NAMES],
                                value="Minor",
                                id="song-quality-select",
                                prompt="Scale/Mode…",
                            )
                        with VerticalScroll(id="song-view-content"):
                            yield Static("", id="song-report")
                            yield Static("", id="song-links-title")
                            yield OptionList(id="song-links")
                    # ── Metronome ─────────────────────────────────────────
                    with Vertical(id="content-metronome"):
                        yield MetronomeWidget()
                    # ── Reference panels (each in its own pane) ───────────
                    with VerticalScroll(id="content-tunings"):
                        yield Static("", id="tunings-panel")
                    with VerticalScroll(id="content-circle"):
                        yield Static("", id="circle-panel")
                    with VerticalScroll(id="content-key-sigs"):
                        yield Static("", id="key-sigs-panel")
                    with VerticalScroll(id="content-capo"):
                        yield Static("", id="capo-panel")
                    with VerticalScroll(id="content-intervals"):
                        yield Static("", id="intervals-panel")
                    with VerticalScroll(id="content-scale-formula"):
                        yield Static(_SCALE_FORMULA, id="scale-formula-panel")
                    with VerticalScroll(id="content-chord-formulas"):
                        yield Static("", id="formulas-panel")
                    with VerticalScroll(id="content-notes"):
                        yield Static("", id="notes-panel")
                    with VerticalScroll(id="content-diatonic"):
                        yield Static("", id="diatonic-all-keys-panel")
                    with VerticalScroll(id="content-barre"):
                        yield Static("", id="barre-positions-panel")
        yield Footer()

    def on_mount(self) -> None:
        self._build_tree()
        self.query_one("#tools-nav").border_title = "Tools"
        self.query_one("#tools-content").border_title = "Key View"
        self.watch(self.app, "theme", self._on_theme_changed)
        self._sync()
        self._update_chord_detail()
        self._sync_chord_view()
        self._sync_song_analysis()
        self._build_reference_panels()
        self.query_one("#key-select", Select).focus()

    def _on_theme_changed(self, _: str) -> None:
        self._build_reference_panels()

    def _pal(self) -> dict[str, str]:
        return palette(self.app.current_theme.dark)

    def _build_reference_panels(self) -> None:
        self._build_tunings_panel()
        self._build_circle_panel()
        self._build_key_sigs_panel()
        self._build_capo_panel()
        self._build_intervals_panel()
        self._build_formulas_panel()
        self._build_notes_on_strings_panel()
        self._build_diatonic_all_keys_panel()
        self._build_barre_positions_panel()

    # ── Tree ──────────────────────────────────────────────────────────────────

    def _build_tree(self) -> None:
        tree = self.query_one("#tools-tree", Tree)
        tree.show_root = False
        interactive = tree.root.add("Interactive", expand=True)
        interactive.add_leaf("Key View", data="content-key-view")
        interactive.add_leaf("Chord View", data="content-chord-view")
        interactive.add_leaf("Song Analysis", data="content-song-analysis")
        interactive.add_leaf("Metronome", data="content-metronome")
        reference = tree.root.add("Reference", expand=True)
        reference.add_leaf("Circle of Fifths", data="content-circle")
        reference.add_leaf("Key Signatures", data="content-key-sigs")
        reference.add_leaf("Diatonic Chords", data="content-diatonic")
        reference.add_leaf("Intervals", data="content-intervals")
        reference.add_leaf("Scale Formulas", data="content-scale-formula")
        reference.add_leaf("Chord Formulas", data="content-chord-formulas")
        reference.add_leaf("Notes on Strings", data="content-notes")
        reference.add_leaf("Barre Positions", data="content-barre")
        reference.add_leaf("Capo Reference", data="content-capo")
        reference.add_leaf("Tunings", data="content-tunings")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        pane_id = event.node.data
        if pane_id is None:
            return
        self._switch_pane(pane_id)
        if pane_id == "content-metronome":
            self.query_one(MetronomeWidget).focus()

    def _switch_pane(self, pane_id: str) -> None:
        self.query_one("#tools-switcher", ContentSwitcher).current = pane_id
        self.query_one("#tools-content").border_title = _PANE_TITLES.get(pane_id, pane_id)
        self.refresh_bindings()

    # ── Bindings guard (position/chord only active on Key View) ───────────────

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if action in (
            "prev_position", "next_position", "prev_chord", "next_chord",
            "next_voicing", "goto_chord_view",
        ):
            switcher = self.query_one("#tools-switcher", ContentSwitcher)
            return switcher.current == "content-key-view"
        if action == "back":
            return bool(self._history)
        return True

    # ── Key View actions ──────────────────────────────────────────────────────

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.value is Select.NULL:
            return
        if event.select.id == "chord-select":
            self._sync_chord_view()
        elif event.select.id in ("song-key-select", "song-quality-select"):
            self._sync_song_analysis()
        else:
            self._position = 1
            self._chord_idx = 0
            self._voicing_idx = 0
            self._sync()

    def action_prev_chord(self) -> None:
        if not self._chords:
            return
        self._chord_idx = (self._chord_idx - 1) % len(self._chords)
        self._voicing_idx = 0
        self._render_chord_strip()
        self._update_chord_detail()

    def action_next_chord(self) -> None:
        if not self._chords:
            return
        self._chord_idx = (self._chord_idx + 1) % len(self._chords)
        self._voicing_idx = 0
        self._render_chord_strip()
        self._update_chord_detail()

    def action_next_voicing(self) -> None:
        entry = self._current_chord_entry()
        if entry is not None and len(entry.voicings) > 1:
            self._voicing_idx = (self._voicing_idx + 1) % len(entry.voicings)
            self._update_chord_detail()

    # ── Theory Web navigation (history stack) ─────────────────────────────────

    def _capture_state(self) -> tuple[str, dict]:
        pane = self.query_one("#tools-switcher", ContentSwitcher).current or ""
        if pane == "content-key-view":
            return (pane, {
                "key": self._key(), "quality": self._quality(),
                "position": self._position, "chord_idx": self._chord_idx,
                "voicing_idx": self._voicing_idx,
            })
        if pane == "content-chord-view":
            return (pane, {"chord": self._chord_view_name()})
        if pane == "content-song-analysis":
            return (pane, {"key": self._song_key(), "quality": self._song_quality()})
        return (pane, {})

    def _restore_state(self, pane: str, state: dict) -> None:
        if pane == "content-key-view":
            with self.prevent(Select.Changed):
                self.query_one("#key-select", Select).value = state["key"]
                self.query_one("#quality-select", Select).value = state["quality"]
            self._position = state["position"]
            self._chord_idx = state["chord_idx"]
            self._voicing_idx = state["voicing_idx"]
            self._sync()
        elif pane == "content-chord-view":
            with self.prevent(Select.Changed):
                self.query_one("#chord-select", Select).value = state["chord"]
            self._sync_chord_view()
        elif pane == "content-song-analysis":
            with self.prevent(Select.Changed):
                self.query_one("#song-key-select", Select).value = state["key"]
                self.query_one("#song-quality-select", Select).value = state["quality"]
            self._sync_song_analysis()

    def _navigate_to(self, pane_id: str) -> None:
        """Follow a Theory Web link: remember where we were, then switch."""
        self._history.append(self._capture_state())
        self._switch_pane(pane_id)

    def action_back(self) -> None:
        if not self._history:
            return
        pane, state = self._history.pop()
        self._switch_pane(pane)
        self._restore_state(pane, state)

    def action_goto_chord_view(self) -> None:
        """Open the Key View's selected chord in the Chord View."""
        entry = self._current_chord_entry()
        if entry is None:
            return
        self._navigate_to("content-chord-view")
        with self.prevent(Select.Changed):
            self.query_one("#chord-select", Select).value = entry.name
        self._sync_chord_view()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "chord-memberships":
            self._follow_membership(event.option_index)
        elif event.option_list.id == "song-links":
            self._follow_song_link(event.option_index)

    def _follow_membership(self, index: int) -> None:
        if not (0 <= index < len(self._membership_targets)):
            return
        key, quality, roman = self._membership_targets[index]
        self._open_key_view(key, quality, roman)

    def _open_key_view(self, key: str, quality: str, roman: str | None = None) -> None:
        self._navigate_to("content-key-view")
        with self.prevent(Select.Changed):
            self.query_one("#key-select", Select).value = key
            self.query_one("#quality-select", Select).value = quality
        self._position = 1
        self._voicing_idx = 0
        # Land on the chord's slot in the diatonic strip when given.
        romans = [r for r, _ in diatonic_chords(key, quality)]
        self._chord_idx = romans.index(roman) if roman in romans else 0
        self._sync()

    def _follow_song_link(self, index: int) -> None:
        if not (0 <= index < len(self._song_link_targets)):
            return
        pane, chord = self._song_link_targets[index]
        if pane == "content-key-view":
            self._open_key_view(self._song_key(), self._song_quality())
        elif pane == "content-chord-view" and chord is not None:
            self._navigate_to("content-chord-view")
            with self.prevent(Select.Changed):
                self.query_one("#chord-select", Select).value = chord
            self._sync_chord_view()

    def action_prev_position(self) -> None:
        n_pos = self._n_positions()
        if n_pos:
            self._position = (self._position - 2) % n_pos + 1
            self._sync_position()

    def action_next_position(self) -> None:
        n_pos = self._n_positions()
        if n_pos:
            self._position = self._position % n_pos + 1
            self._sync_position()

    # ── Song Analysis ─────────────────────────────────────────────────────────

    def _song_key(self) -> str:
        v = self.query_one("#song-key-select", Select).value
        return v if v is not Select.NULL else "A"

    def _song_quality(self) -> str:
        v = self.query_one("#song-quality-select", Select).value
        return v if v is not Select.NULL else "Minor"

    def _sync_song_analysis(self) -> None:
        key = self._song_key()
        quality = self._song_quality()
        loader = self.app.data_loader
        t = Text()

        t.append(f"\n  A song in {key} {quality}\n", style="bold")
        t.append("  " + "─" * 60 + "\n\n")

        # Scale + suggested positions (transposed to the song's key)
        scale_name = QUALITY_TO_SCALE.get(quality, "natural_minor")
        scale = loader.scales.get(scale_name)
        if scale is not None:
            t.append("  Scale        ", style="bold")
            t.append(f"{key} {scale.full_name}\n")
            offset = transposition_offset(key, scale.key)
            spans: list[tuple[int, int, int]] = []
            for pos in scale.positions:
                lo, hi = pos.fret_range
                shift = fit_position_shift(lo + offset, hi + offset, 15)
                spans.append((pos.id, lo + offset + shift, hi + offset + shift))
            t.append("  Positions    ", style="bold")
            t.append("   ".join(f"{pid}: frets {lo}–{hi}" for pid, lo, hi in spans))
            start = min(spans, key=lambda s: s[1])
            t.append(f"\n               start with position {start[0]} — lowest on the neck\n", style="dim")

        # Key context
        ctx = key_context(key, quality)
        if ctx is not None:
            sig = (
                f"{ctx.accidental_count}♯" if ctx.accidental_count > 0
                else f"{abs(ctx.accidental_count)}♭" if ctx.accidental_count < 0
                else "0♯"
            )
            t.append("  Key          ", style="bold")
            t.append(f"{ctx.relative_label} {ctx.relative_name} · {sig}\n")

        # Diatonic chords
        chord_quality = QUALITY_CHORD_PARENT.get(quality, quality)
        chords = diatonic_chords(key, chord_quality)
        if chords:
            t.append("  Chords       ", style="bold")
            t.append("   ".join(f"{r}: {c}" for r, c in chords) + "\n")

        # Common progressions realized in this key
        progressions = self.app.data_loader.progressions_for(chord_quality)
        if progressions:
            t.append("  Progressions ", style="bold")
            first = True
            for prog in progressions:
                realized = realize_progression(key, prog.quality, prog.numerals)
                prefix = "" if first else "               "
                t.append(f"{prefix}{prog.name:<24}", style="" if first else "")
                t.append("  ".join(c for _, c in realized) + "\n")
                first = False

        # Lessons for this scale
        lessons = self.app.lesson_loader.by_theory_ref(f"scale:{scale_name}")
        if lessons:
            titles = " · ".join(l.meta.title for l in lessons[:3])
            more = f"  (+{len(lessons) - 3} more)" if len(lessons) > 3 else ""
            t.append("  Lessons      ", style="bold")
            t.append(f"{titles}{more}\n")

        self.query_one("#song-report", Static).update(t)

        # Jump links: Key View + each diatonic chord with a library voicing
        self._song_link_targets = [("content-key-view", None)]
        labels = [f"Open {key} {quality} in Key View"]
        for _, chord in chords:
            entry = loader.chords.get(chord)
            if entry is None:
                alt = enharmonic_name(chord)
                entry = loader.chords.get(alt) if alt else None
            if entry is not None:
                self._song_link_targets.append(("content-chord-view", entry.name))
                labels.append(f"Open {entry.name} in Chord View")
        self.query_one("#song-links-title", Static).update(
            Text("  Explore — Enter follows the link:", style="bold")
        )
        links = self.query_one("#song-links", OptionList)
        links.clear_options()
        links.add_options(labels)
        links.highlighted = 0

    # ── Reference panel builders ──────────────────────────────────────────────

    def _build_tunings_panel(self) -> None:
        tunings = self.app.data_loader.tunings
        string_labels = ["E", "A", "D", "G", "B", "e"]
        col = 5
        header  = f"  {'Tuning Reference'}\n"
        header += f"  {'─' * 42}\n\n"
        header += f"  {'Name':<22}" + "".join(f"{l:<{col}}" for l in string_labels) + "\n"
        header += f"  {'─' * 42}"
        rows = [header]
        for tuning in tunings.values():
            notes = [_strip_octave(n) for n in tuning.strings]
            rows.append(
                f"  {tuning.name:<22}" + "".join(f"{n:<{col}}" for n in notes)
            )
        self.query_one("#tunings-panel", Static).update("\n".join(rows))

    def _build_key_sigs_panel(self) -> None:
        maj_w, min_w, sig_w = 6, 6, 4
        ruler = "─" * 48
        lines: list[str] = [
            "  Key Signatures & Circle of Fifths",
            f"  {ruler}",
            "",
            f"  {'Major':<{maj_w}} {'Minor':<{min_w}} {'♯/♭':>{sig_w}}  Accidentals",
            f"  {ruler}",
        ]
        for major, minor, count, acc in key_signatures():
            sig = f"{count}♯" if count > 0 else f"{abs(count)}♭" if count < 0 else "—"
            acc_str = "  ".join(acc) if acc else "—"
            lines.append(f"  {major:<{maj_w}} {minor:<{min_w}} {sig:>{sig_w}}  {acc_str}")
        self.query_one("#key-sigs-panel", Static).update("\n".join(lines))

    def _build_notes_on_strings_panel(self) -> None:
        pal = self._pal()
        open_strings = [("E", 4), ("A", 9), ("D", 2), ("G", 7), ("B", 11), ("e", 4)]
        frets = list(range(13))
        inlays = {3, 5, 7, 9, 12}
        col_w, hdr_w = 4, 4
        ruler = "─" * (hdr_w + col_w * 13 + 2)
        t = Text()
        t.append("\n  Notes on Each String (Open → 12th Fret)\n", style=pal["heading"])
        t.append(f"  {ruler}\n\n", style=pal["muted"])
        t.append("  " + f"{'Str':<{hdr_w}}")
        for f in frets:
            # Inlay frets (3 5 7 9 12) are the physical landmarks on the neck.
            t.append(f"{f:^{col_w}}", style=pal["accent"] if f in inlays else pal["muted"])
        t.append("\n")
        t.append(f"  {ruler}\n", style=pal["muted"])
        for name, open_st in open_strings:
            t.append("  " + f"{name:<{hdr_w}}")
            for f in frets:
                note = semitone_to_note((open_st + f) % 12)
                accidental = "#" in note or "b" in note
                t.append(f"{note:^{col_w}}", style=pal["muted"] if accidental else "")
            t.append("\n")
        t.append("\n  natural notes plain · ", style=pal["muted"])
        t.append("accidentals dimmed", style=pal["muted"])
        t.append(" · inlay frets ", style=pal["muted"])
        t.append("highlighted", style=pal["accent"])
        self.query_one("#notes-panel", Static).update(t)

    def _build_diatonic_all_keys_panel(self) -> None:
        pal = self._pal()
        sigs = key_signatures()
        keys = [sig[0] for sig in sigs]
        degree_labels = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
        key_w, col_w = 4, 7
        ruler = "─" * (key_w + col_w * 7 + 2)
        t = Text()
        t.append("\n  Diatonic Chords — All Major Keys\n", style=pal["heading"])
        t.append(f"  {ruler}\n\n", style=pal["muted"])
        t.append("  " + f"{'Key':<{key_w}}")
        t.append("".join(f"{d:^{col_w}}" for d in degree_labels), style=pal["muted"])
        t.append("\n")
        t.append(f"  {ruler}\n", style=pal["muted"])
        for key in keys:
            t.append("  " + f"{key:<{key_w}}", style=pal["heading"])
            for _, name in diatonic_chords(key, "Major"):
                t.append(f"{name:^{col_w}}", style=quality_style(name, pal))
            t.append("\n")
        t.append("\n  ")
        t.append("major", style=pal["maj"])
        t.append(" · ", style=pal["muted"])
        t.append("minor", style=pal["min"])
        t.append(" · ", style=pal["muted"])
        t.append("diminished", style=pal["dim_q"])
        self.query_one("#diatonic-all-keys-panel", Static).update(t)

    def _build_intervals_panel(self) -> None:
        pal = self._pal()
        ruler = "─" * 45
        t = Text()
        t.append("\n  Intervals\n", style=pal["heading"])
        t.append(f"  {ruler}\n", style=pal["muted"])
        t.append(f"  {'Name':<18}{'Semitones':<12}Symbol\n", style=pal["muted"])
        t.append(f"  {ruler}\n", style=pal["muted"])
        for name, semitones, symbol, altered in _INTERVAL_ROWS:
            t.append(f"  {name:<18}{semitones:<12}")
            t.append(f"{symbol}\n", style=pal["altered"] if altered else "")
        t.append("\n  Symbols match the Intervals lesson (Track 4).", style=pal["muted"])
        self.query_one("#intervals-panel", Static).update(t)

    def _build_formulas_panel(self) -> None:
        pal = self._pal()
        t = Text()
        t.append("\n  Chord Formulas\n", style=pal["heading"])
        t.append("  " + "─" * 34 + "\n", style=pal["muted"])
        for group, formulas in _FORMULA_GROUPS:
            t.append(f"\n  {group}\n", style=pal["heading"])
            for name, degrees in formulas:
                t.append(f"    {name:<12}")
                for i, deg in enumerate(degrees):
                    if i:
                        t.append(" – ", style=pal["muted"])
                    altered = deg.startswith(("b", "#"))
                    t.append(deg, style=pal["altered"] if altered else "")
                t.append("\n")
        t.append("\n  altered degrees ", style=pal["muted"])
        t.append("highlighted", style=pal["altered"])
        t.append(" — they define the chord's color", style=pal["muted"])
        self.query_one("#formulas-panel", Static).update(t)

    def _build_circle_panel(self) -> None:
        """ASCII Circle of Fifths: majors on the outer ring, relative minors inside."""
        pal = self._pal()
        width, height = 56, 17
        cx, cy = width // 2, height // 2
        grid = [[" "] * width for _ in range(height)]
        style_grid: list[list[str | None]] = [[None] * width for _ in range(height)]

        def place(label: str, x: int, y: int, style: str | None) -> None:
            col = max(0, min(width - len(label), x - len(label) // 2))
            for i, ch in enumerate(label):
                grid[y][col + i] = ch
                style_grid[y][col + i] = style

        for i, (major, minor, count, _) in enumerate(key_signatures()):
            angle = math.radians(i * 30 - 90)  # C at 12 o'clock, fifths clockwise
            place(
                major,
                round(cx + 24 * math.cos(angle)),
                round(cy + 7.5 * math.sin(angle)),
                pal["heading"] if count == 0 else None,
            )
            place(
                minor,
                round(cx + 14 * math.cos(angle)),
                round(cy + 4.5 * math.sin(angle)),
                pal["muted"],
            )
        place("majors", cx, cy - 1, pal["muted"])
        place("minors inside", cx, cy + 1, pal["muted"])

        t = Text()
        t.append("\n  Circle of Fifths\n", style=pal["heading"])
        t.append("  " + "─" * 50 + "\n\n", style=pal["muted"])
        for y in range(height):
            t.append("  ")
            x = 0
            while x < width:
                style = style_grid[y][x]
                run = x
                while run < width and style_grid[y][run] == style:
                    run += 1
                t.append("".join(grid[y][x:run]), style=style or "")
                x = run
            t.append("\n")
        t.append("\n  clockwise adds a sharp ♯ · counterclockwise adds a flat ♭\n", style=pal["muted"])
        t.append("  neighbors share 6 of 7 notes — the closest keys to modulate to", style=pal["muted"])
        self.query_one("#circle-panel", Static).update(t)

    def _build_barre_positions_panel(self) -> None:
        e_open, a_open = 4, 9
        chromatic_order = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
        col_w, key_w = 12, 5

        def fret_label(open_st: int, target: str) -> str:
            target_st = note_to_semitone(target)
            fret = (target_st - open_st) % 12
            if fret == 0:
                return "open"
            return f"{fret}th" if fret not in (1, 2, 3) else f"{fret}{'st' if fret == 1 else 'nd' if fret == 2 else 'rd'}"

        ruler = "─" * (key_w + col_w * 2 + 2)
        lines: list[str] = [
            "",
            "  Barre Chord Position Finder",
            f"  {ruler}",
            "",
            "  " + f"{'Note':<{key_w}}" + f"{'E-shape (low E)':^{col_w}}" + f"{'A-shape (A str)':^{col_w}}",
            f"  {ruler}",
        ]
        for note in chromatic_order:
            e_label = fret_label(e_open, note)
            a_label = fret_label(a_open, note)
            lines.append("  " + f"{note:<{key_w}}" + f"{e_label:^{col_w}}" + f"{a_label:^{col_w}}")
        lines.append(f"  {ruler}")
        lines.append("  Root at fret → barre that fret with finger 1")
        self.query_one("#barre-positions-panel", Static).update("\n".join(lines))

    def _build_capo_panel(self) -> None:
        shapes, rows = capo_chart()
        col = 5
        width = 7 + col * len(shapes)
        ruler = "─" * width
        lines: list[str] = [
            "",
            "  Capo Reference  (open shape → sounding chord)",
            f"  {ruler}",
            "",
            "  " + f"{'Capo':<7}" + "".join(f"{s:^{col}}" for s in shapes),
            f"  {ruler}",
        ]
        for i, row in enumerate(rows):
            lines.append("  " + f"{i + 1:<7}" + "".join(f"{chord:^{col}}" for chord in row))
        self.query_one("#capo-panel", Static).update("\n".join(lines))

    # ── Key View helpers ──────────────────────────────────────────────────────

    def _key(self) -> str:
        v = self.query_one("#key-select", Select).value
        return v if v is not Select.NULL else "A"

    def _quality(self) -> str:
        v = self.query_one("#quality-select", Select).value
        return v if v is not Select.NULL else "Minor"

    def _n_positions(self) -> int:
        scale_name = QUALITY_TO_SCALE.get(self._quality(), "natural_minor")
        scales = self.app.data_loader.scales
        return len(scales[scale_name].positions) if scale_name in scales else 0

    def _sync(self) -> None:
        key      = self._key()
        quality  = self._quality()
        scale_name = QUALITY_TO_SCALE.get(quality, "natural_minor")
        neck = self.query_one("#full-neck", FullNeckWidget)
        neck.root_note        = key
        neck.scale_name       = scale_name
        neck.current_position = self._position
        neck.characteristic   = CHARACTERISTIC_NOTE.get(quality)
        self._update_key_context(key, quality)
        self._update_chord_strip(key, quality)

    def _update_key_context(self, key: str, quality: str) -> None:
        ctx = key_context(key, quality)
        if ctx is None:
            # Not a mode of a major key (harmonic minor, symmetric scales, …).
            line = f"  {key} {quality}"
        else:
            sig = (
                f"{ctx.accidental_count}♯" if ctx.accidental_count > 0
                else f"{abs(ctx.accidental_count)}♭" if ctx.accidental_count < 0
                else "0♯"
            )
            line = f"  {key} {quality} · {ctx.relative_label} {ctx.relative_name} · {sig}"
        self.query_one("#key-context", Static).update(Text(line, style="dim"))

    def _sync_position(self) -> None:
        self.query_one("#full-neck", FullNeckWidget).current_position = self._position

    # ── Chord View ────────────────────────────────────────────────────────────

    def _chord_view_name(self) -> str:
        v = self.query_one("#chord-select", Select).value
        return v if v is not Select.NULL else "Am"

    def _sync_chord_view(self) -> None:
        name = self._chord_view_name()
        entry = self.app.data_loader.chords.get(name)
        if entry is None:
            return

        # Header: full name + spelled tones
        header = Text(f"\n  {entry.name} — {entry.full_name}", style="bold")
        tones = chord_tones(name)
        if tones:
            header.append(f"    {' · '.join(tones)}", style="dim")
        self.query_one("#chord-header", Static).update(header)

        # All voicings side by side
        blocks: list[Text] = []
        for voicing in entry.voicings:
            barre = None
            if voicing.barre:
                barre = BarreDef(
                    fret=voicing.barre.fret,
                    from_string=voicing.barre.from_string,
                    to_string=voicing.barre.to_string,
                    finger=voicing.barre.finger,
                )
            spec = ChordSpec(
                type="chord",
                frets=voicing.frets,
                fingers=voicing.fingers,
                base_fret=voicing.base_fret,
                barre=barre,
            )
            block = render_chord(spec)
            block.append(f"\n{voicing.label}", style="dim")
            blocks.append(block)
        self.query_one("#chord-voicings", Static).update(_hjoin(blocks, gap=4))

        # Keys this chord lives in, with its function there (Theory Web links)
        memberships = chord_memberships(name)
        self._membership_targets = [
            (m.key_root, m.quality, m.roman) for m in memberships
        ]
        option_list = self.query_one("#chord-memberships", OptionList)
        option_list.clear_options()
        title = self.query_one("#chord-functions-title", Static)
        if memberships:
            title.update(Text("  Functions — Enter opens the key:", style="bold"))
            option_list.add_options(
                [f"{m.roman} in {m.key_root} {m.quality}" for m in memberships]
            )
            option_list.highlighted = 0  # Enter follows the link immediately
            option_list.display = True
        else:
            title.update(Text("  (not a diatonic triad — no key functions)", style="dim"))
            option_list.display = False

        # Lessons that reference this chord
        lessons = self.app.lesson_loader.by_theory_ref(f"chord:{name}")
        lessons_widget = self.query_one("#chord-lessons", Static)
        if lessons:
            titles = " · ".join(l.meta.title for l in lessons[:4])
            more = f"  (+{len(lessons) - 4} more)" if len(lessons) > 4 else ""
            t = Text("\n  Lessons: ", style="bold")
            t.append(f"{titles}{more}  ")
            t.append("→ [2] Lessons", style="dim")
            lessons_widget.update(t)
        else:
            lessons_widget.update("")

    def _update_chord_strip(self, key: str, quality: str) -> None:
        chord_quality = QUALITY_CHORD_PARENT.get(quality, quality)
        if chord_quality != quality:
            self._chord_strip_note = f"  (chords from {chord_quality})"
        elif quality == "Blues":
            self._chord_strip_note = "  (12-bar harmony)"
        else:
            self._chord_strip_note = ""
        self._chords = diatonic_chords(key, chord_quality)
        if not self._chords:
            # Symmetric / gapped scales have no triad-per-degree chord set.
            self._chord_strip_note = "  (no diatonic chord set for this scale)"
            self.query_one("#chord-detail", Static).update("")
        self._render_chord_strip()
        self._update_chord_detail()
        self._update_related(key, quality, chord_quality)

    def _update_related(self, key: str, quality: str, chord_quality: str) -> None:
        """Theory Web panel: progressions realized in this key + related lessons."""
        t = Text()
        progressions = self.app.data_loader.progressions_for(chord_quality)
        if progressions:
            t.append(f"\n  Progressions in {key} {chord_quality}\n", style="bold")
            for prog in progressions:
                realized = realize_progression(key, prog.quality, prog.numerals)
                t.append(f"  {prog.name:<24}", style="dim")
                t.append("  ".join(chord for _, chord in realized))
                t.append("\n")
        scale_name = QUALITY_TO_SCALE.get(quality)
        if scale_name is not None:
            lessons = self.app.lesson_loader.by_theory_ref(f"scale:{scale_name}")
            if lessons:
                titles = " · ".join(l.meta.title for l in lessons[:4])
                more = f"  (+{len(lessons) - 4} more)" if len(lessons) > 4 else ""
                t.append("\n  Lessons: ", style="bold")
                t.append(f"{titles}{more}  ", style="")
                t.append("→ [2] Lessons\n", style="dim")
        self.query_one("#key-related", Static).update(t)

    def _render_chord_strip(self) -> None:
        t = Text("  ")
        for i, (roman, name) in enumerate(self._chords):
            label = f"{roman}: {name}"
            t.append(label, style="bold reverse" if i == self._chord_idx else "")
            if i < len(self._chords) - 1:
                t.append("  │  ")
        if self._chord_strip_note:
            t.append(self._chord_strip_note, style="dim")
        self.query_one("#chord-strip", Static).update(t)

    def _current_chord_entry(self) -> ChordEntry | None:
        if not self._chords:
            return None
        _, chord_name = self._chords[self._chord_idx]
        entry = self.app.data_loader.chords.get(chord_name)
        if entry is None:
            # Data may store the enharmonic spelling (Db vs C#, G#m vs Abm).
            alt = enharmonic_name(chord_name)
            if alt is not None:
                entry = self.app.data_loader.chords.get(alt)
        return entry

    def _update_chord_detail(self) -> None:
        widget = self.query_one("#chord-detail", Static)
        if not self._chords:
            return
        _, chord_name = self._chords[self._chord_idx]
        entry = self._current_chord_entry()
        if entry is None:
            tones = chord_tones(chord_name)
            if tones:
                widget.update(
                    f"  {chord_name}  =  {' · '.join(tones)}\n"
                    f"  (no voicing in the library yet)"
                )
            else:
                widget.update(f"  {chord_name}\n  (no voicing)")
            return
        n_voicings = len(entry.voicings)
        voicing = entry.voicings[self._voicing_idx % n_voicings]
        barre = None
        if voicing.barre:
            barre = BarreDef(
                fret=voicing.barre.fret,
                from_string=voicing.barre.from_string,
                to_string=voicing.barre.to_string,
                finger=voicing.barre.finger,
            )
        spec = ChordSpec(
            type="chord",
            title=chord_name,
            frets=voicing.frets,
            fingers=voicing.fingers,
            base_fret=voicing.base_fret,
            barre=barre,
        )
        diagram = render_chord(spec)
        if n_voicings > 1:
            idx = self._voicing_idx % n_voicings
            diagram.append(
                f"\n  {voicing.label} · voicing {idx + 1}/{n_voicings} · v cycles",
                style="dim",
            )
        widget.update(diagram)
