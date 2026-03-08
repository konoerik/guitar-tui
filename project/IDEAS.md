# Deferred Ideas

Content and feature ideas captured during planning. Review at the milestone noted — do not implement early.

---

## Review at M4 (UI design session)

### Songbook Area

A dedicated content section for theory breakdowns of real songs.

**What it is**: Analysis of a song's musical ingredients — key, mode, chord progression (Roman numerals), scales used, notable techniques, structural sections (verse/chorus/bridge). The song's identity and feel, not its notes.

**What it is not**: Reproduced tab, transcribed melodies, or note-for-note solos. Nothing that replicates the copyrighted expression of the original recording.

**Example — Sultans of Swing (Dire Straits)**:
- Key: D minor / F major
- Progression: Dm – C – Bb – C (verse); Dm – C – Bb – A (turnaround)
- Scales: D natural minor, D minor pentatonic, Dm blues scale on solos
- Techniques: hybrid picking, fingerstyle, position shifts, Knopfler's characteristic pull-off runs
- Notes: link to relevant Artist entry (Knopfler), link to lessons on minor pentatonic and natural minor

**UI questions for M4**:
- Separate screen or subsection of reference?
- How does it link to lessons and artist entries?
- Should progressions be rendered as a diagram (D2 Roman numeral display from the taxonomy)?

---

### Artist Area

A dedicated content section for style profiles and original exercises in the style of notable guitarists.

**What it is**: Characteristic vocabulary, preferred positions, signature techniques, and original licks/exercises that capture the style — similar to how published "Play like X" instructional books work.

**What it is not**: Transcriptions of actual solos or recordings. All tab/notation is original material written to demonstrate the style.

**Example — Mark Knopfler**:
- Style markers: fingerstyle without pick, hybrid picking runs, Telecaster neck pickup tone
- Preferred scales: D minor pentatonic (position 1 heavy), natural minor, occasional Dorian inflection
- Characteristic moves: descending pull-off runs on B/G strings, pedal tone patterns, double-stop thirds
- Original exercises: 4–6 short original licks demonstrating each characteristic move, with tab and fretboard diagram
- Notes: link to Sultans of Swing songbook entry, link to pentatonic and natural minor lessons

**UI questions for M4**:
- Separate screen or part of reference?
- Artist index — searchable? Browsable by style/genre/technique?
- How do original licks relate to the lesson system — are they mini-lessons, or reference-only?

---

### Styles Area

A content section organized by musical genre/style rather than by song or artist.

**What it is**: Theory and technique profiles for genres — the vocabulary, characteristic progressions, scales, and feel that define a style. Blues, rock, jazz, country, funk, classical fingerstyle, etc.

**Example — Blues**:
- Core theory: 12-bar blues form, dominant 7th chords, blues scale vs. minor pentatonic
- Characteristic techniques: bends, vibrato, call-and-response phrasing, shuffle feel
- Key artists entry links (e.g., BB King, SRV, Knopfler)
- Foundational progressions: I7–IV7–V7, quick-change variation, minor blues
- Links to relevant lessons, licks, and songbook entries

**Relationship to Songbook and Artist areas**: Styles is the top-level organizer. A song belongs to a style; an artist belongs to one or more styles. Navigation could flow Style → Artist → Song or Style → Lessons.

**UI questions for M4**:
- Is Styles the top-level navigation category that Songbook and Artist sit under?
- Or are all three peers in the main nav?
- Genre tagging on lessons — should lessons carry a `style` frontmatter tag?

---

## Copyright Boundary (applies to both areas)

Music theory is not copyrightable. The following are always safe:
- Key, tempo, time signature
- Chord progressions expressed as Roman numerals or chord names
- Scale and mode identification
- Description of techniques (fingerstyle, barre, bend, etc.)
- Structural analysis (verse/chorus form, turnarounds, etc.)

The following require original authorship — do not copy from recordings or published tab:
- Specific note sequences (melodies, solos)
- Rhythmic notation transcribed from a recording
- Tab reproduced from a published source

The model: educational analysis + original exercises. Same approach used by Hal Leonard, Guitar World lessons, and TrueFire courses.

---

## Review at M5 (Interactive Features design session)

### Prev/Next Lesson Navigation

In-lesson keyboard shortcuts to move to the previous or next lesson without reopening
the picker modal.

**The idea**: while reading a lesson in LessonMode, pressing `[` or `]` (or `n`/`p`,
or left/right arrow) loads the adjacent lesson in module order, updating the title and
scrolling to the top. The current lesson's position within its module determines what
"next" and "previous" mean.

**Design questions**:
- Key choice: `[`/`]` (bracket navigation, common in browser-style apps) vs. `n`/`p`
  vs. `←`/`→` arrows (arrows may conflict with scroll or Select widget focus)?
- Ordering: strictly within the current module (position field), or across all lessons
  in some global sequence (e.g. track order)?
- Edge behaviour: at the first or last lesson, should the binding wrap around, move to
  the adjacent module, or simply do nothing with a brief status message?
- Footer hint: show `[[] prev  []] next` dynamically, or only when a lesson is loaded?

---

### Numerical Lesson Navigation

A quick-access shortcut for jumping directly to a lesson by number from anywhere in
the app. The proposed flow: `2` (go to Lessons) → `/` (open picker) → type a number
→ lesson loads immediately.

**The idea**: lessons in the picker are numbered in display order. The user types the
number while the picker is open and the matching lesson is selected (or the list
filters). No mouse, no arrow-key scrolling through long lists.

