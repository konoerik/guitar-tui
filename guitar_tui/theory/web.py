"""Theory Web relationships — chord↔key membership, progression realization,
and scale transposition helpers.

Like keys.py, this module contains music knowledge. It backs the M8 Theory
Web views (scale view, chord view, song analysis); the engine layer stays
music-agnostic and never imports it.
"""

from __future__ import annotations

from dataclasses import dataclass

from guitar_tui.theory.keys import (
    KEY_NAMES,
    diatonic_chords,
    enharmonic_name,
    note_to_semitone,
)

# ── Chord → key membership ─────────────────────────────────────────────────────

# Modes are omitted by default: every mode shares its pitch collection with a
# major key, so listing D Dorian, E Phrygian, … alongside C major would repeat
# the same information seven times. Major/Minor answer the practical question.
_MEMBERSHIP_QUALITIES: tuple[str, ...] = ("Major", "Minor")


@dataclass(frozen=True)
class ChordMembership:
    """One key in which a chord is diatonic, and its function there."""

    key_root: str    # e.g. "C"
    quality: str     # "Major" | "Minor"
    roman: str       # e.g. "vi"


def chord_memberships(
    chord_name: str,
    qualities: tuple[str, ...] = _MEMBERSHIP_QUALITIES,
) -> list[ChordMembership]:
    """Every (key, function) slot where *chord_name* is a diatonic chord.

    Matching is enharmonic-aware (Db == C#, Abm == G#m). Chords whose quality
    has no diatonic slot (maj7, sus, …) return an empty list.
    """
    names = {chord_name}
    alt = enharmonic_name(chord_name)
    if alt is not None:
        names.add(alt)
    memberships: list[ChordMembership] = []
    for quality in qualities:
        for root in KEY_NAMES:
            for roman, name in diatonic_chords(root, quality):
                if name in names:
                    memberships.append(ChordMembership(root, quality, roman))
    return memberships


# ── Progression realization ────────────────────────────────────────────────────


def realize_progression(
    root: str, quality: str, numerals: list[str]
) -> list[tuple[str, str]]:
    """Map roman numerals to concrete chords in a key.

    realize_progression("C", "Major", ["I", "V", "vi", "IV"])
        -> [("I", "C"), ("V", "G"), ("vi", "Am"), ("IV", "F")]

    Raises ValueError for a numeral outside the quality's degree table.
    """
    table = dict(diatonic_chords(root, quality))
    realized: list[tuple[str, str]] = []
    for numeral in numerals:
        chord = table.get(numeral)
        if chord is None:
            raise ValueError(
                f"numeral {numeral!r} is not diatonic in {root} {quality}"
            )
        realized.append((numeral, chord))
    return realized


# ── Scale transposition ────────────────────────────────────────────────────────


def transposition_offset(target_root: str, reference_key: str) -> int:
    """Semitones to add to a pattern stored in *reference_key* to sound in
    *target_root* (always 0–11; callers shift down by octaves to fit)."""
    return (note_to_semitone(target_root) - note_to_semitone(reference_key)) % 12


def fit_position_shift(lo: int, hi: int, max_fret: int) -> int:
    """Octave shift (multiple of ±12) that places the fret span [lo, hi]
    within [0, max_fret], preferring the lowest playable placement."""
    shift = 0
    while hi + shift > max_fret:
        shift -= 12
    while lo + shift < 0:
        shift += 12
    # Prefer the lowest valid placement on the neck.
    while lo + shift - 12 >= 0:
        shift -= 12
    return shift
