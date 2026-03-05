"""LessonMode — full-screen lesson viewer with modal picker."""

from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown, Static

from guitar_tui.loaders.lesson_loader import DiagramBlock, ParsedLesson, TextBlock


class LessonPickerModal(ModalScreen[str | None]):
    """Overlay modal for picking a lesson from the full lesson list."""

    BINDINGS = [("escape", "dismiss(None)", "Close")]

    def compose(self) -> ComposeResult:
        yield Label("Select a Lesson", id="picker-title")
        yield ListView(id="lesson-list")

    def on_mount(self) -> None:
        lv = self.query_one("#lesson-list", ListView)
        badges = {"beginner": "●", "intermediate": "◉", "advanced": "◎"}

        by_module: dict[str, list[ParsedLesson]] = {}
        for lesson in self.app.lesson_loader.lessons.values():
            key = lesson.meta.module or "general"
            by_module.setdefault(key, []).append(lesson)

        for module_key in sorted(by_module):
            display = module_key.replace("-", " ").replace("_", " ").title()
            lv.append(ListItem(Label(f"[bold]{display}[/bold]"), disabled=True))
            sorted_lessons = sorted(
                by_module[module_key],
                key=lambda l: (l.meta.position or 9999, l.meta.title),
            )
            for lesson in sorted_lessons:
                badge = badges.get(lesson.meta.difficulty, "○")
                item = ListItem(Label(f"  {badge} {lesson.meta.title}"))
                item.data = lesson.meta.slug  # type: ignore[attr-defined]
                lv.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        slug = getattr(event.item, "data", None)
        if slug is not None:
            self.dismiss(slug)


class LessonMode(Screen):
    """Full-screen lesson viewer. Press / to open lesson picker."""

    BINDINGS = [
        ("slash", "open_picker", "Open Lesson"),
        ("escape", "app.goto_welcome", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            "Press [bold]/[/bold] to open the lesson picker.",
            id="lesson-hint",
        )
        yield ScrollableContainer(id="lesson-body")
        yield Footer()

    async def action_open_picker(self) -> None:
        await self.app.push_screen(LessonPickerModal(), self._on_lesson_picked)

    async def _on_lesson_picked(self, slug: str | None) -> None:
        if slug is None:
            return
        lesson = self.app.lesson_loader.lessons[slug]
        await self._load_lesson(lesson)

    async def _load_lesson(self, lesson: ParsedLesson) -> None:
        hint = self.query_one("#lesson-hint", Static)
        hint.display = False
        body = self.query_one("#lesson-body", ScrollableContainer)
        await body.remove_children()
        for block in lesson.body:
            if isinstance(block, TextBlock):
                await body.mount(Markdown(block.content, classes="lesson-text"))
            elif isinstance(block, DiagramBlock):
                await body.mount(Static(block.rendered, classes="lesson-diagram"))
        self.app.sub_title = lesson.meta.title
