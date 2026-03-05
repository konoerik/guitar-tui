"""Guitar TUI application entry point."""

from textual.app import App, ComposeResult

from guitar_tui.loaders.data_loader import DataLoader
from guitar_tui.loaders.lesson_loader import LessonLoader
from guitar_tui.ui.screens.lesson import LessonMode
from guitar_tui.ui.screens.tools import ToolsMode
from guitar_tui.ui.screens.welcome import WelcomeScreen


class GuitarTUI(App):
    """A TUI application for guitar music theory."""

    CSS_PATH = "ui/app.tcss"
    TITLE = "Guitar TUI"
    SUB_TITLE = "Music Theory at Your Fingertips"

    BINDINGS = [
        ("1", "goto_welcome", "Home"),
        ("2", "goto_lessons", "Lessons"),
        ("3", "goto_tools", "Tools"),
        ("q", "quit", "Quit"),
    ]

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
        self.install_screen(WelcomeScreen(), name="welcome")
        self.install_screen(LessonMode(), name="lessons")
        self.install_screen(ToolsMode(), name="tools")
        self.push_screen("welcome")

    def action_goto_welcome(self) -> None:
        self.switch_screen("welcome")

    def action_goto_lessons(self) -> None:
        self.switch_screen("lessons")

    def action_goto_tools(self) -> None:
        self.switch_screen("tools")


def main() -> None:
    app = GuitarTUI()
    app.run()


if __name__ == "__main__":
    main()
