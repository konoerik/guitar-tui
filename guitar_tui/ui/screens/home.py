"""HomeScreen — lessons list and chord/scale reference viewer."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Select,
    Static,
    TabbedContent,
    TabPane,
)

from guitar_tui.engine.dispatcher import dispatch
from guitar_tui.loaders.models import ChordVoicing, ScalePattern, ScalePosition


def _chord_spec(voicing: ChordVoicing) -> dict:
    spec: dict = {"type": "chord", "title": voicing.full_name, "frets": voicing.frets}
    if voicing.fingers:
        spec["fingers"] = voicing.fingers
    if voicing.base_fret > 1:
        spec["base_fret"] = voicing.base_fret
    if voicing.barre:
        spec["barre"] = {
            "fret": voicing.barre.fret,
            "from": voicing.barre.from_string,
            "to": voicing.barre.to_string,
        }
    return spec


def _scale_spec(scale: ScalePattern, pos: ScalePosition) -> dict:
    return {
        "type": "scale",
        "title": f"{scale.full_name} — {pos.name}",
        "root": scale.key,
        "fret_range": list(pos.fret_range),
        "positions": [
            {"string": n.string, "fret": n.fret, "degree": n.degree, "root": n.root}
            for n in pos.notes
        ],
    }


class HomeScreen(Screen):
    """Main screen with Lessons and Reference tabs."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("l", "focus_lessons", "Lessons"),
        ("r", "focus_reference", "Reference"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(id="tabs"):
            with TabPane("Lessons", id="tab-lessons"):
                yield ListView(id="lesson-list")
            with TabPane("Reference", id="tab-reference"):
                yield Label("Chord", classes="ref-label")
                yield Select(options=[], prompt="Select a chord…", id="chord-select")
                yield Label("Scale", classes="ref-label")
                yield Select(options=[], prompt="Select a scale…", id="scale-select")
                yield Static("", id="ref-diagram")
        yield Footer()

    def on_mount(self) -> None:
        lessons = sorted(
            self.app.lesson_loader.lessons.values(),
            key=lambda l: (l.meta.module or "zzz", l.meta.position or 9999, l.meta.title),
        )
        lv = self.query_one("#lesson-list", ListView)
        badges = {"beginner": "●", "intermediate": "◉", "advanced": "◎"}
        for lesson in lessons:
            badge = badges.get(lesson.meta.difficulty, "○")
            label = f"{badge} {lesson.meta.title}"
            lv.append(ListItem(Label(label), id=f"lesson-{lesson.meta.slug}"))

        chord_select = self.query_one("#chord-select", Select)
        chord_select.set_options([
            (f"{v.name} — {v.full_name}", v.name)
            for v in sorted(self.app.data_loader.chords.values(), key=lambda c: c.name)
        ])

        scale_select = self.query_one("#scale-select", Select)
        scale_select.set_options([
            (s.full_name, s.name)
            for s in sorted(self.app.data_loader.scales.values(), key=lambda s: s.full_name)
        ])

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        from guitar_tui.ui.screens.lesson import LessonScreen
        slug = event.item.id.removeprefix("lesson-")
        lesson = self.app.lesson_loader.lessons[slug]
        self.app.push_screen(LessonScreen(lesson))

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.value is Select.BLANK:
            return
        diagram = self.query_one("#ref-diagram", Static)
        if event.select.id == "chord-select":
            voicing = self.app.data_loader.chords[event.value]
            diagram.update(dispatch(_chord_spec(voicing)))
        elif event.select.id == "scale-select":
            scale = self.app.data_loader.scales[event.value]
            pos = scale.positions[0]
            diagram.update(dispatch(_scale_spec(scale, pos)))

    def action_focus_lessons(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-lessons"
        self.query_one("#lesson-list", ListView).focus()

    def action_focus_reference(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-reference"
        self.query_one("#chord-select", Select).focus()
