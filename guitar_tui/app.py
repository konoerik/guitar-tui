"""Guitar TUI application entry point."""

from pathlib import Path

from textual.app import App

from guitar_tui.loaders.data_loader import DataLoader
from guitar_tui.loaders.lick_loader import LickLoader
from guitar_tui.loaders.lesson_loader import LessonLoader
from guitar_tui.ui.screens.lesson import LessonMode
from guitar_tui.ui.screens.practice import PracticeMode
from guitar_tui.ui.screens.tools import ToolsMode
from guitar_tui.ui.screens.welcome import WelcomeScreen

_CONTENT_DIR = Path(__file__).parent / "content"


class GuitarTUI(App):
    """A TUI application for guitar music theory."""

    CSS_PATH = "ui/app.tcss"
    TITLE = "Guitar TUI"
    SUB_TITLE = "Music Theory at Your Fingertips"

    BINDINGS = [
        ("1", "goto_welcome", "Home"),
        ("2", "goto_lessons", "Lessons"),
        ("3", "goto_tools", "Tools"),
        ("4", "goto_practice", "Practice"),
        ("q", "quit", "Quit"),
    ]

    data_loader: DataLoader
    lesson_loader: LessonLoader
    exercise_loader: LessonLoader
    lick_loader: LickLoader

    # compose() omitted — each Screen composes its own Header/Footer

    def on_mount(self) -> None:
        self.data_loader = DataLoader()
        self.data_loader.load()
        self.lesson_loader = LessonLoader()
        self.lesson_loader.load()
        self.exercise_loader = LessonLoader(
            lessons_dir=_CONTENT_DIR / "exercises",
            index_path=_CONTENT_DIR / "exercises" / "index.yaml",
        )
        self.exercise_loader.load()
        self.lick_loader = LickLoader()
        self.lick_loader.load()
        self.install_screen(WelcomeScreen(), name="welcome")
        self.install_screen(LessonMode(), name="lessons")
        self.install_screen(ToolsMode(), name="tools")
        self.install_screen(PracticeMode(), name="practice")
        self.push_screen("welcome")

    def action_goto_welcome(self) -> None:
        self.switch_screen("welcome")

    def action_goto_lessons(self) -> None:
        self.switch_screen("lessons")

    def action_goto_tools(self) -> None:
        self.switch_screen("tools")

    def action_goto_practice(self) -> None:
        self.switch_screen("practice")


def main() -> None:
    app = GuitarTUI()
    app.run()


if __name__ == "__main__":
    main()
