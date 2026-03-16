"""LessonMode — card-panel lesson viewer with inline track tree."""

from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Markdown, Static, TabbedContent, TabPane, Tree

from guitar_tui.loaders.lesson_loader import DiagramBlock, ParsedLesson, TextBlock
from guitar_tui.loaders.lick_loader import ParsedLick

_OVERVIEW_SENTINEL = "__overview__"
_SEP_SENTINEL      = "__sep__"

_DIFF_BADGE = {"beginner": "●", "intermediate": "◉", "advanced": "◎"}


class LessonMode(Screen):
    """Two-panel lesson viewer: track tree on the left, three-tab content on the right."""

    BINDINGS = [
        ("escape", "back", "Back"),
    ]

    _current_slug: str | None = None

    def compose(self) -> ComposeResult:
        with Horizontal(id="lessons-frame"):
            with VerticalScroll(id="lessons-nav"):
                yield Tree("Tracks", id="lessons-tree")
            with Vertical(id="lessons-content"):
                with TabbedContent(id="lesson-tabs"):
                    with TabPane("Lesson", id="tab-lesson"):
                        yield ScrollableContainer(id="lesson-body")
                    with TabPane("Exercises", id="tab-drills"):
                        yield ScrollableContainer(id="drills-body")
                    with TabPane("Licks", id="tab-licks"):
                        yield ScrollableContainer(id="licks-body")
        yield Footer()

    def on_mount(self) -> None:
        self._build_tree()
        self.query_one("#lessons-nav").border_title = "Tracks"
        self.query_one("#lessons-content").border_title = "Lessons"
        self._show_overview()
        self.query_one("#lesson-body", ScrollableContainer).focus()

    # ── Tree ──────────────────────────────────────────────────────────────────

    def _build_tree(self) -> None:
        tree = self.query_one("#lessons-tree", Tree)
        tree.show_root = False
        tree.root.add_leaf("Introduction", data=_OVERVIEW_SENTINEL)
        tree.root.add_leaf("", data=_SEP_SENTINEL)
        badges = {"beginner": "●", "intermediate": "◉", "advanced": "◎"}
        for i, (track, lessons) in enumerate(
            self.app.lesson_loader.ordered_track_lessons(), start=1
        ):
            branch = tree.root.add(f"{i:02d}. {track.title}", expand=False)
            for lesson in lessons:
                badge = badges.get(lesson.meta.difficulty, "○")
                branch.add_leaf(f"{badge} {lesson.meta.title}", data=lesson.meta.slug)

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        data = event.node.data
        if data == _OVERVIEW_SENTINEL:
            self._current_slug = None
            self.query_one("#lessons-content").border_title = "Lessons"
            self._show_overview()
        elif data is not None and data != _SEP_SENTINEL:
            lesson = self.app.lesson_loader.lessons.get(data)
            if lesson:
                await self._load_lesson(lesson)

    # ── Navigation ────────────────────────────────────────────────────────────

    def action_back(self) -> None:
        if self._current_slug is not None:
            self._current_slug = None
            self.query_one("#lessons-content").border_title = "Lessons"
            self._show_overview()

    # ── Overview (no lesson selected) ─────────────────────────────────────────

    def _show_overview(self) -> None:
        loader = self.app.lesson_loader
        total = sum(len(ls) for _, ls in loader.ordered_track_lessons())
        track_count = len(loader.tracks)
        intro = (
            f"# Introduction\n\n"
            f"{track_count} tracks · {total} lessons · beginner → advanced\n\n"
            "---\n\n"
        )
        if loader.overview:
            intro += f"{loader.overview.body}\n\n---\n\n"
        intro += "Expand a track on the left to see its lessons, then select one to begin."

        lesson_body = self.query_one("#lesson-body", ScrollableContainer)
        lesson_body.remove_children()
        lesson_body.mount(Markdown(intro, classes="lesson-overview"))

        drills_body = self.query_one("#drills-body", ScrollableContainer)
        drills_body.remove_children()
        drills_body.mount(Markdown(
            "*Select a lesson to see related exercises.*",
            classes="lesson-overview",
        ))

        licks_body = self.query_one("#licks-body", ScrollableContainer)
        licks_body.remove_children()
        licks_body.mount(Markdown(
            "*Select a lesson to see related licks.*",
            classes="lesson-overview",
        ))

    # ── Lesson loading ────────────────────────────────────────────────────────

    async def _load_lesson(self, lesson: ParsedLesson) -> None:
        self._current_slug = lesson.meta.slug
        self.query_one("#lessons-content").border_title = lesson.meta.title

        tabs = self.query_one("#lesson-tabs", TabbedContent)
        # Orientation is informational — no drills or licks apply yet.
        # Future: replace this with per-exercise prerequisite tags (option C).
        practice_tabs_visible = lesson.meta.module != "orientation"
        if practice_tabs_visible:
            tabs.show_tab("tab-drills")
            tabs.show_tab("tab-licks")
        else:
            tabs.hide_tab("tab-drills")
            tabs.hide_tab("tab-licks")

        await self._render_lesson_tab(lesson)
        if practice_tabs_visible:
            await self._render_drills_tab(lesson)
            await self._render_licks_tab(lesson)

        # Switch to Lesson tab, scroll to top, and focus content
        tabs.active = "tab-lesson"
        body = self.query_one("#lesson-body", ScrollableContainer)
        body.scroll_home(animate=False)
        body.focus()

    async def _render_lesson_tab(self, lesson: ParsedLesson) -> None:
        body = self.query_one("#lesson-body", ScrollableContainer)
        await body.remove_children()
        widgets = []
        if lesson.meta.summary:
            widgets.append(Static(lesson.meta.summary, classes="lesson-summary"))
        for block in lesson.body:
            if isinstance(block, TextBlock):
                widgets.append(Markdown(block.content, classes="lesson-text"))
            elif isinstance(block, DiagramBlock):
                widgets.append(Static(block.rendered, classes="lesson-diagram"))
        if lesson.meta.see_also:
            titles = [
                self.app.lesson_loader.lessons[s].meta.title
                for s in lesson.meta.see_also
                if s in self.app.lesson_loader.lessons
            ]
            if titles:
                widgets.append(Markdown(
                    "---\n\n**See Also:** " + ", ".join(titles),
                    classes="lesson-text",
                ))
        if lesson.meta.licks:
            lick_titles = [
                self.app.lick_loader.licks[s].meta.title
                for s in lesson.meta.licks
                if s in self.app.lick_loader.licks
            ]
            if lick_titles:
                widgets.append(Markdown(
                    "**Practice:** " + "  ·  ".join(lick_titles) + "  — see **[4] Practice**",
                    classes="lesson-text",
                ))
        if widgets:
            await body.mount(*widgets)

    async def _render_drills_tab(self, lesson: ParsedLesson) -> None:
        body = self.query_one("#drills-body", ScrollableContainer)
        await body.remove_children()

        module = lesson.meta.module or ""
        all_exercises = list(self.app.exercise_loader.lessons.values())

        # Track-specific exercises first, then technique (universal warmups)
        specific  = [e for e in all_exercises if e.meta.module == module and module]
        technique = [e for e in all_exercises if e.meta.module == "technique"]
        exercises = sorted(specific, key=lambda e: (e.meta.position if e.meta.position is not None else 9999, e.meta.title)) + \
                    sorted(technique, key=lambda e: (e.meta.position if e.meta.position is not None else 9999, e.meta.title))

        if not exercises:
            await body.mount(Markdown(
                "*No exercises for this track yet.*",
                classes="lesson-overview",
            ))
            return

        widgets = []
        for ex in exercises:
            widgets.append(Static(f"[bold]{ex.meta.title}[/bold]", classes="section-title"))
            if ex.meta.summary:
                widgets.append(Static(ex.meta.summary, classes="lesson-summary"))
            for block in ex.body:
                if isinstance(block, TextBlock):
                    widgets.append(Markdown(block.content, classes="lesson-text"))
                elif isinstance(block, DiagramBlock):
                    widgets.append(Static(block.rendered, classes="lesson-diagram"))
            widgets.append(Static("", classes="section-spacer"))

        await body.mount(*widgets)
        body.scroll_home(animate=False)

    async def _render_licks_tab(self, lesson: ParsedLesson) -> None:
        body = self.query_one("#licks-body", ScrollableContainer)
        await body.remove_children()

        lick_slugs = lesson.meta.licks
        licks = [
            self.app.lick_loader.licks[s]
            for s in lick_slugs
            if s in self.app.lick_loader.licks
        ]

        if not licks:
            await body.mount(Markdown(
                "*No licks for this lesson. "
                "Browse the full library in* **[4] Practice**.",
                classes="lesson-overview",
            ))
            return

        widgets = []
        for lick in licks:
            widgets.extend(self._lick_widgets(lick))
            widgets.append(Static("", classes="section-spacer"))

        await body.mount(*widgets)
        body.scroll_home(animate=False)

    @staticmethod
    def _lick_widgets(lick: ParsedLick) -> list:
        badge   = _DIFF_BADGE.get(lick.meta.difficulty, "○")
        backing = "  ·  ".join(lick.meta.backing_chords)
        prog    = f"  ({lick.meta.backing_progression})" if lick.meta.backing_progression else ""
        tags    = "  ".join(f"[{t}]" for t in lick.meta.tags)
        header  = (
            f"{badge}  {lick.meta.title}\n"
            f"Key: {lick.meta.key}   Scale: {lick.meta.scale.replace('_', ' ')}\n"
            f"Looper: {backing}{prog}\n"
            f"Style: {tags}"
        )
        widgets = [Static(header, classes="lesson-summary")]
        if lick.meta.summary:
            widgets.append(Static(lick.meta.summary, classes="lick-summary"))
        for block in lick.body:
            if isinstance(block, TextBlock):
                widgets.append(Markdown(block.content, classes="lesson-text"))
            elif isinstance(block, DiagramBlock):
                widgets.append(Static(block.rendered, classes="lesson-diagram"))
        return widgets
