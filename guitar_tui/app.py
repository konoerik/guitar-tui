"""Guitar TUI application entry point."""

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label


class GuitarTUI(App):
    """A TUI application for guitar music theory."""

    CSS_PATH = "ui/app.tcss"
    TITLE = "Guitar TUI"
    SUB_TITLE = "Music Theory at Your Fingertips"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Guitar TUI — coming soon.", id="placeholder")
        yield Footer()


def main() -> None:
    app = GuitarTUI()
    app.run()


if __name__ == "__main__":
    main()
