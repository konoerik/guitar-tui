"""PracticeMode — Exercises and Licks Library."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Markdown, Static, Tree

from guitar_tui.loaders.lesson_loader import DiagramBlock, ParsedLesson, TextBlock
from guitar_tui.loaders.lick_loader import ParsedLick

_MODULE_ORDER = [
    "technique", "open-chords", "natural-minor",
    "major-scale", "seventh-chords",
]
_MODULE_LABELS = {
    "technique":      "Technique",
    "open-chords":    "Open Chords",
    "natural-minor":  "Natural Minor",
    "major-scale":    "Major Scale",
    "seventh-chords": "Seventh Chords",
}
_DIFF_BADGE = {"beginner": "●", "intermediate": "◉", "advanced": "◎"}


class PracticeMode(Screen):
    """Card-panel practice screen: tree nav on the left, content on the right."""

    BINDINGS = [("escape", "app.goto_welcome", "Back")]

    def compose(self) -> ComposeResult:
        with Horizontal(id="practice-frame"):
            with VerticalScroll(id="practice-nav"):
                yield Tree("Practice", id="practice-tree")
            with Vertical(id="practice-content"):
                yield ScrollableContainer(id="practice-body")
        yield Footer()

    def on_mount(self) -> None:
        self._build_tree()
        self.query_one("#practice-nav").border_title = "Practice"
        self.query_one("#practice-content").border_title = "Practice"
        self._show_overview()
        self.query_one("#practice-body", ScrollableContainer).focus()

    # ── Tree ──────────────────────────────────────────────────────────────────

    def _build_tree(self) -> None:
        tree = self.query_one("#practice-tree", Tree)
        tree.show_root = False

        tree.root.add_leaf("Introduction", data=("overview",))
        tree.root.add_leaf("", data=None)  # spacer

        # Exercises branch
        ex_branch = tree.root.add("Exercises", expand=False)
        grouped: dict[str, list[ParsedLesson]] = {}
        for lesson in self.app.exercise_loader.lessons.values():
            key = lesson.meta.module or "other"
            grouped.setdefault(key, []).append(lesson)

        ordered = [m for m in _MODULE_ORDER if m in grouped]
        extras  = sorted(m for m in grouped if m not in _MODULE_ORDER)
        for module in ordered + extras:
            label = _MODULE_LABELS.get(module, module.replace("-", " ").title())
            exercises = sorted(
                grouped[module],
                key=lambda l: (l.meta.position if l.meta.position is not None else 9999, l.meta.title),
            )
            cat = ex_branch.add(label, expand=False)
            for ex in exercises:
                badge = _DIFF_BADGE.get(ex.meta.difficulty, "○")
                cat.add_leaf(f"{badge} {ex.meta.title}", data=("exercise", ex.meta.slug))

        # Licks branch
        lick_branch = tree.root.add("Licks", expand=False)
        for category_label, licks in self.app.lick_loader.by_category():
            cat = lick_branch.add(category_label, expand=False)
            for lick in licks:
                badge = _DIFF_BADGE.get(lick.meta.difficulty, "○")
                cat.add_leaf(f"{badge} {lick.meta.title}", data=("lick", lick.meta.slug))

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        data = event.node.data
        if data is None:
            return
        kind = data[0]
        if kind == "overview":
            self.query_one("#practice-content").border_title = "Practice"
            self._show_overview()
        elif kind == "exercise":
            ex = self.app.exercise_loader.lessons.get(data[1])
            if ex:
                self.query_one("#practice-content").border_title = ex.meta.title
                await self._show_exercise(ex)
        elif kind == "lick":
            lick = self.app.lick_loader.licks.get(data[1])
            if lick:
                self.query_one("#practice-content").border_title = lick.meta.title
                await self._show_lick(lick)

    # ── Content rendering ─────────────────────────────────────────────────────

    def _show_overview(self) -> None:
        body = self.query_one("#practice-body", ScrollableContainer)
        body.remove_children()
        ex_count   = len(self.app.exercise_loader.lessons)
        lick_count = len(self.app.lick_loader.licks)
        md = (
            "# Practice\n\n"
            f"{ex_count} exercises · {lick_count} licks\n\n"
            "---\n\n"
            "**Exercises** are technique drills. Use them with a metronome "
            "at the BPM specified in each exercise before moving on.\n\n"
            "**Licks** are musical phrases with backing chord suggestions. "
            "Record the backing on a looper and practice the phrase over it. "
            "Focus on expression — tone, timing, and dynamics — not just the notes.\n\n"
            "Expand **Exercises** or **Licks** in the tree to browse by category."
        )
        body.mount(Markdown(md, classes="lesson-overview"))

    async def _show_exercise(self, ex: ParsedLesson) -> None:
        body = self.query_one("#practice-body", ScrollableContainer)
        await body.remove_children()
        widgets = []
        if ex.meta.summary:
            widgets.append(Static(ex.meta.summary, classes="lesson-summary"))
        for block in ex.body:
            if isinstance(block, TextBlock):
                widgets.append(Markdown(block.content, classes="lesson-text"))
            elif isinstance(block, DiagramBlock):
                widgets.append(Static(block.rendered, classes="lesson-diagram"))
        if widgets:
            await body.mount(*widgets)
        body.scroll_home(animate=False)

    async def _show_lick(self, lick: ParsedLick) -> None:
        body = self.query_one("#practice-body", ScrollableContainer)
        await body.remove_children()

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

        await body.mount(*widgets)
        body.scroll_home(animate=False)
