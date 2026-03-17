# UI/UX Redesign — Information Architecture v2

**Status**: ✓ Complete — Exercises/Licks tabs in lesson view, lick library in Practice, `[1]–[4]` nav retained, Tools screen kept as-is
**Owner**: Developer (UI/engine) + Instructor (content prerequisites)
**Rationale**: Current four-screen structure (Welcome / Lessons / Tools / Practice) reflects
build order, not use modes. This redesign aligns the app's structure with how it is
actually used.

---

## Three use modes → three screens

| Mode | User intent | Screen |
|------|-------------|--------|
| **Study** | Working on a concept — lesson, drill, lick | `[s]` |
| **Reference** | Jamming, mid-session lookup | `[r]` |
| **Analyze** | Decoding a song | `[a]` — reserved |

---

## Screen definitions

### `[s]` Study  *(merges current Lessons + Practice)*

**Left pane** — lesson navigator (unchanged from current Lessons screen)
- Track tree, `/` to open picker

**Right pane** — three fixed sub-tabs, in this order:

| Tab | Content | Key |
|-----|---------|-----|
| **Lesson** | Lesson content — text, diagrams, See Also | `1` or left/right arrow |
| **Drills** | Exercises contextual to the current lesson's track/module | `2` |
| **Lick** | Licks tagged to the current lesson via `licks:` frontmatter | `3` |

Sub-tab order is fixed — Lesson → Drills → Lick reflects the intended learning
sequence: understand → isolate the skill → play something real. It is not
user-reorderable.

**Default state (no lesson selected)**
Shows the welcome/orientation content: curriculum arc (three phases), prerequisite
note, navigation guide, and a "browse all licks" panel below. This remains the
first thing a new user sees. After any lesson is opened, returning to no-selection
shows a lighter prompt rather than the full welcome text.

**Licks in Study, not Reference**
Licks are pedagogical content tied to scale concepts and learning progression. A
player mid-jam does not reach for the lick library. A student finishing the Dorian
lesson does. "Browse all licks" lives in the Study default state (organised by
scale/mode category, as currently), not in Reference.

---

### `[r]` Reference  *(restructures current Tools)*

Optimised for zero-scroll jam use. Everything a player needs mid-session is
visible at once — no tab switching, no scrolling for common lookups.

**Layout**

```
┌─────────────────────┬──────────────────────────────────────┐
│  Key / Scale        │  Full-neck diagram                   │
│  selector           │                                      │
│                     │  Diatonic chord strip                │
│                     │  (interactive, , / . to navigate)    │
├─────────────────────┴──────────────────────────────────────┤
│  Quick panels (visible without scrolling at ≥120 cols)     │
│  Barre positions · Key signatures · Capo chart             │
├────────────────────────────────────────────────────────────┤
│  Extended tables (scroll for these — less time-sensitive)  │
│  Intervals · Scale formulas · Notes per string · Tunings   │
│  Diatonic chords — all keys                                │
└────────────────────────────────────────────────────────────┘
```

The current two-tab structure (Key View / Reference) is eliminated. The Key View
content and the most-needed reference panels coexist spatially. Extended tables
remain accessible but do not compete for screen space with the jam tools.

**Terminal width dependency**: the no-scroll layout for quick panels requires
≥120 columns. Below that threshold the quick panels stack vertically. This is
the same threshold decision needed for the terminal size recommendation (see
BACKLOG.md). Resolve that first before implementing the Reference layout.

**Metronome panel**

A visual metronome lives in the Reference screen as a persistent tool panel —
visible alongside the key/scale selector, not behind a tab or modal. It stays
running when the user adjusts the key selector or browses chords.

```
  BPM: 120  │  Time: 7/8  │  Group: 2+2+3
            │
  ○  ○  │  ○  ○  │  ○  ●  ○
  1  2  │  3  4  │  5  6  7
            │
  [Start]  [-5]  [+5]  [Tap]
```

Key bindings (when metronome panel is focused):
- `Space` — start/stop
- `-` / `+` — BPM -1 / +1
- `t` — tap tempo (two taps to set)

Group separators are the primary value-add over a phone metronome — they make
odd meters legible as felt groupings, not just a count of undifferentiated beats.

Audio is out of scope for v1 (platform fragmentation, asyncio jitter). Specified
fully in BACKLOG.md.

---

### `[a]` Analyze  *(reserved — future Songbook)*

Slot is reserved now. Key binding is active but shows a placeholder until
Songbook content is built. Reserving it prevents it from being displaced by
future additions and communicates to users that something is coming.

Content spec lives in `project/CURRICULUM.md` (section 4: Songbook).

---

