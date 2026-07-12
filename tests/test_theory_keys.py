"""Tests for music theory: note conversion, diatonic chords, capo chart, key signatures."""

import pytest

from guitar_tui.theory.keys import (
    CHARACTERISTIC_NOTE,
    KEY_NAMES,
    QUALITY_NAMES,
    capo_chart,
    diatonic_chords,
    key_context,
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


_NO_CHORD_QUALITIES = {"Hungarian Minor", "Whole Tone", "Diminished (W–H)", "Hirajoshi"}


def test_all_qualities_produce_chords():
    for quality in QUALITY_NAMES:
        chords = diatonic_chords("A", quality)
        if quality in _NO_CHORD_QUALITIES:
            assert chords == [], f"Expected no chord set for {quality!r}"
        else:
            assert len(chords) > 0, f"No chords for quality {quality!r}"


class TestEnharmonicName:
    def test_sharp_to_flat(self) -> None:
        from guitar_tui.theory.keys import enharmonic_name
        assert enharmonic_name("C#") == "Db"
        assert enharmonic_name("C#m") == "Dbm"
        assert enharmonic_name("Ab") == "G#"
        assert enharmonic_name("Abm") == "G#m"
        assert enharmonic_name("Eb7") == "D#7"

    def test_natural_roots_return_none(self) -> None:
        from guitar_tui.theory.keys import enharmonic_name
        assert enharmonic_name("C") is None
        assert enharmonic_name("Am") is None
        assert enharmonic_name("B°") is None


class TestChordTones:
    def test_triads_and_sevenths(self) -> None:
        from guitar_tui.theory.keys import chord_tones
        assert chord_tones("C") == ["C", "E", "G"]
        assert chord_tones("Am") == ["A", "C", "E"]
        assert chord_tones("C#°") == ["C#", "E", "G"]
        assert chord_tones("G7") == ["G", "B", "D", "F"]

    def test_unknown_quality_returns_none(self) -> None:
        from guitar_tui.theory.keys import chord_tones
        assert chord_tones("Cmaj9#11") is None
        assert chord_tones("") is None


# ── Key context (Key View header) ──────────────────────────────────────────────


class TestKeyContext:
    def test_a_minor_relative_major_c(self) -> None:
        ctx = key_context("A", "Minor")
        assert ctx is not None
        assert ctx.parent_major == "C"
        assert ctx.relative_label == "relative major"
        assert ctx.relative_name == "C"
        assert ctx.accidental_count == 0

    def test_c_major_relative_minor_am(self) -> None:
        ctx = key_context("C", "Major")
        assert ctx is not None
        assert ctx.relative_label == "relative minor"
        assert ctx.relative_name == "Am"
        assert ctx.accidental_count == 0

    def test_modes_of_c_share_parent_major(self) -> None:
        for root, quality in [
            ("D", "Dorian"), ("E", "Phrygian"), ("F", "Lydian"), ("G", "Mixolydian"),
        ]:
            ctx = key_context(root, quality)
            assert ctx is not None
            assert ctx.parent_major == "C", f"{root} {quality}"
            assert ctx.relative_label == "parent major"
            assert ctx.accidental_count == 0

    def test_e_minor_has_one_sharp(self) -> None:
        ctx = key_context("E", "Minor")
        assert ctx is not None
        assert ctx.parent_major == "G"
        assert ctx.accidental_count == 1

    def test_f_major_has_one_flat(self) -> None:
        ctx = key_context("F", "Major")
        assert ctx is not None
        assert ctx.accidental_count == -1
        assert ctx.relative_name == "Dm"

    def test_pentatonics_match_parent_quality(self) -> None:
        assert key_context("A", "Minor Pentatonic") == key_context("A", "Minor")
        assert key_context("C", "Major Pentatonic") == key_context("C", "Major")

    def test_blues_uses_relative_major(self) -> None:
        ctx = key_context("A", "Blues")
        assert ctx is not None
        assert ctx.relative_label == "relative major"
        assert ctx.relative_name == "C"

    def test_unknown_quality_returns_none(self) -> None:
        assert key_context("C", "Klezmer") is None

    def test_all_selector_combinations_covered(self) -> None:
        # Qualities derived from the major scale have a key context; scales
        # outside the major-key system (harmonic minor family, symmetric,
        # hirajoshi) intentionally return None.
        outside_major_system = {
            "Harmonic Minor", "Phrygian Dominant", "Hungarian Minor",
            "Whole Tone", "Diminished (W–H)", "Hirajoshi",
        }
        for key in KEY_NAMES:
            for quality in QUALITY_NAMES:
                ctx = key_context(key, quality)
                if quality in outside_major_system:
                    assert ctx is None, f"{key} {quality}"
                else:
                    assert ctx is not None, f"{key} {quality}"

    def test_enharmonic_parent_spelling(self) -> None:
        # Eb Minor -> parent F# major (6 sharps) per circle-of-fifths table.
        ctx = key_context("Eb", "Minor")
        assert ctx is not None
        assert ctx.parent_major == "F#"
        assert ctx.accidental_count == 6


# ── Characteristic notes ───────────────────────────────────────────────────────


class TestCharacteristicNote:
    def test_mode_intervals_and_symbols(self) -> None:
        assert CHARACTERISTIC_NOTE["Dorian"] == (9, "6")
        assert CHARACTERISTIC_NOTE["Phrygian"] == (1, "b2")
        assert CHARACTERISTIC_NOTE["Lydian"] == (6, "#4")
        assert CHARACTERISTIC_NOTE["Mixolydian"] == (10, "b7")
        assert CHARACTERISTIC_NOTE["Blues"] == (6, "b5")

    def test_plain_scales_have_no_characteristic(self) -> None:
        for quality in ("Major", "Minor", "Major Pentatonic", "Minor Pentatonic"):
            assert quality not in CHARACTERISTIC_NOTE

    def test_characteristic_note_is_in_scale(self) -> None:
        # The characteristic pitch must actually occur in the quality's chords/scale
        # family — spot-check via diatonic spelling: D Dorian's 6 is B.
        assert semitone_to_note((note_to_semitone("D") + 9) % 12) == "B"
        # E Phrygian's b2 is F.
        assert semitone_to_note((note_to_semitone("E") + 1) % 12) == "F"


# ── Track 16 scale families ────────────────────────────────────────────────────


class TestWorldScaleDegrees:
    def test_harmonic_minor_chords_a(self) -> None:
        chords = diatonic_chords("A", "Harmonic Minor")
        table = dict(chords)
        assert table["i"] == "Am"
        assert table["V"] == "E"        # the raised 7th creates a true dominant
        assert table["bIII+"] == "C+"
        assert table["vii°"] == "Ab°"   # G#° spelled via fixed chromatic table

    def test_phrygian_dominant_chords_e(self) -> None:
        chords = diatonic_chords("E", "Phrygian Dominant")
        table = dict(chords)
        assert table["I"] == "E"        # major I — the defining sound
        assert table["bII"] == "F"
        assert table["bVI+"] == "C+"

    def test_augmented_chord_tones(self) -> None:
        from guitar_tui.theory.keys import chord_tones
        assert chord_tones("C+") == ["C", "E", "Ab"]  # G# spelled Ab

    def test_new_scales_in_quality_map(self) -> None:
        for quality, scale in [
            ("Harmonic Minor", "harmonic_minor"),
            ("Phrygian Dominant", "phrygian_dominant"),
            ("Hungarian Minor", "hungarian_minor"),
            ("Whole Tone", "whole_tone"),
            ("Diminished (W–H)", "diminished"),
            ("Hirajoshi", "hirajoshi"),
        ]:
            from guitar_tui.theory.keys import QUALITY_TO_SCALE
            assert QUALITY_TO_SCALE[quality] == scale

    def test_new_characteristic_notes(self) -> None:
        assert CHARACTERISTIC_NOTE["Harmonic Minor"] == (11, "7")
        assert CHARACTERISTIC_NOTE["Phrygian Dominant"] == (4, "3")
        assert CHARACTERISTIC_NOTE["Hungarian Minor"] == (6, "#4")
