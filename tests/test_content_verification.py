"""Mathematical verification of all music content.

Every diagram block in lessons/exercises/licks and every entry in the data
layer is checked against actual music theory: pitch classes are recomputed
from standard tuning + frets and compared with what the chord name, degree
label, or key/scale frontmatter claims.

Rendering checks cannot catch a wrong note; these tests exist because the
2026-07-11 audit (docs/reviews/) found that hand-authored content drifts —
reversed string arrays, off-by-one frets, mislabeled degrees. New content
must pass here before it ships.
"""

from __future__ import annotations

import re
from pathlib import Path

import frontmatter
import pytest
import yaml

from guitar_tui.engine.dispatcher import dispatch

CONTENT_DIR = Path(__file__).parent.parent / "guitar_tui" / "content"
DATA_DIR = Path(__file__).parent.parent / "guitar_tui" / "data"

_DIAGRAM_RE = re.compile(r"```diagram\n(.*?)```", re.DOTALL)

# ── pitch math ─────────────────────────────────────────────────────────────────

_NOTE_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_PC_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Open-string pitch classes by frets-array index (0 = low E .. 5 = high e).
_OPEN_PC = [4, 9, 2, 7, 11, 4]
# Open-string pitch classes by string number (1 = high e .. 6 = low E).
_STRING_PC = {1: 4, 2: 11, 3: 7, 4: 2, 5: 9, 6: 4}

_DEGREE_SEMITONES = {
    "1": 0, "b2": 1, "2": 2, "#2": 3, "b3": 3, "3": 4, "4": 5, "#4": 6,
    "b5": 6, "5": 7, "#5": 8, "b6": 8, "6": 9, "b7": 10, "7": 11,
}

_QUALITY_INTERVALS: dict[str, set[int]] = {
    "": {0, 4, 7}, "m": {0, 3, 7}, "7": {0, 4, 7, 10}, "maj7": {0, 4, 7, 11},
    "m7": {0, 3, 7, 10}, "sus2": {0, 2, 7}, "sus4": {0, 5, 7},
    "add9": {0, 2, 4, 7}, "5": {0, 7}, "dim": {0, 3, 6}, "°": {0, 3, 6},
    "m7b5": {0, 3, 6, 10}, "dim7": {0, 3, 6, 9}, "6": {0, 4, 7, 9},
    "m6": {0, 3, 7, 9}, "9": {0, 2, 4, 7, 10}, "aug": {0, 4, 8},
}

# Qualities where a voicing may omit the perfect 5th (standard practice,
# e.g. the open C7). The 5th is structural for dim/aug/power chords.
_FIFTH_OMITTABLE = {"", "m", "7", "maj7", "m7", "6", "m6", "9", "add9", "sus2", "sus4"}

_SCALE_FORMULAS: dict[str, list[int]] = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "natural_minor": [0, 2, 3, 5, 7, 8, 10],
    "minor_pentatonic": [0, 3, 5, 7, 10],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "major_pentatonic": [0, 2, 4, 7, 9],
    "blues_scale": [0, 3, 5, 6, 7, 10],
    "blues": [0, 3, 5, 6, 7, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "phrygian_dominant": [0, 1, 4, 5, 7, 8, 10],
    "hungarian_minor": [0, 2, 3, 6, 7, 8, 11],
    "whole_tone": [0, 2, 4, 6, 8, 10],
    "diminished": [0, 2, 3, 5, 6, 8, 9, 11],
    "hirajoshi": [0, 2, 3, 7, 8],
}

# Licks that intentionally use notes outside their declared scale (chromatic
# passing tones etc.). Add the slug here with a justification comment.
_OUTSIDE_SCALE_ALLOWED: set[str] = set()

_CHORD_NAME_RE = re.compile(r"^([A-G][#b]?)(m7b5|maj7|dim7|add9|sus2|sus4|dim|aug|m7|m6|m|7|6|9|5|°)?$")