## Key bindings

### Top-level navigation

| Key | Action |
|-----|--------|
| `s` | Study |
| `r` | Reference |
| `a` | Analyze (reserved) |
| `q` | Quit |

Letter bindings are semantic and memorable. Numbers (1/2/3/4) are retired as
top-level screen keys. Within-screen sub-navigation continues to use numbers
where appropriate (Study sub-tabs).

### Study screen

| Key | Action |
|-----|--------|
| `/` | Open lesson picker |
| `1` | Lesson tab |
| `2` | Drills tab |
| `3` | Lick tab |
| `Esc` | Return to no-selection state |

### Reference screen

| Key | Action |
|-----|--------|
| `,` | Previous diatonic chord |
| `.` | Next diatonic chord |
| `[` | Previous scale position |
| `]` | Next scale position |

---

## Migration map

| Current | New | Notes |
|---------|-----|-------|
| Welcome `[1]` | Study default state | Content preserved; shown on first launch and when no lesson is selected |
| Lessons `[2]` | Study `[s]` | Navigator unchanged; right pane gains Drills + Lick tabs |
| Tools `[3]` | Reference `[r]` | Two-tab structure eliminated; spatial layout |
| Practice `[4]` | Dissolved | Exercises → Study Drills tab; Licks → Study Lick tab + Study default state |
| — | Analyze `[a]` | Reserved; placeholder shown until Songbook is built |

---

## Content prerequisites (Instructor)

The Drills tab will show an empty state for any lesson whose track has no
exercises. An empty tab is worse than no tab — it signals an incomplete
curriculum. The following must be in place before the Drills tab ships:

### Minimum exercise coverage before launch

| Track | Status | Gap |
|-------|--------|-----|
| 1 — Orientation | No exercises planned | Acceptable — meta-lessons, no physical drill needed |
| 2 — Open Chords | No exercises | **Needs at minimum one**: clean-ringing arpeggio drill |
| 3 — First Progressions | No exercises | Covered by `one_minute_changes` (technique module) — acceptable |
| 4 — Theory Basics | No exercises planned | Acceptable — analytical track; could add interval ear-training prompt |
| 5 — Barre Chords | `barre_strength` ✓ | Good |
| 6 — Pentatonic | `pentatonic_sequences` ✓ | Good; 1–2 more welcome |
| 7 — Natural Minor | No exercises | **Needs one**: position-linking drill |
| 8 — Major Scale | No exercises | **Needs one**: three-notes-per-string introduction |
| 9 — Seventh Chords | No exercises | `seventh_voicings` planned in CURRICULUM.md — write before launch |
| 10 — Modes | No exercises | Acceptable for launch — analytical; drills are harder to define |
| 11 — Song Analysis | No exercises | Acceptable — capstone track |

### Lick coverage (already complete for launch)
All eight scale/mode categories have at least one lick. No blocking gap.

### `licks:` frontmatter (Developer + Instructor)
The `licks:` field on `LessonMeta` (see BACKLOG.md) becomes a prerequisite for
the Lick tab to show anything useful. Developer implements the field; Instructor
adds `licks:` to the ~10–12 relevant lessons in parallel.

---

## Implementation order

Each step is independently deployable and does not break the current structure
until the final cutover.

### Step 1 — Content + navigation groundwork (no structural change)
- Developer: implement `licks:` frontmatter field + lesson screen rendering
- Instructor: add `licks:` to relevant lessons
- Instructor: write missing exercises for Tracks 2, 7, 8, 9

### Step 2 — Study screen (Lessons → Study)
- Developer: add Drills + Lick sub-tabs to the lesson right pane
- Developer: contextual exercise filtering by track/module
- Developer: welcome content as default no-selection state with "browse all licks" panel
- Test: verify empty states are handled gracefully for lessons with no exercises/licks

### Step 3 — Reference screen (Tools → Reference)
- Developer: resolve terminal size minimum first (see BACKLOG.md)
- Developer: eliminate two-tab structure; implement spatial layout
- Developer: quick panels visible without scrolling at ≥120 cols

### Step 4 — Navigation cutover
- Developer: retire `[1]`–`[4]` top-level bindings; introduce `s`/`r`/`a`/`q`
- Developer: add `[a]` Analyze placeholder screen
- Developer: remove Practice as standalone screen

### Step 5 — Analyze screen (future)
- Triggered when Songbook content is ready
- Slot already reserved; binding already active

---

## Proposal: inline content blocks with show/hide toggle

**Status**: Proposed — evaluate before implementing

### The idea

Extend the existing diagram block pattern to support two new block types inline
in lesson Markdown: `exercise` and `lick`. Both resolve a slug to the canonical
source file at render time, pulling in the full content at the point in the
lesson where it is most relevant.

