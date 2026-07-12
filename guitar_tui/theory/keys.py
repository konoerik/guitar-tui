"""Note names, semitone values, and diatonic chord construction.

This module contains music knowledge (note relationships, key/chord theory).
It is intentionally separate from the engine layer, which is music-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass

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


# Enharmonic root spellings. Chord data uses conventional per-chord names
# (Db major but G#m minor); generated names use one fixed chromatic spelling —
# lookups must try both.
_ENHARMONIC_ROOTS: dict[str, str] = {
    "C#": "Db", "Db": "C#",
    "D#": "Eb", "Eb": "D#",
    "F#": "Gb", "Gb": "F#",
    "G#": "Ab", "Ab": "G#",
    "A#": "Bb", "Bb": "A#",
}


def enharmonic_name(chord_name: str) -> str | None:
    """Return *chord_name* with its root respelled enharmonically, or None.

    "C#" -> "Db", "Abm" -> "G#m", "Eb7" -> "D#7"; natural roots return None.
    """
    if len(chord_name) >= 2 and chord_name[:2] in _ENHARMONIC_ROOTS:
        return _ENHARMONIC_ROOTS[chord_name[:2]] + chord_name[2:]
    return None


# Chord spelling — the qualities diatonic_chords() can generate.
_CHORD_TONE_INTERVALS: dict[str, tuple[int, ...]] = {
    "":  (0, 4, 7),
    "m": (0, 3, 7),
    "°": (0, 3, 6),
    "+": (0, 4, 8),
    "7": (0, 4, 7, 10),
}


def chord_tones(chord_name: str) -> list[str] | None:
    """Spell out a chord's notes, e.g. "C#°" -> ["C#", "E", "G"].

    Returns None when the name's quality is not recognized.
    """
    if not chord_name or chord_name[0] not in _NOTE_TO_ST:
        return None
    root_len = 2 if len(chord_name) >= 2 and chord_name[1] in "#b" else 1
    root, suffix = chord_name[:root_len], chord_name[root_len:]
    intervals = _CHORD_TONE_INTERVALS.get(suffix)
    if intervals is None or root not in _NOTE_TO_ST:
        return None
    root_st = _NOTE_TO_ST[root]
    return [semitone_to_note(root_st + i) for i in intervals]


# ---------------------------------------------------------------------------
# Quality → DataLoader scale name
# ---------------------------------------------------------------------------

QUALITY_TO_SCALE: dict[str, str] = {
    "Major":             "major",
    "Major Pentatonic":  "major_pentatonic",
    "Minor":             "natural_minor",
    "Minor Pentatonic":  "minor_pentatonic",
    "Blues":             "blues_scale",
    "Dorian":            "dorian",
    "Phrygian":          "phrygian",
    "Lydian":            "lydian",
    "Mixolydian":        "mixolydian",
    "Harmonic Minor":    "harmonic_minor",
    "Phrygian Dominant": "phrygian_dominant",
    "Hungarian Minor":   "hungarian_minor",
    "Whole Tone":        "whole_tone",
    "Diminished (W–H)":  "diminished",
    "Hirajoshi":         "hirajoshi",
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

# Harmonic minor and its 5th mode have standard tertian harmony.
_HARMONIC_MINOR_DEGREES: list[tuple[int, str, str]] = [
    (0,  "i",     "min"),
    (2,  "ii°",   "dim"),
    (3,  "bIII+", "aug"),
    (5,  "iv",    "min"),
    (7,  "V",     "maj"),
    (8,  "bVI",   "maj"),
    (11, "vii°",  "dim"),
]

_PHRYGIAN_DOMINANT_DEGREES: list[tuple[int, str, str]] = [
    (0,  "I",    "maj"),
    (1,  "bII",  "maj"),
    (4,  "iii°", "dim"),
    (5,  "iv",   "min"),
    (7,  "v°",   "dim"),
    (8,  "bVI+", "aug"),
    (10, "bvii", "min"),
]

# Symmetric and gapped scales don't stack into a usable triad-per-degree set;
# the Key View shows no chord strip for these.
_NO_DEGREE_QUALITIES: frozenset[str] = frozenset(
    {"Hungarian Minor", "Whole Tone", "Diminished (W–H)", "Hirajoshi"}
)

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
    suffix = {"maj": "", "min": "m", "dim": "°", "aug": "+", "dom7": "7"}.get(quality, "")
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
# Key context — parent major key, relative naming, accidentals
# ---------------------------------------------------------------------------

# Semitones from the selected root UP to the parent major key's root.
# E.g. D Dorian is the 2nd mode of C major: C is 10 semitones above D (mod 12).
_PARENT_MAJOR_OFFSET: dict[str, int] = {
    "Major":            0,
    "Major Pentatonic": 0,
    "Minor":            3,
    "Minor Pentatonic": 3,
    "Blues":            3,
    "Dorian":           10,
    "Phrygian":         8,
    "Lydian":           7,
    "Mixolydian":       5,
}

# Major key spelling by semitone, per circle-of-fifths convention (_KEY_SIGS).
_MAJOR_KEY_BY_ST: dict[int, tuple[str, str, int]] = {
    note_to_semitone(major): (major, minor, count)
    for major, minor, count, _ in _KEY_SIGS
}


@dataclass(frozen=True)
class KeyContext:
    """Context for a root + quality: parent major key and how to name it."""

    parent_major: str        # e.g. "C" for A Minor or D Dorian
    relative_label: str      # "relative minor" | "relative major" | "parent major"
    relative_name: str       # e.g. "Am", "C"
    accidental_count: int    # >0 sharps, <0 flats, 0 none


def key_context(root: str, quality_name: str) -> KeyContext | None:
    """Return the KeyContext for a root and quality, or None if unknown."""
    offset = _PARENT_MAJOR_OFFSET.get(quality_name)
    if offset is None:
        return None
    parent_st = (note_to_semitone(root) + offset) % 12
    parent_major, relative_minor, count = _MAJOR_KEY_BY_ST[parent_st]
    if quality_name in ("Major", "Major Pentatonic"):
        return KeyContext(parent_major, "relative minor", relative_minor, count)
    if quality_name in ("Minor", "Minor Pentatonic", "Blues"):
        return KeyContext(parent_major, "relative major", parent_major, count)
    return KeyContext(parent_major, "parent major", parent_major, count)


# Characteristic note per quality: (semitones above root, interval symbol).
# The note that distinguishes each mode from plain major/minor; for blues,
# the b5 "blue note". Symbols match the Intervals reference table.
CHARACTERISTIC_NOTE: dict[str, tuple[int, str]] = {
    "Dorian":            (9,  "6"),
    "Phrygian":          (1,  "b2"),
    "Lydian":            (6,  "#4"),
    "Mixolydian":        (10, "b7"),
    "Blues":             (6,  "b5"),
    "Harmonic Minor":    (11, "7"),
    "Phrygian Dominant": (4,  "3"),
    "Hungarian Minor":   (6,  "#4"),
}


# ---------------------------------------------------------------------------
# Diatonic chord construction
# ---------------------------------------------------------------------------

# Qualities that have a degree table (usable in progressions data).
DEGREE_QUALITIES: tuple[str, ...] = (
    "Major", "Minor", "Blues", "Dorian", "Phrygian", "Lydian", "Mixolydian",
    "Harmonic Minor", "Phrygian Dominant",
)


def _degrees_for(quality_name: str) -> list[tuple[int, str, str]]:
    if quality_name == "Major":
        return _MAJOR_DEGREES
    if quality_name == "Minor":
        return _MINOR_DEGREES
    if quality_name == "Blues":
        return _BLUES_DEGREES
    if quality_name == "Harmonic Minor":
        return _HARMONIC_MINOR_DEGREES
    if quality_name == "Phrygian Dominant":
        return _PHRYGIAN_DOMINANT_DEGREES
    if quality_name in _NO_DEGREE_QUALITIES:
        return []
    return _MODAL_DEGREES.get(quality_name, _MAJOR_DEGREES)


def valid_numerals(quality_name: str) -> list[str]:
    """The roman numerals available in a quality's degree table."""
    return [roman for _, roman, _ in _degrees_for(quality_name)]


def diatonic_chords(root: str, quality_name: str) -> list[tuple[str, str]]:
    """Return [(roman_numeral, chord_name), ...] for a given root and quality."""
    root_st = note_to_semitone(root)
    return [
        (roman, _chord_name(root_st + offset, q))
        for offset, roman, q in _degrees_for(quality_name)
    ]
