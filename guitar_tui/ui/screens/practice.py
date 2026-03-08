"""PracticeMode — Exercises and Licks Library."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown, Static, TabbedContent, TabPane

from guitar_tui.loaders.lesson_loader import DiagramBlock, TextBlock
from guitar_tui.loaders.lick_loader import ParsedLick


# ── Lick list item ──────────────────────────────────────────────────────────────


class _LickItem(ListItem):
    """A ListView item that carries a lick slug."""

    def __init__(self, label: Label, slug: str) -> None:
        super().__init__(label)
        self.slug = slug


# ── Screen ─────────────────────────────────────────────────────────────────────


class PracticeMode(Screen):
    """Practice hub — Exercises (scrollable drills) and Licks Library (looper-ready phrases)."""

    BINDINGS = [
        ("escape", "app.goto_welcome", "Back"),
        ("t", "next_tab", "Switch Tab"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent():
            with TabPane("Exercises", id="tab-exercises"):
                with ScrollableContainer(id="exercises-scroll"):
                    pass  # populated in on_mount
            with TabPane("Licks", id="tab-licks"):
                with Horizontal(id="licks-layout"):
                    with ScrollableContainer(id="licks-list-pane"):
                        yield ListView(id="licks-list")
                    with ScrollableContainer(id="lick-detail-pane"):
                        yield Static("", id="lick-detail-header")
                        yield Static("", id="lick-detail-body")
        yield Footer()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_mount(self) -> None:
        self._build_exercises()
        self._build_licks_list()

    # ------------------------------------------------------------------
    # Tab switching
    # ------------------------------------------------------------------

    def action_next_tab(self) -> None:
        tc = self.query_one(TabbedContent)
        tc.active = "tab-licks" if tc.active == "tab-exercises" else "tab-exercises"

    # ------------------------------------------------------------------
    # Exercises tab
    # ------------------------------------------------------------------

    def _build_exercises(self) -> None:
        loader = self.app.exercise_loader
        pane = self.query_one("#exercises-scroll", ScrollableContainer)

        # Group by module (technique / scale / chord), ordered deliberately
        module_order = ["technique", "scale", "chord"]
        module_labels = {
            "technique": "Technique",
            "scale":     "Scale",
            "chord":     "Chord",
        }

        grouped: dict[str, list] = {}
        for lesson in loader.lessons.values():
            key = lesson.meta.module or "other"
            grouped.setdefault(key, []).append(lesson)

        ordered = [m for m in module_order if m in grouped]
        extras  = sorted(m for m in grouped if m not in module_order)

        widgets = []
        for module in ordered + extras:
            label = module_labels.get(module, module.replace("-", " ").title())
            exercises = sorted(
                grouped[module],
                key=lambda l: (l.meta.position or 9999, l.meta.title),
            )
            widgets.append(Static(f"── {label} Exercises ──", classes="exercise-category"))
            for ex in exercises:
                if ex.meta.summary:
                    widgets.append(Static(ex.meta.summary, classes="exercise-summary"))
                for block in ex.body:
                    if isinstance(block, TextBlock):
                        widgets.append(Markdown(block.content, classes="exercise-text"))
                    elif isinstance(block, DiagramBlock):
                        widgets.append(Static(block.rendered, classes="exercise-diagram"))
                widgets.append(Static("", classes="exercise-spacer"))

        pane.mount(*widgets)

    # ------------------------------------------------------------------
    # Licks tab — list
    # ------------------------------------------------------------------

    def _build_licks_list(self) -> None:
        lv = self.query_one("#licks-list", ListView)
        lv_items: list[ListItem] = []

        for category_label, licks in self.app.lick_loader.by_category():
            lv_items.append(
                ListItem(Label(f"[bold]{category_label}[/bold]"), disabled=True)
            )
            for lick in licks:
                tags = "  " + "  ".join(f"[{t}]" for t in lick.meta.tags[:2])
                item = _LickItem(
                    Label(f"  {lick.meta.title}{tags}"),
                    slug=lick.meta.slug,
                )
                lv_items.append(item)

        for item in lv_items:
            lv.append(item)

        # Show first lick automatically if any exist
        first = next(
            (l for ls in (licks for _, licks in self.app.lick_loader.by_category()) for l in ls),
            None,
        )
        if first:
            self._show_lick(first)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, _LickItem):
            lick = self.app.lick_loader.licks.get(event.item.slug)
            if lick:
                self._show_lick(lick)

    # ------------------------------------------------------------------
    # Licks tab — detail
    # ------------------------------------------------------------------

    def _show_lick(self, lick: ParsedLick) -> None:
        # Build header block
        diff_badge = {"beginner": "●", "intermediate": "◉", "advanced": "◎"}.get(
            lick.meta.difficulty, "○"
        )
        backing = "  ·  ".join(lick.meta.backing_chords)
        prog    = f"  ({lick.meta.backing_progression})" if lick.meta.backing_progression else ""
        style_tags = "  ".join(f"[{t}]" for t in lick.meta.tags)

        header_lines = [
            f"{diff_badge}  {lick.meta.title}",
            f"Key: {lick.meta.key}   Scale: {lick.meta.scale.replace('_', ' ')}",
            f"Looper: {backing}{prog}",
            f"Style: {style_tags}",
            "",
        ]
        self.query_one("#lick-detail-header", Static).update("\n".join(header_lines))

        # Rebuild body widgets — remove old, mount new
        detail_pane = self.query_one("#lick-detail-pane", ScrollableContainer)
        # Clear everything except the header and body statics
        for w in detail_pane.query(".lick-body-block"):
            w.remove()

        widgets = []
        if lick.meta.summary:
            widgets.append(Static(lick.meta.summary, classes="lick-body-block lick-summary"))
        for block in lick.body:
            if isinstance(block, TextBlock):
                widgets.append(Markdown(block.content, classes="lick-body-block lick-text"))
            elif isinstance(block, DiagramBlock):
                widgets.append(Static(block.rendered, classes="lick-body-block lick-diagram"))

        detail_pane.mount(*widgets)
        detail_pane.scroll_home(animate=False)
