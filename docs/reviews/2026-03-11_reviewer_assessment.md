# Reviewer Assessment — 2026-03-11

**App state**: Post-M6 UI redesign — card-panel navigation, tabbed lesson view, lick cross-references, pentatonic key view, terminal size warning, lick linking in lesson bodies.

---

## Navigation

The redesign is a genuine improvement over the previous layout. The card-panel style with tree navigation on the left and content on the right is clean and consistent across all four screens. The TabbedContent approach in the Lessons screen (Lesson / Exercises / Licks) is particularly well-suited to the target audience — an intermediate player who wants to read about a scale and immediately see a phrase to practice without leaving the screen. This directly addresses the previous feedback about the lesson/practice split feeling disconnected.

**What works well:**
- The tree tracks are collapsed by default — not overwhelming on first entry
- Numbered tracks (`01.`, `02.`) make the curriculum order legible at a glance
- Introduction node above the tracks sets the right expectation
- The Key View chord strip with inline diagram is the most useful single feature for intermediate players — it answers "what key am I in, what chords are available, what does one of them look like" without switching screens
- The metronome in the Tools screen is well-placed — practitioners will have it open alongside lessons
- Orientation track correctly hides the Exercises and Licks tabs (no drills before you can play)

**Issues:**

The `escape` key behaviour on the Lessons screen is inconsistent: pressing escape when a lesson is open returns to the overview; pressing escape from the overview goes to Welcome. This is discoverable but not obvious. A breadcrumb or current-location indicator in the border title would help (it does update, but users may miss it).

The Practice screen now feels somewhat redundant for users who found what they needed in the Lessons screen. Its value is as the unfiltered full library — but there is no copy on the Practice overview that says "this is the complete library; lessons only show you a filtered subset." That framing would clarify why both screens exist.

---

## Music Theory Accuracy

### Keys and diatonic degrees

All diatonic chord formulas in `keys.py` were verified and are correct:
- Major, natural minor, Dorian, Phrygian, Lydian, Mixolydian all produce correct Roman numerals and chord qualities for every degree.
- Natural minor correctly uses `v minor` (not `V major`), which is right for Aeolian — the harmonic minor `V` is not in scope here and the lessons do not claim otherwise.

### Blues quality in the Key View — substantive issue

When the user selects **Blues** in the Key View, the chord strip shows the natural minor diatonic chords (Am, B°, C, Dm, Em, F, G in A). This is **misleading for intermediate players**. Blues harmony is built on three dominant 7th chords — I7, IV7, V7 (A7, D7, E7 in the key of A). Showing minor diatonic chords implies you would play over Am, Dm, Em, which is the natural minor context, not the blues context. A player who opens the Blues scale view to understand what to play over a 12-bar blues will get the wrong picture.

Options: show the three dominant 7th chords explicitly for Blues (A7, D7, E7), or add a note in the chord strip saying "Blues uses I7–IV7–V7 harmony" instead of displaying the natural minor set.

### Bm and F in the Open Chords track

Track 02 is titled "Open Chords" but positions 9 and 10 are Bm and F — both full barre chords. This is a category mismatch. Bm has no practical open voicing; F (full barre) is one of the hardest chords for beginners. These should either be labelled explicitly as "First Barre Chords" within the track, or moved to a short section between Tracks 02 and 05 with that framing. Calling them open chords when they require a full index finger barre is a beginner friction point.

### Strumming basics sequencing

`strumming_basics` is at Track 03, position 6 — the last lesson in First Progressions. But strumming is needed from the first time a player opens the app and tries to play a chord. The first three tracks assume the player already knows how to hold a pick, strum down-strokes, and produce sound. This is fine if the stated prerequisite is "you can already make sound on the guitar" — but the welcome screen does not state that. If strumming is genuinely a beginner topic, it should be Track 02, position 0 or 1. If the app assumes the player can already strum, the welcome screen should say so.

### Lydian lick key mismatch