def _pc_of(name: str) -> int:
    pc = _NOTE_PC[name[0].upper()]
    for ch in name[1:]:
        pc += 1 if ch == "#" else -1 if ch == "b" else 0
    return pc % 12


def _pc_name(pc: int) -> str:
    return _PC_NAMES[pc % 12]


def _parse_chord_title(title: str) -> tuple[int, str] | None:
    """Try to extract (root_pc, quality) from a diagram title.

    Handles plain names ("E7", "Cadd9"), verbose names ("C Major", "A minor"),
    and titles with a dash-separated segment ("I — G Major", "C Major — G-shape").
    Returns None when no segment parses — the diagram is then skipped, not failed.
    """
    for segment in re.split(r"\s+[—–-]\s+", title.strip()):
        seg = segment.strip().split(" (")[0].strip()  # drop parentheticals
        m = re.match(r"^([A-G][#b]?)\s+(major|minor|diminished)$", seg, re.IGNORECASE)
        if m:
            qual = {"major": "", "minor": "m", "diminished": "dim"}[m.group(2).lower()]
            return _pc_of(m.group(1)), qual
        m = _CHORD_NAME_RE.match(seg)
        if m:
            root, qual = m.group(1), m.group(2) or ""
            if qual in _QUALITY_INTERVALS:
                return _pc_of(root), qual
    return None


def _chord_pcs(frets: list[int | None], base_fret: int) -> set[int]:
    pcs: set[int] = set()
    for i, f in enumerate(frets):
        if f is None:
            continue
        actual = f if f == 0 else (base_fret + f - 1 if base_fret > 1 else f)
        pcs.add((_OPEN_PC[i] + actual) % 12)
    return pcs


def _assert_chord_matches(tag: str, root_pc: int, quality: str, actual: set[int]) -> None:
    expected = {(root_pc + i) % 12 for i in _QUALITY_INTERVALS[quality]}
    required = set(expected)
    if quality in _FIFTH_OMITTABLE:
        required.discard((root_pc + 7) % 12)
    wrong = actual - expected
    missing = required - actual
    assert not wrong, (
        f"{tag}: sounds {sorted(map(_pc_name, actual))}, which includes "
        f"{sorted(map(_pc_name, wrong))} not in the chord ({sorted(map(_pc_name, expected))})"
    )
    assert not missing, (
        f"{tag}: sounds {sorted(map(_pc_name, actual))}, missing required "
        f"tones {sorted(map(_pc_name, missing))}"
    )


# ── content collection ─────────────────────────────────────────────────────────


def _collect_blocks() -> list[tuple[str, dict, dict]]:
    """Return (block_id, frontmatter_metadata, spec_dict) for every diagram block."""
    blocks: list[tuple[str, dict, dict]] = []
    for md in sorted(CONTENT_DIR.rglob("*.md")):
        post = frontmatter.load(md)
        rel = str(md.relative_to(CONTENT_DIR))
        for i, raw in enumerate(_DIAGRAM_RE.findall(post.content)):
            spec = yaml.safe_load(raw)
            blocks.append((f"{rel}#{i}", post.metadata, spec))
    return blocks


_ALL_BLOCKS = _collect_blocks()
_CHORD_BLOCKS = [b for b in _ALL_BLOCKS if b[2].get("type") == "chord"]
_SCALE_BLOCKS = [b for b in _ALL_BLOCKS if b[2].get("type") == "scale"]
_FRETBOARD_BLOCKS = [b for b in _ALL_BLOCKS if b[2].get("type") == "fretboard"]
_KEYED_TABS = [
    b for b in _ALL_BLOCKS
    if b[2].get("type") == "tab" and b[1].get("key") and b[1].get("scale")
]

_MEASURED_TABS = [
    b for b in _ALL_BLOCKS
    if b[2].get("type") == "tab"
    and any(line.get("measures") for line in b[2].get("lines", []))
]

