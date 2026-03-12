"""Note names, semitone values, and diatonic chord construction.

This module contains music knowledge (note relationships, key/chord theory).
It is intentionally separate from the engine layer, which is music-agnostic.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Chromatic scale — guitar-friendly enharmonic spellings
# ---------------------------------------------------------------------------

# Display names for each semitone (0 = C).  Mixed sharps/flats follow
# conventional guitar usage (e.g. Bb rather than A#, Eb rather than D#).
_CHROMATIC: list[str] = [
    "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B",
]

_NOTE_TO_ST: dict[str, int] = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4,
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11,
}

# Keys shown in the selector, in guitar-friendly order starting from A.
KEY_NAMES: list[str] = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab"]


def note_to_semitone(note: str) -> int:
    """Return the semitone value (0–11, C=0) for a note name."""
    return _NOTE_TO_ST[note]


def semitone_to_note(st: int) -> str:
    """Return the display note name for a semitone value."""
    return _CHROMATIC[st % 12]


# ---------------------------------------------------------------------------
# Quality → DataLoader scale name
# ---------------------------------------------------------------------------

QUALITY_TO_SCALE: dict[str, str] = {
    "Major":            "major",
    "Major Pentatonic": "major_pentatonic",
    "Minor":            "natural_minor",
    "Minor Pentatonic": "minor_pentatonic",
    "Blues":            "blues_scale",
    "Dorian":           "dorian",
    "Phrygian":         "phrygian",
    "Lydian":           "lydian",
    "Mixolydian":       "mixolydian",
}

# Pentatonic/blues scales share chord harmony with their parent scale.
# Maps quality name → parent quality used for the diatonic chord strip.
QUALITY_CHORD_PARENT: dict[str, str] = {
    "Major Pentatonic": "Major",
    "Minor Pentatonic": "Minor",
}

QUALITY_NAMES: list[str] = list(QUALITY_TO_SCALE.keys())

# ---------------------------------------------------------------------------
# Diatonic chord construction
# ---------------------------------------------------------------------------

# Each entry: (semitone_offset_from_root, roman_numeral, chord_quality)
# chord_quality: "maj" | "min" | "dim"

_MAJOR_DEGREES: list[tuple[int, str, str]] = [
    (0,  "I",    "maj"),
    (2,  "ii",   "min"),
    (4,  "iii",  "min"),
    (5,  "IV",   "maj"),
    (7,  "V",    "maj"),
    (9,  "vi",   "min"),
    (11, "vii°", "dim"),
]

_MINOR_DEGREES: list[tuple[int, str, str]] = [
    (0,  "i",    "min"),
    (2,  "ii°",  "dim"),
    (3,  "bIII", "maj"),
    (5,  "iv",   "min"),
    (7,  "v",    "min"),
    (8,  "bVI",  "maj"),
    (10, "bVII", "maj"),
]

# Blues uses three dominant 7th chords — not a diatonic scale family.
_BLUES_DEGREES: list[tuple[int, str, str]] = [
    (0, "I7",  "dom7"),
    (5, "IV7", "dom7"),
    (7, "V7",  "dom7"),
]

_MODAL_DEGREES: dict[str, list[tuple[int, str, str]]] = {
    "Dorian": [
        (0,  "i",    "min"),
        (2,  "ii",   "min"),
        (3,  "bIII", "maj"),
        (5,  "IV",   "maj"),
        (7,  "v",    "min"),
        (9,  "vi°",  "dim"),
        (10, "bVII", "maj"),
    ],
    "Mixolydian": [
        (0,  "I",    "maj"),
        (2,  "ii",   "min"),
        (4,  "iii°", "dim"),
        (5,  "IV",   "maj"),
        (7,  "v",    "min"),
        (9,  "vi",   "min"),
        (10, "bVII", "maj"),
    ],
    "Phrygian": [
        (0,  "i",    "min"),
        (1,  "bII",  "maj"),
        (3,  "bIII", "maj"),
        (5,  "iv",   "min"),
        (7,  "v°",   "dim"),
        (8,  "bVI",  "maj"),
        (10, "bvii", "min"),
    ],
    "Lydian": [
        (0,  "I",    "maj"),
        (2,  "II",   "maj"),
        (4,  "iii",  "min"),
        (6,  "#iv°", "dim"),
        (7,  "V",    "maj"),
        (9,  "vi",   "min"),
        (11, "vii",  "min"),
    ],
}


def _chord_name(root_st: int, quality: str) -> str:
    note = semitone_to_note(root_st % 12)
    suffix = {"maj": "", "min": "m", "dim": "°", "dom7": "7"}.get(quality, "")
    return f"{note}{suffix}"


# ---------------------------------------------------------------------------
# Key signatures — circle of fifths order
# ---------------------------------------------------------------------------

# (major_key, relative_minor, accidental_count, [accidental_notes])
# Positive count = sharps (♯), negative = flats (♭), zero = no accidentals.
_KEY_SIGS: list[tuple[str, str, int, list[str]]] = [
    ("C",  "Am",   0, []),
    ("G",  "Em",   1, ["F#"]),
    ("D",  "Bm",   2, ["F#", "C#"]),
    ("A",  "F#m",  3, ["F#", "C#", "G#"]),
    ("E",  "C#m",  4, ["F#", "C#", "G#", "D#"]),
    ("B",  "G#m",  5, ["F#", "C#", "G#", "D#", "A#"]),
    ("F#", "D#m",  6, ["F#", "C#", "G#", "D#", "A#", "E#"]),
    ("Db", "Bbm", -5, ["Bb", "Eb", "Ab", "Db", "Gb"]),
    ("Ab", "Fm",  -4, ["Bb", "Eb", "Ab", "Db"]),
    ("Eb", "Cm",  -3, ["Bb", "Eb", "Ab"]),
    ("Bb", "Gm",  -2, ["Bb", "Eb"]),
    ("F",  "Dm",  -1, ["Bb"]),
]

# Open chord shapes used in the capo reference: (display, root_semitone, quality_suffix)
_CAPO_SHAPES: list[tuple[str, int, str]] = [
    ("E",  4, ""),
    ("Em", 4, "m"),
    ("A",  9, ""),
    ("Am", 9, "m"),
    ("D",  2, ""),
    ("G",  7, ""),
    ("C",  0, ""),
]

_MAX_CAPO = 7


def key_signatures() -> list[tuple[str, str, int, list[str]]]:
    """Key signature data in circle-of-fifths order.

    Returns a list of (major_key, relative_minor, accidental_count, accidental_notes).
    Positive count = sharps, negative = flats, zero = no accidentals.
    """
    return _KEY_SIGS


def capo_chart() -> tuple[list[str], list[list[str]]]:
    """Capo reference table.

    Returns (shape_names, rows) where rows[i] contains the sounding chord
    name for capo fret i+1 across each shape in shape_names.
    """
    shape_names = [s[0] for s in _CAPO_SHAPES]
    rows: list[list[str]] = []
    for fret in range(1, _MAX_CAPO + 1):
        row = [
            f"{semitone_to_note((root_st + fret) % 12)}{suffix}"
            for _, root_st, suffix in _CAPO_SHAPES
        ]
        rows.append(row)
    return shape_names, rows


# ---------------------------------------------------------------------------
# Diatonic chord construction
# ---------------------------------------------------------------------------

def diatonic_chords(root: str, quality_name: str) -> list[tuple[str, str]]:
    """Return [(roman_numeral, chord_name), ...] for a given root and quality."""
    root_st = note_to_semitone(root)
    if quality_name == "Major":
        degrees = _MAJOR_DEGREES
    elif quality_name == "Minor":
        degrees = _MINOR_DEGREES
    elif quality_name == "Blues":
        degrees = _BLUES_DEGREES
    else:
        degrees = _MODAL_DEGREES.get(quality_name, _MAJOR_DEGREES)
    return [
        (roman, _chord_name(root_st + offset, q))
        for offset, roman, q in degrees
    ]
