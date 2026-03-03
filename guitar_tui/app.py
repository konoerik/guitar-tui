"""Guitar TUI application entry point."""

from textual.app import App, ComposeResult

from guitar_tui.loaders.data_loader import DataLoader
from guitar_tui.loaders.lesson_loader import LessonLoader
from guitar_tui.ui.screens.home import HomeScreen


class GuitarTUI(App):
    """A TUI application for guitar music theory."""

    CSS_PATH = "ui/app.tcss"
    TITLE = "Guitar TUI"
    SUB_TITLE = "Music Theory at Your Fingertips"
    data_loader: DataLoader
    lesson_loader: LessonLoader

    def compose(self) -> ComposeResult:
        return
        yield  # empty; each Screen composes its own Header/Footer

    def on_mount(self) -> None:
        self.data_loader = DataLoader()
        self.data_loader.load()
        self.lesson_loader = LessonLoader()
        self.lesson_loader.load()
        self.push_screen(HomeScreen())


def main() -> None:
    app = GuitarTUI()
    app.run()


if __name__ == "__main__":
    main()