_CHORD_FILES = sorted((DATA_DIR / "chords").glob("*.yaml"))
_SCALE_FILES = sorted((DATA_DIR / "scales").glob("*.yaml"))


def _ids(blocks: list[tuple[str, dict, dict]]) -> list[str]:
    return [b[0] for b in blocks]


# ── every diagram renders with consistent geometry ─────────────────────────────


@pytest.mark.parametrize("block", _ALL_BLOCKS, ids=_ids(_ALL_BLOCKS))
def test_diagram_renders_and_aligns(block: tuple[str, dict, dict]) -> None:
    tag, _, spec = block
    plain = dispatch(spec).plain
    lines = plain.split("\n")
    dtype = spec.get("type")

    if dtype == "chord":
        for line in lines:
            if any(c in line for c in "│╒├└"):
                assert len(line) == 25, f"{tag}: chord row width {len(line)} != 25: {line!r}"
    elif dtype in ("scale", "fretboard"):
        rows = [l for l in lines if len(l) > 2 and l[1] == " " and l[0] in "eBGDAE" and "──" in l]
        assert len({len(r) for r in rows}) == 1, f"{tag}: unequal string-row widths"
    elif dtype == "tab":
        staff = [l for l in lines if len(l) > 3 and l[1:3] == " |" and l[0] in "eBGDAE"]
        for start in range(0, len(staff), 6):
            group = staff[start:start + 6]
            assert len({len(r) for r in group}) == 1, f"{tag}: unequal tab staff widths"
            for row in group:
                assert " " not in row[3:].rstrip(), f"{tag}: space inside staff: {row!r}"


# ── tab measures: every bar in a line spans the same number of slots ───────────


@pytest.mark.parametrize("block", _MEASURED_TABS, ids=_ids(_MEASURED_TABS))
def test_tab_measures_equal_slots(block: tuple[str, dict, dict]) -> None:
    """Bars drawn on one staff must be rhythmically (and visually) equal length.

    The 2026-07-12 audit found bars that summed to 7 slots next to bars of 8 —
    the renderer draws them without complaint, just narrower.
    """
    tag, _, spec = block
    for line in spec.get("lines", []):
        measures = line.get("measures")
        if not measures:
            continue
        sums = [
            sum(beat.get("duration", 1) for beat in measure["beats"])
            for measure in measures
        ]
        assert len(set(sums)) == 1, f"{tag}: unequal bar lengths {sums}"


# ── chord diagrams sound like their titles ─────────────────────────────────────


@pytest.mark.parametrize("block", _CHORD_BLOCKS, ids=_ids(_CHORD_BLOCKS))
def test_chord_diagram_matches_title(block: tuple[str, dict, dict]) -> None:
    tag, _, spec = block
    parsed = _parse_chord_title(spec.get("title") or "")
    if parsed is None:
        pytest.skip("title is not a parseable chord name")
    root_pc, quality = parsed
    actual = _chord_pcs(spec["frets"], spec.get("base_fret", 1))
    _assert_chord_matches(tag, root_pc, quality, actual)


# ── scale diagrams: degrees, roots, completeness ───────────────────────────────


@pytest.mark.parametrize("block", _SCALE_BLOCKS, ids=_ids(_SCALE_BLOCKS))
def test_scale_diagram_degrees(block: tuple[str, dict, dict]) -> None:
    tag, _, spec = block
    root_pc = _pc_of(spec["root"])
    for n in spec["positions"]:
        pc = (_STRING_PC[n["string"]] + n["fret"]) % 12
        deg = n.get("degree")
        if deg is not None:
            assert deg in _DEGREE_SEMITONES, f"{tag}: unknown degree {deg!r}"
            expected = (root_pc + _DEGREE_SEMITONES[deg]) % 12
            assert pc == expected, (
                f"{tag}: string {n['string']} fret {n['fret']} is {_pc_name(pc)}, "
                f"but degree {deg} of {spec['root']} is {_pc_name(expected)}"
            )
        if n.get("root"):
            assert pc == root_pc, (
                f"{tag}: ({n['string']},{n['fret']}) flagged root but is {_pc_name(pc)}"
            )


