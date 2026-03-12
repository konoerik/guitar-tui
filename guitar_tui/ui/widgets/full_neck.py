"""FullNeckWidget — renders the complete guitar neck for a scale.

All positions are shown simultaneously; a bracket indicator marks whichever
position is currently selected.  Notes that fall outside 0–MAX_FRET after
transposition wrap cyclically (per position, not per note) so every position
is always visible.
"""

from __future__ import annotations

from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

from guitar_tui.theory.keys import note_to_semitone

# String labels displayed top-to-bottom (string 1 = high e, 6 = low E).
_LABELS: dict[int, str] = {1: "e", 2: "B", 3: "G", 4: "D", 5: "A", 6: "E"}

# Column layout constants.
_PREFIX   = 4
_COL      = 4
_MAX_FRET = 15
_FRETS    = _MAX_FRET + 1


def _col_start(fret: int) -> int:
    return _PREFIX + fret * _COL


def _position_shift(lo: int, hi: int) -> int:
    shift = 0
    while hi + shift > _MAX_FRET:
        shift -= 12
    while lo + shift < 0:
        shift += 12
    # Prefer the lowest valid placement on the neck.
    while lo + shift - 12 >= 0:
        shift -= 12
    return shift


_DARK_COLORS  = {"root": "bold red",      "tone": "cyan",      "bracket": "yellow"}
_LIGHT_COLORS = {"root": "bold dark_red", "tone": "dark_cyan", "bracket": "dark_goldenrod"}


class FullNeckWidget(Static):
    """Full-neck diagram that redraws on key/scale/position changes."""

    root_note:        reactive[str] = reactive("A",             layout=True)
    scale_name:       reactive[str] = reactive("natural_minor", layout=True)
    current_position: reactive[int] = reactive(1,              layout=True)

    def on_mount(self) -> None:
        self.watch(self.app, "theme", self._on_theme_changed)
        self._refresh()

    def _on_theme_changed(self, _: str) -> None:
        self._refresh()

    def _colors(self) -> dict[str, str]:
        return _DARK_COLORS if self.app.current_theme.dark else _LIGHT_COLORS

    def watch_root_note(self, _: str) -> None:
        self._refresh()

    def watch_scale_name(self, _: str) -> None:
        self._refresh()

    def watch_current_position(self, _: int) -> None:
        self._refresh()

    def _refresh(self) -> None:
        self.update(self._build())

    def _build(self) -> Text:
        loader = self.app.data_loader
        if self.scale_name not in loader.scales:
            return Text(f"  (scale '{self.scale_name}' not loaded)")

        scale  = loader.scales[self.scale_name]
        offset = (note_to_semitone(self.root_note) - note_to_semitone(scale.key)) % 12
        colors = self._colors()

        # Build note map — all notes in a position shifted as a unit.
        note_map: dict[tuple[int, int], bool] = {}
        pos_ranges: list[tuple[int, int]] = []
        for pos in scale.positions:
            lo_raw = pos.fret_range[0] + offset
            hi_raw = pos.fret_range[1] + offset
            shift  = _position_shift(lo_raw, hi_raw)
            for note in pos.notes:
                nf = note.fret + offset + shift
                if 0 <= nf <= _MAX_FRET:
                    existing = note_map.get((note.string, nf), False)
                    note_map[(note.string, nf)] = note.root or existing
            pos_ranges.append((lo_raw + shift, hi_raw + shift))

        n_pos   = len(pos_ranges)
        cur_idx = max(0, min(self.current_position - 1, n_pos - 1))

        t = Text()

        # Fret-number header
        t.append("    " + "".join(f"{f:^4}" for f in range(_FRETS)) + "\n")

        # One row per string
        for string in range(1, 7):
            label = _LABELS[string]
            t.append(f" {label}  ")
            for fret in range(_FRETS):
                key = (string, fret)
                t.append("─")
                if key in note_map:
                    if note_map[key]:
                        t.append("■", style=colors["root"])
                    else:
                        t.append("●", style=colors["tone"])
                else:
                    t.append("│" if fret == 0 else "┼")
                t.append("──")
            t.append("\n")

        # Position bracket
        bracket = _bracket(pos_ranges[cur_idx], cur_idx + 1, n_pos)
        t.append(bracket + "\n", style=colors["bracket"])

        # Legend
        t.append("\n  ")
        t.append("■", style=colors["root"])
        t.append(f" root ({self.root_note})   ")
        t.append("●", style=colors["tone"])
        t.append(f" scale tone   ◀ [ / ] ▶   position {cur_idx + 1} of {n_pos}")

        return t


def _bracket(fret_range: tuple[int, int], cur: int, total: int) -> str:
    lo = max(0, fret_range[0])
    hi = min(_MAX_FRET, fret_range[1])

    if lo > hi or lo > _MAX_FRET:
        return f"    (position {cur} outside visible range)"

    start = _col_start(lo)
    end   = _col_start(hi) + _COL - 1
    inner = end - start - 1

    label = f" pos {cur}/{total} "
    if len(label) <= inner:
        pad  = inner - len(label)
        fill = "─" * (pad // 2) + label + "─" * (pad - pad // 2)
    else:
        fill = "─" * inner

    return " " * start + "╰" + fill + "╯"
