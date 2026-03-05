"""ToolsMode — chord finder, scale finder, tuning reference."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, Select, Static, TabbedContent, TabPane

from guitar_tui.engine.dispatcher import dispatch
from guitar_tui.loaders.models import ChordEntry, ChordVoicing, ScalePattern, ScalePosition


def _chord_spec(entry: ChordEntry, voicing: ChordVoicing) -> dict:
    title = (
        f"{entry.full_name} — {voicing.label}"
        if len(entry.voicings) > 1
        else entry.full_name
    )
    spec: dict = {"type": "chord", "title": title, "frets": voicing.frets}
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


class ToolsMode(Screen):
    """Tools screen: chord finder, scale finder, tuning reference."""

    BINDINGS = [
        ("escape", "app.goto_welcome", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(id="tools-tabs"):
            with TabPane("Chord Finder", id="tab-chord-finder"):
                yield Label("Chord Finder", classes="tool-title")
                yield Select(options=[], prompt="Select a chord…", id="chord-select")
                yield Select(
                    options=[],
                    prompt="Select a voicing…",
                    id="voicing-select",
                    disabled=True,
                )
                yield Static("", id="chord-diagram")
            with TabPane("Scale Finder", id="tab-scale-finder"):
                yield Label("Scale Finder", classes="tool-title")
                yield Select(options=[], prompt="Select a scale…", id="scale-select")
                yield Static("", id="scale-diagram")
            with TabPane("Tuning", id="tab-tuning"):
                yield Label("Tuning reference coming soon.", classes="placeholder")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#chord-select", Select).set_options([
            (f"{e.name} — {e.full_name}", e.name)
            for e in sorted(self.app.data_loader.chords.values(), key=lambda c: c.name)
        ])
        self.query_one("#scale-select", Select).set_options([
            (s.full_name, s.name)
            for s in sorted(self.app.data_loader.scales.values(), key=lambda s: s.full_name)
        ])

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.value is Select.NULL:
            return

        if event.select.id == "chord-select":
            entry = self.app.data_loader.chords[event.value]
            voicing_select = self.query_one("#voicing-select", Select)
            voicing_select.set_options([(v.label, v.id) for v in entry.voicings])
            voicing_select.disabled = len(entry.voicings) <= 1
            self.query_one("#chord-diagram", Static).update(
                dispatch(_chord_spec(entry, entry.voicings[0]))
            )

        elif event.select.id == "voicing-select":
            chord_select = self.query_one("#chord-select", Select)
            if chord_select.value is Select.NULL:
                return
            entry = self.app.data_loader.chords[chord_select.value]
            voicing = next(v for v in entry.voicings if v.id == event.value)
            self.query_one("#chord-diagram", Static).update(
                dispatch(_chord_spec(entry, voicing))
            )

        elif event.select.id == "scale-select":
            scale = self.app.data_loader.scales[event.value]
            self.query_one("#scale-diagram", Static).update(
                dispatch(_scale_spec(scale, scale.positions[0]))
            )