@pytest.mark.parametrize("block", _SCALE_BLOCKS, ids=_ids(_SCALE_BLOCKS))
def test_scale_diagram_box_complete(block: tuple[str, dict, dict]) -> None:
    """Every in-scale note inside the declared fret_range must be shown."""
    tag, _, spec = block
    if not spec.get("fret_range"):
        pytest.skip("no explicit fret_range")
    lo, hi = spec["fret_range"]
    scale_pcs = {(_STRING_PC[n["string"]] + n["fret"]) % 12 for n in spec["positions"]}
    listed = {(n["string"], n["fret"]) for n in spec["positions"]}
    for string in range(1, 7):
        for fret in range(lo, hi + 1):
            pc = (_STRING_PC[string] + fret) % 12
            if pc in scale_pcs:
                assert (string, fret) in listed, (
                    f"{tag}: string {string} fret {fret} = {_pc_name(pc)} is in the "
                    f"scale and inside fret_range [{lo},{hi}] but missing from the box"
                )


# ── fretboard note-name labels ─────────────────────────────────────────────────


@pytest.mark.parametrize("block", _FRETBOARD_BLOCKS, ids=_ids(_FRETBOARD_BLOCKS))
def test_fretboard_labels_match_pitch(block: tuple[str, dict, dict]) -> None:
    tag, _, spec = block
    for n in spec.get("highlights", []):
        label = (n.get("label") or "").strip()
        if not re.fullmatch(r"[A-G][#b]?", label):
            continue
        pc = (_STRING_PC[n["string"]] + n["fret"]) % 12
        assert pc == _pc_of(label), (
            f"{tag}: string {n['string']} fret {n['fret']} is {_pc_name(pc)}, labeled {label!r}"
        )


# ── lick tabs stay inside their declared scale ─────────────────────────────────


@pytest.mark.parametrize("block", _KEYED_TABS, ids=_ids(_KEYED_TABS))
def test_lick_notes_in_declared_scale(block: tuple[str, dict, dict]) -> None:
    tag, meta, spec = block
    if meta.get("slug") in _OUTSIDE_SCALE_ALLOWED:
        pytest.skip("slug allowlisted for chromatic content")
    formula = _SCALE_FORMULAS.get(meta["scale"])
    assert formula is not None, f"{tag}: unknown scale {meta['scale']!r}"
    allowed = {(_pc_of(meta["key"]) + i) % 12 for i in formula}
    for line in spec.get("lines", []):
        measures = line.get("measures") or [{"beats": line.get("beats", [])}]
        for measure in measures:
            for beat in measure["beats"]:
                if beat.get("rest"):
                    continue
                for i, fret in enumerate(beat.get("notes", [])):
                    if fret is None:
                        continue
                    pc = (_OPEN_PC[i] + fret) % 12
                    assert pc in allowed, (
                        f"{tag}: string index {i} fret {fret} = {_pc_name(pc)} is not in "
                        f"{meta['key']} {meta['scale']} ({sorted(map(_pc_name, allowed))})"
                    )


# ── data layer: chord voicings ─────────────────────────────────────────────────


def _collect_voicings() -> list[tuple[str, str, dict]]:
    out: list[tuple[str, str, dict]] = []
    for path in _CHORD_FILES:
        doc = yaml.safe_load(path.read_text())
        for entry in doc.get("chords", []):
            for v in entry.get("voicings") or [entry]:
                out.append((f"{path.name}:{entry['name']}/{v.get('id', 'legacy')}", entry["name"], v))
    return out


_VOICINGS = _collect_voicings()


