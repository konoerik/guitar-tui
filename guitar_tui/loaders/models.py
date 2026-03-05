"""Pydantic models for the music theory data layer.

These models validate YAML data loaded from guitar_tui/data/.
They are distinct from DiagramSpec models (engine layer, M2).

Scale positions store absolute fret numbers for a reference key (e.g. A).
Key transposition is out of scope for M1 — see DECISIONS.md D5 note.
"""

from pydantic import BaseModel, Field, field_validator, model_validator


# ── Chord models ──────────────────────────────────────────────────────────────

class BarreSpec(BaseModel):
    """A barre across one or more strings at a given fret."""

    fret: int = Field(ge=1)
    from_string: int = Field(ge=1, le=6)
    to_string: int = Field(ge=1, le=6)
    finger: int | None = Field(default=None, ge=1, le=4)


class ChordVoicing(BaseModel):
    """A single chord voicing within a ChordEntry.

    frets: 6 values, index 0 = low E (string 6), index 5 = high e (string 1).
           int = fret number (1-based); 0 = open string; None = muted (X).
    fingers: 6 values matching frets. 1–4 = finger number; None = no label.
    id: machine-readable voicing key, e.g. "open", "barre_5".
    label: human-readable label for the voicing selector, e.g. "Open", "Barre (5th fret)".
    """

    id: str = "default"
    label: str = "Default"
    frets: list[int | None]                      # exactly 6 values
    fingers: list[int | None] | None = None      # exactly 6 values if present
    base_fret: int = Field(default=1, ge=1)
    barre: BarreSpec | None = None

    @field_validator("frets")
    @classmethod
    def frets_length(cls, v: list) -> list:
        if len(v) != 6:
            raise ValueError(f"frets must have exactly 6 values, got {len(v)}")
        return v

    @field_validator("fingers")
    @classmethod
    def fingers_length(cls, v: list | None) -> list | None:
        if v is not None and len(v) != 6:
            raise ValueError(f"fingers must have exactly 6 values, got {len(v)}")
        return v


class ChordEntry(BaseModel):
    """All voicings for one chord name.

    YAML format (new):
        name: Am
        full_name: A minor
        voicings:
          - id: open
            label: Open
            frets: [null, 0, 2, 2, 1, 0]
            ...

    YAML format (legacy — single voicing at top level, backwards compatible):
        name: Am
        full_name: A minor
        frets: [null, 0, 2, 2, 1, 0]
        ...

    The model_validator normalises the legacy format transparently.
    """

    name: str
    full_name: str
    voicings: list[ChordVoicing]

    @model_validator(mode="before")
    @classmethod
    def normalize_legacy_format(cls, data: object) -> object:
        if not isinstance(data, dict):
            return data
        if "frets" in data and "voicings" not in data:
            # Legacy flat format: extract name/full_name, wrap the rest as one voicing
            voicing_data = {k: v for k, v in data.items() if k not in ("name", "full_name")}
            voicing_data.setdefault("id", "default")
            voicing_data.setdefault("label", "Default")
            return {
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "voicings": [voicing_data],
            }
        return data


class ChordLibrary(BaseModel):
    """Top-level wrapper for a chord YAML file."""

    chords: list[ChordEntry]


# ── Scale models ──────────────────────────────────────────────────────────────

class ScaleNote(BaseModel):
    """A single note within a scale position diagram.

    fret: absolute fret number for the reference key stored in ScalePattern.
    string: 1 = high e, 6 = low E (consistent with DiagramSpec convention).
    """

    string: int = Field(ge=1, le=6)
    fret: int = Field(ge=0)
    degree: str | None = None    # e.g. "1", "b3", "4", "5", "b7"
    root: bool = False


class ScalePosition(BaseModel):
    """One fingering position of a scale pattern."""

    id: int = Field(ge=1)
    name: str                           # e.g. "Position 1"
    caged_shape: str | None = None      # "E", "D", "C", "A", or "G"
    fret_range: tuple[int, int]         # [low_fret, high_fret] for display
    notes: list[ScaleNote]

    @field_validator("fret_range")
    @classmethod
    def fret_range_valid(cls, v: tuple) -> tuple:
        if v[0] > v[1]:
            raise ValueError(f"fret_range low ({v[0]}) must be <= high ({v[1]})")
        return v


class ScalePattern(BaseModel):
    """A scale pattern with all fingering positions.

    Fret numbers are absolute for `key`. Transposition is M2+ scope.
    """

    name: str                   # slug-style, used as dict key, e.g. "minor_pentatonic"
    full_name: str              # display name, e.g. "Minor Pentatonic"
    key: str                    # reference key for stored fret numbers, e.g. "A"
    intervals: list[str]        # interval formula, e.g. ["1", "b3", "4", "5", "b7"]
    positions: list[ScalePosition]


# ── Tuning models ─────────────────────────────────────────────────────────────

class Tuning(BaseModel):
    """A guitar tuning.

    strings: 6 note names low to high, e.g. ["E2", "A2", "D3", "G3", "B3", "E4"].
    """

    name: str
    strings: list[str]

    @field_validator("strings")
    @classmethod
    def strings_length(cls, v: list) -> list:
        if len(v) != 6:
            raise ValueError(f"strings must have exactly 6 values, got {len(v)}")
        return v
