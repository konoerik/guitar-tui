"""WelcomeScreen — three-card layout with a rotating daily hint."""

import datetime

from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Static

_HINTS: list[str] = [
    "The minor pentatonic and natural minor share the same notes — pentatonic just "
    "leaves out the 2nd and 6th. Those two notes are what give natural minor its "
    "fuller, more melodic sound.",

    "Every major key has a relative minor that shares all the same notes and chords. "
    "C major and A minor are the same key, just with a different home base.",

    "The I–IV–V progression works in every key because the 4th and 5th are the two "
    "strongest harmonic relationships to the root. That's why it always sounds resolved.",

    "Barre chords are open chord shapes moved up the neck — the index finger replaces "
    "the nut. One E shape and one A shape give you every major chord in every key.",

    "The circle of fifths is a map, not a formula. Moving clockwise adds a sharp; "
    "counter-clockwise adds a flat. Keys next to each other share almost all their notes.",

    "Dorian is natural minor with a raised 6th. That one note — the major 6th — is "
    "what makes it sound less dark, more groovy. It's the scale behind countless "
    "rock and jazz standards.",

    "A dominant 7th chord wants to resolve to the chord a fifth below. G7 pulls toward C. "
    "That tension-and-release is the engine of blues and jazz harmony.",

    "The pentatonic scale works over almost any chord in its key because it avoids the "
    "notes most likely to clash — the 2nd, 4th, 6th, and 7th. Sometimes less is more.",

    "String bending is easier with support. Place fingers 1, 2, and 3 on the string "
    "and bend with finger 3 while the others add leverage. Your intonation will improve immediately.",

    "Vibrato is the most personal technique on guitar. Width and speed define your sound "
    "more than any scale. Slow and wide is expressive; fast and narrow is tense. "
    "Listen to your favorite players and notice the difference.",

    "Roman numerals in chord analysis tell you the function of a chord, not its name. "
    "I, IV, V works in any key — that's the whole point.",

    "Mixolydian is just a major scale with a flat 7th. It's the scale of classic rock "
    "riffs — Sweet Home Alabama, La Grange, and most 12-bar blues played in a major context.",

    "Position playing means keeping your hand in a four-fret window. It's not a rule — "
    "it's efficiency. You only shift when you need to.",

    "Modes are not exotic scales. They are the major scale with a different note treated "
    "as home. Play C major starting on D and anchoring to D — that's D Dorian.",

    "The tritone is the most unstable interval in Western music — exactly halfway between "
    "the root and the octave. Dominant 7th chords contain one, which is why they demand resolution.",

    "A capo doesn't change how you play — it changes what the audience hears. Capo on 2, "
    "play a G shape: you're playing in A. All your open chord muscle memory still works.",

    "Sus chords have no 3rd, so they're neither major nor minor. They create ambiguity "
    "that can resolve — or float freely in the right context.",

    "Ear training is pattern recognition. The more you associate an interval with a song "
    "you know, the faster your ear learns. A minor 3rd opens Smoke on the Water. "
    "A perfect 5th opens Star Wars.",

    "The blues scale adds one note to the minor pentatonic: the flat 5th. That note, "
    "bent up toward the 5th, is the core gesture of blues guitar.",

    "In the [3] Tools screen, the Key View shows you the diatonic chords for any key "
    "and scale. If you're noodling and want to know what chords fit, start there.",

    "Lessons list their prerequisites. If something isn't clicking, check the "
    "prerequisite lesson — the gap is usually there.",

    "Learning Position 2 of the minor pentatonic immediately above Position 1 and "
    "connecting the two is the single biggest step toward playing the whole neck.",

    "Every chord in a key has a Roman numeral function. In C major: C is I, Dm is ii, "
    "Em is iii, F is IV, G is V, Am is vi, Bdim is vii°. Learn the functions, "
    "not just the names.",

    "Phrygian's defining sound is the half-step above the root. Root to b2 and back — "
    "one fret up and down from your tonic — immediately signals Phrygian to any listener.",

    "Lydian is the major scale with a raised 4th. It sounds elevated, floating, "
    "slightly unreal. It's the scale of Superman, E.T., and the Simpsons theme.",

    "The I–V–vi–IV progression underlies thousands of pop songs. In C: C–G–Am–F. "
    "In G: G–D–Em–C. Learn it in three keys and you can play along with a huge "
    "amount of recorded music.",

    "Natural harmonics ring clearly at frets 12, 7, and 5. Fret 12 is the octave. "
    "Touch the string lightly above the fret — don't press — and release as you pick.",

    "Chord inversions change the bass note but not the chord's function. C major with "
    "E in the bass is still C major — it just sits differently in the mix.",

    "The CAGED system describes five ways to play the same chord up the neck. "
    "Every open chord shape you know is one of them.",

    "Hammer-ons and pull-offs let you play two notes with one pick stroke. The key is "
    "finger strength on the fret hand — the picked note needs to be loud enough "
    "that the hammered note matches it in volume.",

    "The major scale generates all diatonic chords. Once you know which degree is "
    "major, minor, or diminished, you know the harmony for any key — "
    "without memorizing chord names separately.",

    "Slides connect two notes with a single continuous motion. They work best when "
    "the destination note lands on the beat, with the slide arriving just before it.",
]


def _hint_of_the_day() -> str:
    day = datetime.date.today().timetuple().tm_yday
    return _HINTS[day % len(_HINTS)]


_WELCOME_TEXT = """\
Guitar theory for guitarists who got busy with life
but never lost interest in the instrument.

[dim]Assumes you can already hold a guitar, fret a note, and strum a chord.[/dim]

[bold][2] Lessons[/bold]    Curriculum — 11 tracks, 78 lessons, open chords through song analysis.
[bold][3] Tools[/bold]      Key and scale explorer, chord strip, reference tables.
[bold][4] Practice[/bold]   Technique exercises and a lick library for looper use.
[bold][q] Quit[/bold]       [dim]Number keys switch screens at any time.[/dim]\
"""

_INFO_TEXT = """\
[bold]Guitar TUI[/bold]  v0.1.0  ·  MIT License  ·  © 2026 Erikton Konomi

github.com/konoerik/guitar-tui

[dim]Recommended terminal size: 110 × 36 or larger.[/dim]\
"""


class WelcomeScreen(Screen):
    """Home screen: three-card layout with a rotating daily hint."""

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="welcome-scroll"):
            with Vertical(id="welcome-card"):
                yield Static(_WELCOME_TEXT, id="welcome-text")
            with Vertical(id="hint-card"):
                yield Static(id="hint-text")
            with Vertical(id="info-card"):
                yield Static(_INFO_TEXT, id="info-text")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#welcome-card").border_title = "Guitar TUI"
        self.query_one("#hint-card").border_title = "Hint of the day"
        self.query_one("#info-card").border_title = "About"
        self.query_one("#hint-text", Static).update(_hint_of_the_day())