@pytest.mark.parametrize("item", _VOICINGS, ids=[v[0] for v in _VOICINGS])
def test_chord_data_voicing(item: tuple[str, str, dict]) -> None:
    tag, name, voicing = item
    m = _CHORD_NAME_RE.match(name)
    assert m, f"{tag}: chord name {name!r} is not parseable — extend the name grammar"
    root_pc, quality = _pc_of(m.group(1)), m.group(2) or ""
    actual = _chord_pcs(voicing["frets"], voicing.get("base_fret", 1))
    _assert_chord_matches(tag, root_pc, quality, actual)
    barre = voicing.get("barre")
    if barre:
        for string in range(barre["from_string"], barre["to_string"] + 1):
            fret = voicing["frets"][6 - string]
            if fret is not None and fret != 0:
                assert fret >= barre["fret"], (
                    f"{tag}: string {string} fret {fret} sits behind the barre at {barre['fret']}"
                )


# ── data layer: scale positions ────────────────────────────────────────────────


def _collect_scale_positions() -> list[tuple[str, dict, dict]]:
    out: list[tuple[str, dict, dict]] = []
    for path in _SCALE_FILES:
        doc = yaml.safe_load(path.read_text())
        for pos in doc.get("positions", []):
            out.append((f"{path.name}:pos{pos.get('id')}", doc, pos))
    return out


_SCALE_POSITIONS = _collect_scale_positions()


@pytest.mark.parametrize("item", _SCALE_POSITIONS, ids=[p[0] for p in _SCALE_POSITIONS])
def test_scale_data_position(item: tuple[str, dict, dict]) -> None:
    tag, doc, pos = item
    root_pc = _pc_of(doc["key"])
    allowed = {(root_pc + _DEGREE_SEMITONES[d]) % 12 for d in doc["intervals"]}
    lo, hi = pos["fret_range"]
    seen: set[tuple[int, int]] = set()

    for n in pos["notes"]:
        key = (n["string"], n["fret"])
        assert key not in seen, f"{tag}: duplicate note {key}"
        seen.add(key)
        pc = (_STRING_PC[n["string"]] + n["fret"]) % 12
        assert pc in allowed, f"{tag}: {key} = {_pc_name(pc)} is not in the scale"
        assert lo <= n["fret"] <= hi, f"{tag}: {key} outside fret_range [{lo},{hi}]"
        deg = n.get("degree")
        if deg is not None:
            expected = (root_pc + _DEGREE_SEMITONES[deg]) % 12
            assert pc == expected, (
                f"{tag}: {key} is {_pc_name(pc)}, labeled degree {deg} (= {_pc_name(expected)})"
            )
        if n.get("root"):
            assert pc == root_pc, f"{tag}: {key} flagged root but is {_pc_name(pc)}"

    # Both E strings are the same pitch — a box must treat them identically.
    s1 = sorted(f for s, f in seen if s == 1)
    s6 = sorted(f for s, f in seen if s == 6)
    assert s1 == s6, f"{tag}: string 1 frets {s1} != string 6 frets {s6}"

    # Completeness: every in-scale fret inside the declared range must be present.
    for string in range(1, 7):
        for fret in range(lo, hi + 1):
            if (_STRING_PC[string] + fret) % 12 in allowed:
                assert (string, fret) in seen, (
                    f"{tag}: string {string} fret {fret} is in scale, inside "
                    f"fret_range [{lo},{hi}], but missing from the position"
                )


@pytest.mark.parametrize("path", _SCALE_FILES, ids=[p.name for p in _SCALE_FILES])
def test_scale_data_formula(path: Path) -> None:
    doc = yaml.safe_load(path.read_text())
    formula = _SCALE_FORMULAS.get(doc["name"])
    if formula is None:
        pytest.skip(f"no canonical formula for {doc['name']!r} — add one to _SCALE_FORMULAS")
    stated = [_DEGREE_SEMITONES[d] for d in doc["intervals"]]
    assert stated == formula, (
        f"{path.name}: intervals {doc['intervals']} -> {stated}, expected {formula}"
    )