The `lydian_raised_fourth` lick is in **G Lydian**, but the Lydian mode lesson teaches the position in **F Lydian** at the 12th–15th fret region. The lesson body directs the player to [4] Practice for that specific lick, but the key and fret region will be different. This is not an error (the shapes are transposable) but it will cause confusion — the player will have memorised a shape at frets 12–15 in F and then find the lick at a completely different position in G. Either align the lick key to F, or explicitly note in both the lesson and the lick that the key differs.

### Phrygian dominant — mentioned but not explained

The Phrygian lesson correctly introduces Phrygian dominant as a variation but says "while technically a different mode (the 5th mode of harmonic minor), it is closely related." This is accurate but the wording "5th mode of harmonic minor" will mean nothing to someone who has not studied harmonic minor. Since harmonic minor is not covered anywhere in the curriculum, this sentence hangs. Either cut it to just "a common variation with a raised 3rd" or mark it explicitly as advanced/outside this curriculum's scope.

---

## Content Gaps for Intermediate Players

### Major scale licks — significant gap

Track 08 is seven lessons on the major scale with zero lick cross-references and zero licks in the library. This is the biggest content gap relative to the target audience. Intermediate players use the major scale constantly — it is the basis of classic rock solos (Comfortably Numb solo, Hotel California), country lead, and pop melody. The minor pentatonic and modes have dedicated licks; the major scale has none. At minimum, one major scale lick (a three-note-per-string ascending run, or a classic melodic phrase in the style of classic rock) would close this gap.

### Natural minor lick coverage

Track 07 is seven lessons (intro + five positions + scale chords) with a single lick (`natural_minor_descent`). The descent covers position 1 only. Positions 2–5 and the `minor_scale_chords` lesson have no associated lick. One lick covering positions 3–4 (the upper-neck range) would give intermediate players something to practice in the less familiar positions.

### Pentatonic positions 3, 4, 5

Positions 3, 4, and 5 of the minor pentatonic have no lick cross-references. Position 1 and 2 are covered. For an intermediate player trying to break out of the box, positions 3–5 are exactly where they are stuck. A connector lick or a phrase demonstrating position 4 (the one most players skip) would be high value.

### Expressive technique — absent

The app currently has no lessons on:
- **String bending** (touched in `pent_bend_release` but not taught)
- **Vibrato** (not mentioned anywhere — the most important expressive technique)
- **Hammer-ons and pull-offs** (standard lead vocabulary, implied but never explained)
- **Slides** (mentioned in `major_pent_country_walk` lick description, not taught)

These are not music theory topics, so they sit outside the current curriculum philosophy. But for intermediate players, these techniques are the difference between playing notes and playing music. A short "Techniques" section — even just four one-page lessons — would address the most common intermediate plateau: knowing what notes to play but not how to make them sound good.

---

## Reference Content

The reference tables (Intervals, Scale Formula, Chord Formulas, Key Signatures, Tunings, Capo Chart, Barre Positions, Diatonic All Keys, Notes on Strings) are comprehensive and accurate. The Diatonic Chords All Keys table is particularly useful for intermediate players who are learning to analyse songs. The barre position finder is clean and practical.

The new pentatonic/blues options in the Key View scale selector are a welcome addition — fixing what was genuinely the most obvious gap in the previous version. The full-neck scale display with position bracketing is the strongest visual feature in the app.

---

## Summary

| Area | Status |
|---|---|
| Navigation structure | Strong improvement — no major issues |
| Theory accuracy | Accurate except Blues chord strip context |
| Bm/F in Open Chords | Category mismatch — needs label clarification |
| Lick coverage | Adequate for pentatonic/modes; missing major scale entirely |
| Expressive technique | Out of scope but noticeably absent for intermediate players |
| Key View | Now complete with pentatonics; Blues chord logic needs fix |
| Lydian lick key | Minor confusion — align keys or add note |

**Priority fixes before public release:**
1. Blues chord strip: show I7–IV7–V7 instead of natural minor chords
2. Bm/F labelling in Open Chords track
3. Lydian lick key alignment

**Recommended additions (post-release):**
1. Major scale lick(s) for Track 08
2. Natural minor lick(s) for upper positions
3. Pentatonic licks for positions 3–5
4. Short Techniques section (bending, vibrato, hammer-ons, slides)
