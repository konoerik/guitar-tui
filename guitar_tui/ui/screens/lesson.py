"""LessonScreen — displays a single parsed lesson."""

from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, Static

from guitar_tui.loaders.lesson_loader import DiagramBlock, ParsedLesson, TextBlock


class LessonScreen(Screen):
    """Renders lesson body blocks: prose as Markdown, diagrams as Static."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, lesson: ParsedLesson) -> None:
        super().__init__()
        self._lesson = lesson

    def compose(self) -> ComposeResult:
        yield Header()
        with ScrollableContainer(id="lesson-body"):
            for block in self._lesson.body:
                if isinstance(block, TextBlock):
                    yield Markdown(block.content, classes="lesson-text")
                elif isinstance(block, DiagramBlock):
                    yield Static(block.rendered, classes="lesson-diagram")
        yield Footer()

    def on_mount(self) -> None:
        self.app.sub_title = self._lesson.meta.title

    def on_unmount(self) -> None:
        self.app.sub_title = "Music Theory at Your Fingertips"