```
```exercise
slug: pentatonic_sequences
```

```lick
slug: pent_box1_run
```
```

This is the same architecture as `diagram` blocks — the lesson author places a
reference, the engine resolves it. The lesson file stays focused on explanation;
practice content is pulled in from its single canonical source.

### Why it is architecturally consistent

The diagram engine already does this: a YAML block in a Markdown file is
dispatched to a type-aware renderer. Adding `exercise` and `lick` as block types
is a natural extension of the same pattern. Benefits:

- **Single source of truth** — exercise/lick content lives once; changes
  propagate to every lesson that references it
- **Placement precision** — the author controls *where* in the lesson flow the
  exercise appears, not just *whether* it is associated
- **Reuse** — `chromatic_warmup` can be referenced from multiple lessons
  without duplication

### Show/hide toggle

Two levels:

**Global** — a Study screen toggle (`x` or similar): "compact mode" (lesson
text + diagrams only) vs "full mode" (lesson + inline exercises + licks).
Covers 80% of the use case.

**Per-block** — a focused exercise or lick block can be expanded/collapsed with
`Space`. Collapsed state shows a one-line header:
`▶ Exercise: Pentatonic Sequences  [Space to expand]`

Toggle state is **session-only** — reset on restart. No persistent user state
needed.

### Relationship to Drills/Lick sub-tabs

These are complementary, not competing:

| Mechanism | Purpose |
|-----------|---------|
| Inline blocks | Flow — "at this point in the explanation, try this" |
| Drills / Lick sub-tabs | Discovery — "here is everything relevant to this lesson by type" |

A lesson can have an inline lick block at the exact moment the concept lands,
and still list the same lick in the Lick sub-tab for reference. Both serve
different reading modes.

### Loader dependency constraint

Currently all three loaders are independent:
```
LessonLoader   — no dependencies
ExerciseLoader — no dependencies (second LessonLoader instance)
LickLoader     — no dependencies
```

Inline block resolution requires the lesson parser to resolve exercise and lick
slugs at parse time — which would couple the loaders. **The clean solution is a
two-pass approach**: parse all three loaders independently first, then resolve
inline blocks as a post-processing step in the app layer (same pattern as
`see_also` validation in `on_mount`). This preserves loader independence.

### Schema changes required
- New block types `exercise` and `lick` added to dispatcher alongside `diagram`
- `schemas/lesson_format.md` and `schemas/diagram_spec.md` updated
- `licks:` frontmatter (sub-tab driving) remains separate — different concern
- Future: `bpm` field on `exercise` blocks pre-sets the metronome widget

### Instructor assessment

**Inline is pedagogically stronger than tabs.** Tabs tell the reader *that* a
lick is associated with a lesson. Inline blocks tell the reader *when* to engage
with it — which is the more important information. The sequence understand →
demonstrate → play only works if the lick appears at the right moment in the
lesson text, not in a tab the reader may not think to open.

**Default states should differ by block type:**
- `exercise` blocks — **default collapsed.** Long content (rules, diagrams,
  progression notes) that interrupts reading flow. Reader opts in.
  `▶ Exercise: Pentatonic Sequences`
- `lick` blocks — **default expanded.** The payoff moment after understanding
  the concept. Shorter content; should be immediately visible.

**Toggle state — returning-learner concern.** Session-only state means a
returning learner always sees exercises expanded again on re-read, even if they
have already completed the drill. Not a blocker, but a known usability gap.
A lightweight persistent file (set of collapsed slugs per lesson) would fix it.
Decision to use session-only state should be made consciously, not by default.

**Browse-all licks outside lessons** — fully compatible. Slug references mean
the same lick content appears in three places with zero duplication: inline in
the lesson, in the Lick sub-tab, and in the browse-all view in Study default
state. A player browsing phrases without being in a lesson is a distinct use
case that the architecture supports for free.

### Evaluate before implementing
This proposal should be assessed alongside the full Study screen redesign (Step 2)
before any code is written. The two-pass loading approach needs a design review.

---

## Open decisions

| Decision | Status | Notes |
|----------|--------|-------|
| Terminal size minimum | Unresolved | Blocks Reference layout — must be settled before Step 3 |
| `uv.lock` in `.gitignore` | Deferred | See DEPLOYMENT.md |
| Lesson picker as modal vs. persistent sidebar | Deferred | Current modal works; sidebar is a future refinement |
| Track progress indicator (e.g. "3 / 9") in lesson header | Deferred | Useful with `n`/`p` navigation; low effort once bindings exist |
