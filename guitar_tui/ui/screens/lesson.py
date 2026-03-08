"""LessonMode — full-screen lesson viewer with modal picker."""

from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown, Static

from guitar_tui.loaders.lesson_loader import DiagramBlock, ParsedLesson, TextBlock


class _LessonItem(ListItem):
    """A ListItem that carries a lesson slug."""

    def __init__(self, label: Label, slug: str) -> None:
        super().__init__(label)
        self.slug = slug


class LessonPickerModal(ModalScreen[str | None]):
    """Overlay modal for picking a lesson from the full lesson list.

    Pass ``current_slug`` to pre-scroll the list to the open lesson.
    """

    BINDINGS = [("escape", "dismiss(None)", "Close")]

    def __init__(self, current_slug: str | None = None) -> None:
        super().__init__()
        self.current_slug = current_slug

    def compose(self) -> ComposeResult:
        yield Label("Select a Lesson", id="picker-title")
        yield ListView(id="lesson-list")

    def on_mount(self) -> None:
        lv = self.query_one("#lesson-list", ListView)
        badges = {"beginner": "●", "intermediate": "◉", "advanced": "◎"}

        lv_index = 0
        slug_to_lv_index: dict[str, int] = {}

        for track, lessons in self.app.lesson_loader.ordered_track_lessons():
            lv.append(ListItem(Label(f"[bold]{track.title}[/bold]"), disabled=True))
            lv_index += 1
            for lesson in lessons:
                badge = badges.get(lesson.meta.difficulty, "○")
                item = _LessonItem(Label(f"  {badge} {lesson.meta.title}"), slug=lesson.meta.slug)
                lv.append(item)
                slug_to_lv_index[lesson.meta.slug] = lv_index
                lv_index += 1

        if self.current_slug and self.current_slug in slug_to_lv_index:
            lv.index = slug_to_lv_index[self.current_slug]

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, _LessonItem):
            self.dismiss(event.item.slug)


class LessonMode(Screen):
    """Full-screen lesson viewer. Press / to open lesson picker."""

    BINDINGS = [
        ("slash", "open_picker", "Open Lesson"),
        ("[", "prev_lesson", "Previous"),
        ("]", "next_lesson", "Next"),
        ("escape", "back", "Back"),
    ]

    _current_slug: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(id="lesson-body")
        yield Footer()

    def on_mount(self) -> None:
        self._show_overview()

    def action_back(self) -> None:
        if self._current_slug is not None:
            self._current_slug = None
            self.app.sub_title = "Music Theory at Your Fingertips"
            self._show_overview()
        else:
            self.app.action_goto_welcome()

    async def action_open_picker(self) -> None:
        await self.app.push_screen(
            LessonPickerModal(current_slug=self._current_slug),
            self._on_lesson_picked,
        )

    async def action_prev_lesson(self) -> None:
        lesson = self._adjacent_lesson(offset=-1)
        if lesson is not None:
            await self._load_lesson(lesson)

    async def action_next_lesson(self) -> None:
        lesson = self._adjacent_lesson(offset=1)
        if lesson is not None:
            await self._load_lesson(lesson)

    def _adjacent_lesson(self, offset: int) -> ParsedLesson | None:
        """Return the lesson ``offset`` steps from the current one, or None."""
        if self._current_slug is None:
            return None
        ordered = self.app.lesson_loader.ordered_lessons()
        slugs = [l.meta.slug for l in ordered]
        try:
            idx = slugs.index(self._current_slug)
        except ValueError:
            return None
        target = idx + offset
        if 0 <= target < len(ordered):
            return ordered[target]
        return None

    async def _on_lesson_picked(self, slug: str | None) -> None:
        if slug is None:
            return
        lesson = self.app.lesson_loader.lessons[slug]
        await self._load_lesson(lesson)

    def _show_overview(self) -> None:
        body = self.query_one("#lesson-body", ScrollableContainer)
        body.remove_children()
        body.mount(Markdown(self._build_overview_md(), classes="lesson-overview"))

    def _build_overview_md(self) -> str:
        loader = self.app.lesson_loader
        lines: list[str] = []
        if loader.overview:
            lines.append(f"# {loader.overview.title}\n")
            lines.append(f"{loader.overview.body}\n")
            lines.append("---\n")
        lines.append("Press **/** to open a lesson.\n")
        for i, (track, lessons) in enumerate(
            loader.ordered_track_lessons(), start=1
        ):
            count = len(lessons)
            noun = "lesson" if count == 1 else "lessons"
            lines.append("---\n")
            lines.append(f"### {i}. {track.title}  ·  *{count} {noun}*\n")
            if track.description:
                lines.append(f"{track.description}\n")
        return "\n".join(lines)

    async def _load_lesson(self, lesson: ParsedLesson) -> None:
        self._current_slug = lesson.meta.slug
        body = self.query_one("#lesson-body", ScrollableContainer)
        await body.remove_children()
        if lesson.meta.summary:
            await body.mount(Static(lesson.meta.summary, classes="lesson-summary"))
        for block in lesson.body:
            if isinstance(block, TextBlock):
                await body.mount(Markdown(block.content, classes="lesson-text"))
            elif isinstance(block, DiagramBlock):
                await body.mount(Static(block.rendered, classes="lesson-diagram"))
        if lesson.meta.see_also:
            titles: list[str] = []
            for slug in lesson.meta.see_also:
                ref_lesson = self.app.lesson_loader.lessons.get(slug)
                if ref_lesson:
                    titles.append(ref_lesson.meta.title)
            if titles:
                see_also_md = "---\n\n**See Also:** " + ", ".join(titles)
                await body.mount(Markdown(see_also_md, classes="lesson-text"))
        body.scroll_home(animate=False)
        self.app.sub_title = lesson.meta.title
