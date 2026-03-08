"""WelcomeScreen — home base, shows navigation guide."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

_SEP = "─" * 56

_WELCOME = f"""\
[bold]Guitar TUI[/bold]
guitar music theory in a shell

[dim]Assumes you can already form basic open chord shapes.
New to guitar entirely? Start with a beginner course first, then return.[/dim]

{_SEP}

  11 tracks  ·  78 lessons  ·  beginner → advanced

  Phase 1   Tracks 1–3    Playing foundation
            Read notation · Build open chord shapes · Play real progressions

  Phase 2   Tracks 4–9    Vocabulary expansion
            Theory · Barre chords · Three scale tracks · Seventh chords

  Phase 3   Tracks 10–11  Synthesis and application
            Modes as a unified system · Song analysis · A method, not just facts

{_SEP}

  [bold][2] Lessons[/bold]     structured curriculum from open chords to song analysis
  [bold][3] Tools[/bold]       key view · scale explorer · chord reference · tuning guide
  [bold][4] Practice[/bold]    technique exercises · licks library with backing chords

  [bold][q] Quit[/bold]

  [dim]New here?  Press [bold]2[/bold], then [bold]/[/bold] — start with Track 1: Orientation.[/dim]
"""


class WelcomeScreen(Screen):
    """Home base screen showing navigation guide."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(_WELCOME, id="welcome-content")
        yield Footer()
