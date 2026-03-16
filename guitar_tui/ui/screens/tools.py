"""ToolsMode — Key View and Reference panels."""

from __future__ import annotations

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import ContentSwitcher, Footer, Select, Static, Tree

from guitar_tui.engine.chord_renderer import render_chord
from guitar_tui.engine.models import BarreDef, ChordSpec
from guitar_tui.theory.keys import (
    KEY_NAMES,
    QUALITY_CHORD_PARENT,
    QUALITY_NAMES,
    QUALITY_TO_SCALE,
    capo_chart,
    diatonic_chords,
    key_signatures,
    note_to_semitone,
    semitone_to_note,
)
from guitar_tui.ui.widgets.full_neck import FullNeckWidget
from guitar_tui.ui.widgets.metronome import MetronomeWidget


_INTERVALS_TABLE = """\
  Intervals
  ─────────────────────────────────────────────
  Name              Semitones   Symbol
  ─────────────────────────────────────────────
  Unison            0           P1
  Minor 2nd         1           b2
  Major 2nd         2           2
  Minor 3rd         3           b3
  Major 3rd         4           3
  Perfect 4th       5           P4
  Tritone           6           #4 / b5
  Perfect 5th       7           P5
  Minor 6th         8           b6
  Major 6th         9           6
  Minor 7th         10          b7
  Major 7th         11          7
  Octave            12          P8"""

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

_CHORD_FORMULAS = """\
  Chord Formulas
  ──────────────────────────────────

  Chord           Formula
  ──────────────────────────────────
  Major           1 – 3 – 5
  Minor           1 – b3 – 5
  Dom 7           1 – 3 – 5 – b7
  Major 7         1 – 3 – 5 – 7
  Minor 7         1 – b3 – 5 – b7
  Dim             1 – b3 – b5
  Aug             1 – 3 – #5
  Sus2            1 – 2 – 5
  Sus4            1 – 4 – 5
  Add9            1 – 3 – 5 – 9
  Power           1 – 5"""

