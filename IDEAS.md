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
