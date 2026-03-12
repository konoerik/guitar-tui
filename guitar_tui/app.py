"""Guitar TUI application entry point."""

from pathlib import Path

from textual.app import App
from textual.events import Resize

from guitar_tui.loaders.data_loader import DataLoader
from guitar_tui.loaders.lick_loader import LickLoader
from guitar_tui.loaders.lesson_loader import LessonLoader
from guitar_tui.settings import AppSettings, load as load_settings, save as save_settings
from guitar_tui.ui.screens.lesson import LessonMode
from guitar_tui.ui.screens.practice import PracticeMode
from guitar_tui.ui.screens.size_warning import SizeWarningModal
from guitar_tui.ui.screens.tools import ToolsMode
from guitar_tui.ui.screens.welcome import WelcomeScreen

_CONTENT_DIR = Path(__file__).parent / "content"

# Minimum terminal dimensions for a comfortable experience.
# Adjust these after empirical testing on different setups.
MIN_COLS = 110
MIN_ROWS = 36


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
    settings: AppSettings
    _resize_timer = None

    # compose() omitted — each Screen composes its own Header/Footer

    def on_mount(self) -> None:
        self.settings = load_settings()
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
        self._validate_lick_refs()
        self.install_screen(WelcomeScreen(), name="welcome")
        self.install_screen(LessonMode(), name="lessons")
        self.install_screen(ToolsMode(), name="tools")
        self.install_screen(PracticeMode(), name="practice")
        self.push_screen("welcome")
        self._check_terminal_size()

    def _check_terminal_size(self) -> None:
        cols, rows = self.size
        if cols < MIN_COLS or rows < MIN_ROWS:
            self.push_screen(SizeWarningModal(cols, rows, MIN_COLS, MIN_ROWS))

    def on_resize(self, event: Resize) -> None:
        if self._resize_timer is not None:
            self._resize_timer.stop()
        cols, rows = event.size
        if cols < MIN_COLS or rows < MIN_ROWS:
            self._resize_timer = self.set_timer(0.5, self._notify_resize_warning)

    def _notify_resize_warning(self) -> None:
        cols, rows = self.size
        if cols < MIN_COLS or rows < MIN_ROWS:
            self.notify(
                f"Terminal too small ({cols}×{rows}) — recommended {MIN_COLS}×{MIN_ROWS}",
                severity="warning",
                timeout=4,
            )

    def _validate_lick_refs(self) -> None:
        import warnings
        known = set(self.lick_loader.licks)
        for lesson in self.lesson_loader.lessons.values():
            for slug in lesson.meta.licks:
                if slug not in known:
                    warnings.warn(
                        f"Lesson {lesson.meta.slug!r} references unknown lick {slug!r}.",
                        stacklevel=2,
                    )

    def save_settings(self) -> None:
        """Persist current settings to disk. Call after any settings mutation."""
        save_settings(self.settings)

    def action_goto_welcome(self) -> None:
        self.switch_screen("welcome")

    def action_goto_lessons(self) -> None:
        self.switch_screen("lessons")

    def action_goto_tools(self) -> None:
        self.switch_screen("tools")

    def action_goto_practice(self) -> None:
        self.switch_screen("practice")

    def action_quit(self) -> None:
        save_settings(self.settings)
        self.exit()


def main() -> None:
    app = GuitarTUI()
    app.run()


if __name__ == "__main__":
    main()