# Maps tree leaf data → ContentSwitcher pane ID
_PANE_TITLES: dict[str, str] = {
    "content-key-view":      "Key View",
    "content-metronome":     "Metronome",
    "content-tunings":       "Tunings",
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


class ToolsMode(Screen):
    """Card-panel tools screen: tree nav on the left, content on the right."""

    BINDINGS = [
        ("escape", "app.goto_welcome", "Back"),
        ("[", "prev_position", "◀ Pos"),
        ("]", "next_position", "Pos ▶"),
        ("comma", "prev_chord", "◀ Chord"),
        ("full_stop", "next_chord", "Chord ▶"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._position: int = 1
        self._chord_idx: int = 0
        self._chords: list[tuple[str, str]] = []
        self._chord_strip_note: str = ""

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
                        with ScrollableContainer(id="key-content"):
                            yield FullNeckWidget(id="full-neck")
                        with ScrollableContainer(id="chord-row"):
                            yield Static("", id="chord-strip")
                            yield Static("", id="chord-detail")
                    # ── Metronome ─────────────────────────────────────────
                    with Vertical(id="content-metronome"):
                        yield MetronomeWidget()
                    # ── Reference panels (each in its own pane) ───────────
                    with VerticalScroll(id="content-tunings"):
                        yield Static("", id="tunings-panel")
                    with VerticalScroll(id="content-key-sigs"):
                        yield Static("", id="key-sigs-panel")
                    with VerticalScroll(id="content-capo"):
                        yield Static("", id="capo-panel")
                    with VerticalScroll(id="content-intervals"):
                        yield Static(_INTERVALS_TABLE, id="intervals-panel")
                    with VerticalScroll(id="content-scale-formula"):
                        yield Static(_SCALE_FORMULA, id="scale-formula-panel")
                    with VerticalScroll(id="content-chord-formulas"):
                        yield Static(_CHORD_FORMULAS, id="formulas-panel")
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
        self._sync()
        self._update_chord_detail()
        self._build_tunings_panel()
        self._build_key_sigs_panel()
        self._build_capo_panel()
        self._build_notes_on_strings_panel()
        self._build_diatonic_all_keys_panel()
        self._build_barre_positions_panel()
        self.query_one("#key-select", Select).focus()

    # ── Tree ──────────────────────────────────────────────────────────────────

    def _build_tree(self) -> None:
        tree = self.query_one("#tools-tree", Tree)
        tree.show_root = False
        tree.root.add_leaf("Key View", data="content-key-view")
        tree.root.add_leaf("Metronome", data="content-metronome")
        tree.root.add_leaf("", data=None)  # spacer
        tree.root.add_leaf("Tunings", data="content-tunings")
        tree.root.add_leaf("Key Signatures", data="content-key-sigs")
        tree.root.add_leaf("Capo Reference", data="content-capo")
        tree.root.add_leaf("Intervals", data="content-intervals")
        tree.root.add_leaf("Scale Formulas", data="content-scale-formula")
        tree.root.add_leaf("Chord Formulas", data="content-chord-formulas")
        tree.root.add_leaf("Notes on Strings", data="content-notes")
        tree.root.add_leaf("Diatonic Chords", data="content-diatonic")
        tree.root.add_leaf("Barre Positions", data="content-barre")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        pane_id = event.node.data
        if pane_id is None:
            return
        self.query_one("#tools-switcher", ContentSwitcher).current = pane_id
        self.query_one("#tools-content").border_title = _PANE_TITLES.get(pane_id, pane_id)
        if pane_id == "content-metronome":
            self.query_one(MetronomeWidget).focus()
        self.refresh_bindings()

    # ── Bindings guard (position/chord only active on Key View) ───────────────

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if action in ("prev_position", "next_position", "prev_chord", "next_chord"):
            switcher = self.query_one("#tools-switcher", ContentSwitcher)
            return switcher.current == "content-key-view"
        return True

    # ── Key View actions ──────────────────────────────────────────────────────

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.value is not Select.NULL:
            self._position = 1
            self._chord_idx = 0
            self._sync()

    def action_prev_chord(self) -> None:
        if not self._chords:
            return
        self._chord_idx = (self._chord_idx - 1) % len(self._chords)
        self._render_chord_strip()
        self._update_chord_detail()

    def action_next_chord(self) -> None:
        if not self._chords:
            return
        self._chord_idx = (self._chord_idx + 1) % len(self._chords)
        self._render_chord_strip()
        self._update_chord_detail()

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
        open_strings = [("E", 4), ("A", 9), ("D", 2), ("G", 7), ("B", 11), ("e", 4)]
        frets = list(range(13))
        col_w, hdr_w = 4, 4
        ruler = "─" * (hdr_w + col_w * 13 + 2)
        lines: list[str] = [
            "",
            "  Notes on Each String (Open → 12th Fret)",
            f"  {ruler}",
            "",
            "  " + f"{'Str':<{hdr_w}}" + "".join(f"{f:^{col_w}}" for f in frets),
            f"  {ruler}",
        ]
        for name, open_st in open_strings:
            notes = [semitone_to_note((open_st + f) % 12) for f in frets]
            lines.append("  " + f"{name:<{hdr_w}}" + "".join(f"{n:^{col_w}}" for n in notes))
        self.query_one("#notes-panel", Static).update("\n".join(lines))

    def _build_diatonic_all_keys_panel(self) -> None:
        sigs = key_signatures()
        keys = [sig[0] for sig in sigs]
        degree_labels = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
        key_w, col_w = 4, 7
        ruler = "─" * (key_w + col_w * 7 + 2)
        lines: list[str] = [
            "",
            "  Diatonic Chords — All Major Keys",
            f"  {ruler}",
            "",
            "  " + f"{'Key':<{key_w}}" + "".join(f"{d:^{col_w}}" for d in degree_labels),
            f"  {ruler}",
        ]
        for key in keys:
            chords = diatonic_chords(key, "Major")
            chord_names = [name for _, name in chords]
            lines.append("  " + f"{key:<{key_w}}" + "".join(f"{n:^{col_w}}" for n in chord_names))
        self.query_one("#diatonic-all-keys-panel", Static).update("\n".join(lines))

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
        self._update_chord_strip(key, quality)

    def _sync_position(self) -> None:
        self.query_one("#full-neck", FullNeckWidget).current_position = self._position

    def _update_chord_strip(self, key: str, quality: str) -> None:
        chord_quality = QUALITY_CHORD_PARENT.get(quality, quality)
        if chord_quality != quality:
            self._chord_strip_note = f"  (chords from {chord_quality})"
        elif quality == "Blues":
            self._chord_strip_note = "  (12-bar harmony)"
        else:
            self._chord_strip_note = ""
        self._chords = diatonic_chords(key, chord_quality)
        self._render_chord_strip()
        self._update_chord_detail()

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

    def _update_chord_detail(self) -> None:
        widget = self.query_one("#chord-detail", Static)
        if not self._chords:
            return
        _, chord_name = self._chords[self._chord_idx]
        entry = self.app.data_loader.chords.get(chord_name)
        if entry is None:
            widget.update(f"  {chord_name}\n  (no voicing)")
            return
        voicing = entry.voicings[0]
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
        widget.update(render_chord(spec))