**Design questions**:
- Is the number a persistent index (lesson 7 is always lesson 7) or a transient
  display index that changes if the lesson list changes?
- Single-digit only (≤9 lessons per module) or arbitrary number input with a short
  timeout?
- Does typing filter the list (like fuzzy search by number) or jump the cursor
  directly to that item?
- Should numbers be scoped per-module or global across all lessons?

---

### Chord Builder — Interval Explorer

An interactive utility for understanding how chords are constructed from intervals.
The user starts with a root note and adds intervals one at a time, watching the chord
name update as the voicing takes shape.

**The idea**: start with just a root. Add a major 3rd → you have the root and 3rd.
Add another root an octave up → power chord shape. Replace the 3rd with a 5th and
add a minor 7th → dominant 7th. Each addition shows what the resulting chord is
called and why, grounding chord names in interval logic rather than memorisation.

**Educational value**: the builder teaches that chord names are just descriptions of
interval stacks. A learner who builds an Am7 from scratch (root → minor 3rd → 5th →
minor 7th) understands it far better than one who memorised a fingering shape.

**Design questions**:
- Is this a fretboard-based builder (tap frets to add notes) or an abstract
  interval builder (buttons: +m3, +M3, +P5, +m7, +M7)?
- Does it show a chord diagram alongside the interval description?
- How does it handle enharmonics and inversions?
- Does it link to the Theory Web (M7) — e.g. "this chord appears in these keys"?
- Should it be a tab in ToolsMode or a dedicated screen?

---

## Review at M7 (Theory Web design session)

### Theory Web — Interconnected Reference

The reference area in M4 is two independent lookups: a chord selector and a scale
selector. Neither knows about the other. The Theory Web replaces this with a unified
view where every element reveals its musical context.

**The core idea**: music theory is a web, not a list. A scale implies chords. A chord
implies keys. A key implies progressions. The UI should reflect this — navigating the
theory is navigating the web.

**Scale View**

When a user selects a scale (e.g. A minor pentatonic):

```
┌─ A Minor Pentatonic ────────────────────────────────────────────┐
│                                                                  │
│  Positions: [ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]                      │
│  ┌────────────────────────────────────────┐                     │
│  │  [scale diagram — current position]    │                     │
│  └────────────────────────────────────────┘                     │
│                                                                  │
│  Diatonic chords                                                 │
│   Am    C     D     Em    G                                      │
│  [box] [box] [box] [box] [box]                                   │
│                                                                  │
│  Common progressions                                             │
│   Am – G – C – D    (I – bVII – bIII – IV)                      │
│   Am – F – C – G    (i – bVI – bIII – bVII)                     │
│                                                                  │
│  See also: lessons · artists · songs                             │
└──────────────────────────────────────────────────────────────────┘
```

**Chord View**

When a user selects a chord (e.g. Am):

```
┌─ Am — A minor ──────────────────────────────────────────────────┐
│                                                                  │
│  Voicings: [ Open ] [ Barre 5fr ] [ Barre 7fr ]                  │
│  ┌────────────────────┐                                          │
│  │ [chord diagram]    │                                          │
│  └────────────────────┘                                          │
│                                                                  │
│  Belongs to                                                      │
│   C major (vi)  ·  A minor (i)  ·  D minor (v)  ·  G major (ii) │
│                                                                  │
│  See also: lessons · progressions                                │
└──────────────────────────────────────────────────────────────────┘
```

**UI questions for M7**:
- Does the Theory Web replace the current Reference tab, or live alongside it?
- Should the Scale View and Chord View be separate tabs, or a single unified view
  where the selection type changes the displayed context?
- How are the diatonic chord boxes laid out — horizontally scrollable, or a grid?
- Does clicking a diatonic chord from the Scale View open the Chord View for that chord
  (navigating the web), or open a separate overlay?
- How does the progression panel render — as a tab diagram, or as chord name labels?

---

### Song Analysis Workflow — "Analyse a Song"

A guided interactive screen for reverse-engineering the theory of an unfamiliar song.
The learner starts from what they hear and arrives at the theory tools they need.

**The workflow** (keyboard-driven, no audio input):

```
Step 1 — What is the home chord?
  Select a note: [ A ] [ B ] [ C ] [ D ] [ E ] [ F ] [ G ]
  (and optionally # / b)

Step 2 — Major or minor feel?
  [ Major ]  [ Minor ]

Step 3 — Results
  Key: A minor
  ┌──────────────────────────────────────────────────────────┐
  │  Scale: A Natural Minor / A Minor Pentatonic             │
  │  Diatonic chords: Am  Bdim  C  Dm  Em  F  G              │
  │  Likely progression shapes: i–VII–VI  /  i–iv–VII  /...  │
  │  Suggested positions: [Pos 1 at 5fr]  [Pos 2 at 7fr]     │
  │                                                          │
  │  → Open in Theory Web      → Go to A Minor lessons       │
  └──────────────────────────────────────────────────────────┘
```

**The educational value**: the workflow teaches the analytical process — the same steps
a musician takes mentally — while immediately surfacing the tools needed to play. It is
the Theory Web used in reverse: start from what you hear, arrive at the theory.

**UI questions for M8**:
- Does this live as a dedicated screen ("Analyse"), or as a mode within the Theory Web?
- Should the results page be a static display or allow the user to drill into each
  element (clicking "A Minor Pentatonic" opens the Scale View for that scale)?
- How does capo affect the workflow? (e.g. "this is in E for the guitar but the
  singer's key is G — show me the capo position")
- Is the Songbook the "worked examples" section of the Song Analysis screen, or a
  separate area entirely?
