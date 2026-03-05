"""WelcomeScreen — home base, shows navigation guide."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

_WELCOME = """\
[bold]Guitar TUI[/bold]
Music Theory at Your Fingertips


  [bold][1] Home[/bold]        This screen

  [bold][2] Lessons[/bold]    Structured lessons from open chords to modes

  [bold][3] Tools[/bold]      Chord finder, scale finder, tuning reference

  [bold][q] Quit[/bold]
"""


class WelcomeScreen(Screen):
    """Home base screen showing navigation guide."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(_WELCOME, id="welcome-content")
        yield Footer()
