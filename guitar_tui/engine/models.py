"""DiagramSpec Pydantic models for the music-agnostic rendering engine.

These models define the interface between lesson content (M3) and the engine.
No imports from guitar_tui.data or guitar_tui.content are permitted here.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ── Chord ─────────────────────────────────────────────────────────────────────


class BarreDef(BaseModel):
    """A barre across one or more strings at a given fret.

    YAML uses 'from' and 'to' (Python keywords), so aliases are required.
    populate_by_name=True allows using either field name or alias.
    """

    model_config = ConfigDict(populate_by_name=True)

    fret: int = Field(ge=1)
    from_string: int = Field(ge=1, le=6, alias="from")
    to_string: int = Field(ge=1, le=6, alias="to")
    finger: int | None = Field(default=None, ge=1, le=4)


class ChordSpec(BaseModel):
    """Specification for a chord box diagram."""

    type: Literal["chord"]
    title: str | None = None
    caption: str | None = None
    frets: list[int | None]       # exactly 6; index 0 = low E, index 5 = high e
    fingers: list[int | None] | None = None  # exactly 6 if provided
    barre: BarreDef | None = None
    base_fret: int = Field(default=1, ge=1)

    @field_validator("frets")
    @classmethod
    def frets_length(cls, v: list) -> list:
        if len(v) != 6:
            raise ValueError(f"frets must have exactly 6 elements, got {len(v)}")
        return v

    @field_validator("fingers")
    @classmethod
    def fingers_length(cls, v: list | None) -> list | None:
        if v is not None and len(v) != 6:
            raise ValueError(f"fingers must have exactly 6 elements, got {len(v)}")
        return v


# ── Scale ─────────────────────────────────────────────────────────────────────


class ScaleNote(BaseModel):
    """A single note within a scale position diagram."""

    string: int = Field(ge=1, le=6)   # 1 = high e, 6 = low E
    fret: int = Field(ge=0)
    degree: str | None = None          # e.g. "1", "b3", "5"
    root: bool = False


class ScaleSpec(BaseModel):
    """Specification for a scale position diagram."""

    type: Literal["scale"]
    title: str | None = None
    caption: str | None = None
    root: str                          # root note name, e.g. "A", "F#"
    positions: list[ScaleNote]
    fret_range: tuple[int, int] | None = None  # auto-computed from positions if None
    highlight_root: bool = True


# ── Tab ───────────────────────────────────────────────────────────────────────


class TabBeat(BaseModel):
    """One beat/event in a tab line."""

    notes: list[int | None]   # exactly 6; index 0 = low E, index 5 = high e
    label: str | None = None

    @field_validator("notes")
    @classmethod
    def notes_length(cls, v: list) -> list:
        if len(v) != 6:
            raise ValueError(f"notes must have exactly 6 elements, got {len(v)}")
        return v


class TabLine(BaseModel):
    """One logical line (measure) of tablature."""

    beats: list[TabBeat]


class TabSpec(BaseModel):
    """Specification for a guitar tablature block."""

    type: Literal["tab"]
    title: str | None = None
    caption: str | None = None
    lines: list[TabLine]
    tempo: int | None = None
    time: str | None = None


# ── Fretboard ─────────────────────────────────────────────────────────────────


class FretNote(BaseModel):
    """A highlighted note on the fretboard."""

    string: int = Field(ge=1, le=6)   # 1 = high e, 6 = low E
    fret: int = Field(ge=0)
    label: str | None = None
    style: str = "highlight"           # "root", "highlight", or "muted"


class FretboardSpec(BaseModel):
    """Specification for a full or partial fretboard overview."""

    type: Literal["fretboard"]
    title: str | None = None
    caption: str | None = None
    highlights: list[FretNote]
    fret_range: tuple[int, int] = (0, 12)
    tuning: str = "standard"
    show_notes: bool = False


# ── Discriminated union ────────────────────────────────────────────────────────

DiagramSpec = Annotated[
    ChordSpec | ScaleSpec | TabSpec | FretboardSpec,
    Field(discriminator="type"),
]
