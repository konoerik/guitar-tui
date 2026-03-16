"""MetronomeWidget — visual beat indicator with BPM and time-signature control."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

_MIN_BPM = 20
_MAX_BPM = 300
_MIN_BEATS = 1
_MAX_BEATS = 12

# (max_bpm_inclusive, Italian tempo marking)
_TEMPO_MARKS: list[tuple[int, str]] = [
    (24,  "Larghissimo"),
    (40,  "Largo"),
    (55,  "Lento"),
    (65,  "Adagio"),
    (76,  "Andante"),
    (108, "Moderato"),
    (120, "Allegretto"),
    (156, "Allegro"),
    (176, "Vivace"),
    (200, "Presto"),
    (300, "Prestissimo"),
]


def _tempo_name(bpm: int) -> str:
    for threshold, name in _TEMPO_MARKS:
        if bpm <= threshold:
            return name
    return "Prestissimo"


class MetronomeWidget(Widget):
    """Visual metronome: beat display, BPM control.

    Timer is attached to the widget — it keeps ticking when you navigate
    to another Tools pane and is still running when you come back.
    """

    can_focus = True

    BINDINGS = [
        ("space", "toggle", "Start / Stop"),
        ("up", "bpm_up", "BPM +1"),
        ("down", "bpm_down", "BPM −1"),
        ("right", "bpm_up_10", "BPM +10"),
        ("left", "bpm_down_10", "BPM −10"),
        ("plus", "beats_up", "Beats +"),
        ("underscore", "beats_down", "Beats −"),
    ]

    bpm: reactive[int] = reactive(80)
    beats: reactive[int] = reactive(4)
    current_beat: reactive[int] = reactive(0)
    running: reactive[bool] = reactive(False)

    def __init__(self) -> None:
        super().__init__()
        self._timer = None

    def compose(self) -> ComposeResult:
        yield Static("", id="metro-beat-row")
        yield Static("", id="metro-info-row")
        yield Static("", id="metro-hint-row")

    def on_mount(self) -> None:
        self.bpm = self.app.settings.metronome_bpm
        self.beats = self.app.settings.metronome_time_sig[0]
        self._update_display()

    def on_unmount(self) -> None:
        self._stop_timer()

    # ── Reactive watchers ─────────────────────────────────────────────────────

    def watch_bpm(self, bpm: int) -> None:
        self._update_display()
        if self.running:
            self._stop_timer()
            self._start_timer()

    def watch_beats(self, beats: int) -> None:
        self.current_beat = 0
        self._update_display()

    def watch_current_beat(self, _: int) -> None:
        self._update_display()

    def watch_running(self, _: bool) -> None:
        self._update_display()

    # ── Actions ───────────────────────────────────────────────────────────────

    def action_toggle(self) -> None:
        if self.running:
            self._stop_timer()
            self.running = False
            self.current_beat = 0
            self.app.settings.metronome_bpm = self.bpm
            self.app.save_settings()
        else:
            self.current_beat = 0
            self.running = True
            self._start_timer()

    def action_bpm_up(self) -> None:
        self.bpm = min(_MAX_BPM, self.bpm + 1)

    def action_bpm_down(self) -> None:
        self.bpm = max(_MIN_BPM, self.bpm - 1)

    def action_bpm_up_10(self) -> None:
        self.bpm = min(_MAX_BPM, self.bpm + 10)

    def action_bpm_down_10(self) -> None:
        self.bpm = max(_MIN_BPM, self.bpm - 10)

    def action_beats_up(self) -> None:
        self.beats = min(_MAX_BEATS, self.beats + 1)

    def action_beats_down(self) -> None:
        self.beats = max(_MIN_BEATS, self.beats - 1)

    # ── Timer ─────────────────────────────────────────────────────────────────

    def _start_timer(self) -> None:
        self._timer = self.set_interval(60.0 / self.bpm, self._tick)

    def _stop_timer(self) -> None:
        if self._timer is not None:
            self._timer.stop()
            self._timer = None

    def _tick(self) -> None:
        self.current_beat = (self.current_beat + 1) % self.beats

    # ── Display ───────────────────────────────────────────────────────────────

    def _update_display(self) -> None:
        try:
            self._render_beat_row()
            self._render_info_row()
            self._render_hint_row()
        except Exception:
            pass  # widget may not be mounted yet

    def _render_beat_row(self) -> None:
        # Left box: odd beats (index 0, 2, 4...) — red on beat 1, green on beat 3+
        # Right box: even beats (index 1, 3, 5...) — always green
        left_active  = self.running and (self.current_beat % 2 == 0)
        right_active = self.running and (self.current_beat % 2 == 1)
        is_downbeat  = self.current_beat == 0

        if left_active and is_downbeat:
            left_mid = "│  [bold red]◆[/bold red]  │"
        elif left_active:
            left_mid = "│  [bold green]◆[/bold green]  │"
        else:
            left_mid = "│  [dim]◇[/dim]  │"

        if right_active:
            right_mid = "│  [bold green]●[/bold green]  │"
        else:
            right_mid = "│  [dim]○[/dim]  │"

        off_label = f"beat 2–{self.beats}" if self.beats > 2 else "beat 2"

        sep = "        "
        lines = [
            f"  ╭─────╮{sep}╭─────╮",
            f"  {left_mid}{sep}{right_mid}",
            f"  ╰─────╯{sep}╰─────╯",
            f"  [dim]beat 1, 3…  {sep}{off_label}[/dim]",
        ]
        self.query_one("#metro-beat-row", Static).update(
            "\n" + "\n".join(lines) + "\n"
        )

    def _render_info_row(self) -> None:
        status = "[green]▶ running[/green]" if self.running else "[dim]■ stopped[/dim]"
        tempo = _tempo_name(self.bpm)
        self.query_one("#metro-info-row", Static).update(
            f"\n  [bold]{tempo}[/bold]   ·   {self.bpm} BPM   ·   {self.beats}/4   ·   {status}\n"
        )

    def _render_hint_row(self) -> None:
        self.query_one("#metro-hint-row", Static).update(
            "\n"
            "  [dim]Space[/dim]  start / stop\n"
            "  [dim]↑ ↓[/dim]   BPM ± 1\n"
            "  [dim]← →[/dim]   BPM ± 10\n"
            "  [dim]+ _[/dim]   beats per bar\n"
        )
