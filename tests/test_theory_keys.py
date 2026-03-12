"""Tests for music theory: note conversion, diatonic chords, capo chart, key signatures."""

import pytest

from guitar_tui.theory.keys import (
    KEY_NAMES,
    QUALITY_NAMES,
    capo_chart,
    diatonic_chords,
    key_signatures,
    note_to_semitone,
    semitone_to_note,
)


# ── Note conversion ────────────────────────────────────────────────────────────


def test_note_to_semitone_natural_notes():
    assert note_to_semitone("C") == 0
    assert note_to_semitone("D") == 2
    assert note_to_semitone("E") == 4
    assert note_to_semitone("F") == 5
    assert note_to_semitone("G") == 7
    assert note_to_semitone("A") == 9
    assert note_to_semitone("B") == 11


def test_note_to_semitone_enharmonics():
    assert note_to_semitone("C#") == note_to_semitone("Db")
    assert note_to_semitone("D#") == note_to_semitone("Eb")
    assert note_to_semitone("F#") == note_to_semitone("Gb")
    assert note_to_semitone("G#") == note_to_semitone("Ab")
    assert note_to_semitone("A#") == note_to_semitone("Bb")


def test_semitone_to_note_round_trip():
    for note in KEY_NAMES:
        st = note_to_semitone(note)
        assert semitone_to_note(st) is not None


def test_semitone_to_note_wraps_octave():
    assert semitone_to_note(0) == semitone_to_note(12)
    assert semitone_to_note(1) == semitone_to_note(13)


def test_all_12_semitones_have_names():
    for i in range(12):
        name = semitone_to_note(i)
        assert isinstance(name, str)
        assert len(name) >= 1


# ── Diatonic chords ────────────────────────────────────────────────────────────


def test_major_chords_a():
    chords = diatonic_chords("A", "Major")
    assert len(chords) == 7
    romans = [r for r, _ in chords]
    names  = [n for _, n in chords]
    assert romans[0] == "I"   and names[0] == "A"
    assert romans[1] == "ii"  and names[1] == "Bm"
    assert romans[2] == "iii" and names[2] == "C#m"
    assert romans[3] == "IV"  and names[3] == "D"
    assert romans[4] == "V"   and names[4] == "E"
    assert romans[5] == "vi"  and names[5] == "F#m"
    assert romans[6] == "vii°" and names[6] == "Ab°"  # enharmonic: Ab = G#


def test_minor_chords_a():
    chords = diatonic_chords("A", "Minor")
    assert len(chords) == 7
    romans = [r for r, _ in chords]
    names  = [n for _, n in chords]
    assert romans[0] == "i"    and names[0] == "Am"
    assert romans[1] == "ii°"  and names[1] == "B°"
    assert romans[2] == "bIII" and names[2] == "C"
    assert romans[3] == "iv"   and names[3] == "Dm"
    assert romans[4] == "v"    and names[4] == "Em"
    assert romans[5] == "bVI"  and names[5] == "F"
    assert romans[6] == "bVII" and names[6] == "G"


def test_blues_chords_a():
    chords = diatonic_chords("A", "Blues")
    assert len(chords) == 3
    romans = [r for r, _ in chords]
    names  = [n for _, n in chords]
    assert romans[0] == "I7"  and names[0] == "A7"
    assert romans[1] == "IV7" and names[1] == "D7"
    assert romans[2] == "V7"  and names[2] == "E7"


def test_dorian_chords_d():
    chords = diatonic_chords("D", "Dorian")
    assert len(chords) == 7
    names = [n for _, n in chords]
    assert names[0] == "Dm"
    assert names[3] == "G"  # IV is major — the Dorian fingerprint


def test_phrygian_chords_e():
    chords = diatonic_chords("E", "Phrygian")
    assert len(chords) == 7
    names = [n for _, n in chords]
    assert names[0] == "Em"
    assert names[1] == "F"  # bII is major — the Phrygian fingerprint


def test_lydian_chords_f():
    chords = diatonic_chords("F", "Lydian")
    assert len(chords) == 7
    names = [n for _, n in chords]
    assert names[0] == "F"
    assert names[1] == "G"  # II is major — the Lydian fingerprint


def test_mixolydian_chords_g():
    chords = diatonic_chords("G", "Mixolydian")
    assert len(chords) == 7
    names = [n for _, n in chords]
    assert names[0] == "G"
    assert names[6] == "F"  # bVII is major — the Mixolydian fingerprint


def test_unknown_quality_falls_back_to_major():
    chords = diatonic_chords("C", "Unknown")
    major  = diatonic_chords("C", "Major")
    assert chords == major


def test_all_12_keys_major_return_7_chords():
    for key in KEY_NAMES:
        chords = diatonic_chords(key, "Major")
        assert len(chords) == 7, f"Expected 7 chords for {key} Major, got {len(chords)}"


# ── Key signatures ─────────────────────────────────────────────────────────────


def test_key_signatures_returns_12_keys():
    sigs = key_signatures()
    assert len(sigs) == 12


def test_key_signatures_structure():
    for major, relative_minor, count, notes in key_signatures():
        assert isinstance(major, str)
        assert isinstance(relative_minor, str)
        assert isinstance(count, int)
        assert isinstance(notes, list)
        # Accidental count matches the notes list length
        assert abs(count) == len(notes)


def test_c_major_has_no_accidentals():
    sigs = {major: (rel, count, notes) for major, rel, count, notes in key_signatures()}
    rel, count, notes = sigs["C"]
    assert rel == "Am"
    assert count == 0
    assert notes == []


def test_g_major_has_one_sharp():
    sigs = {major: (rel, count, notes) for major, rel, count, notes in key_signatures()}
    rel, count, notes = sigs["G"]
    assert count == 1
    assert "F#" in notes


# ── Capo chart ─────────────────────────────────────────────────────────────────


def test_capo_chart_shape_names():
    shape_names, _ = capo_chart()
    assert "E" in shape_names
    assert "A" in shape_names
    assert "G" in shape_names
    assert len(shape_names) == 7


def test_capo_chart_has_7_frets():
    _, rows = capo_chart()
    assert len(rows) == 7


def test_capo_chart_row_length_matches_shapes():
    shape_names, rows = capo_chart()
    for row in rows:
        assert len(row) == len(shape_names)


def test_capo_e_shape_transpositions():
    shape_names, rows = capo_chart()
    e_idx = shape_names.index("E")
    # E shape at capo 2 = F#, capo 3 = G, capo 5 = A
    assert rows[1][e_idx] == "F#"
    assert rows[2][e_idx] == "G"
    assert rows[4][e_idx] == "A"


# ── QUALITY_NAMES completeness ─────────────────────────────────────────────────


def test_quality_names_non_empty():
    assert len(QUALITY_NAMES) > 0


def test_all_qualities_produce_chords():
    for quality in QUALITY_NAMES:
        chords = diatonic_chords("A", quality)
        assert len(chords) > 0, f"No chords for quality {quality!r}"
