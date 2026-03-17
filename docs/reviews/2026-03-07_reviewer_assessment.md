# Guitar TUI — Reviewer Assessment
*Technology column evaluation — Guitar Magazine*
*Date: 2026-03-07*
*Reviewer persona: Guitar magazine technology columnist*
*App state: M6 complete — 78 lessons across 11 tracks, Practice screen with Exercises + Licks Library*

---

## What Changed Since Last Review

The previous assessment (2026-03-05) identified the reference tooling as the main gap and the welcome screen as a weak first impression. Both complaints have been substantially addressed. A new Practice screen has also appeared that was not on the roadmap at the time of the last review. This assessment focuses on the new material and revisits the areas flagged before.

---

## Reference Tooling — Previous Gap, Now Closed

The single biggest criticism in the last review was that a tool billing itself as a "theory reference" did not surface its own data. That has been corrected.

The Reference tab in the Tools screen now includes:

- **Intervals table** — complete with quality names and semitone counts, well-formatted
- **Scale formula panel** — major scale interval formula (W W H W W W H) with mode derivations
- **Notes per string** — open to 12th fret for all six strings; this is one of the most-reached-for reference items mid-session
- **Diatonic chords for all 12 major keys** — organised in circle-of-fifths order with relative minor shown; this is the circle-of-fifths reference the last review asked for, delivered in a more useful form than a circle diagram would have been in a text interface
- **Barre position finder** — root note to E-shape fret (low E string) and A-shape fret (A string); this is exactly the sticky-note reference many intermediate players keep next to their amp

The key signatures, chord formulas, tunings, and capo tables were already in place from earlier work. The reference section is now genuinely comprehensive for the app's target audience. The previous verdict — "excellent lesson viewer, incomplete reference tool" — no longer stands.

One observation: the reference tab contains a lot of information in a single scrollable pane. A player who only wants the barre position finder has to scroll past the interval table, scale formula, and key signatures to get there. This is not a blocker, but a tab or collapsible section structure within the reference view would improve navigation as the content continues to grow. Not a priority for now — the current layout is functional — but worth tracking.

---

## Welcome Screen

The previous review gave the welcome screen its harshest criticism. The redesign has addressed all the specific complaints:

- The prerequisite note is present ("Assumes you can already form basic open chord shapes. New to guitar entirely? Start with a beginner course first, then return.")
- The curriculum arc is laid out in three phases — Playing foundation, Vocabulary expansion, Synthesis and application — giving a new user a genuine sense of the scope and sequencing
- The navigation guide now includes the new Practice screen
- The "New here?" nudge at the bottom directs to Track 1 specifically

The voice is appropriate: direct, scoped, not salesy. "Music theory in a shell" is a better pitch than "Music Theory at Your Fingertips." The lesson count is accurate. No further changes needed.

---

## Practice Screen — New

This is the most significant structural addition since the last review. The Practice screen introduces two things that the lesson-and-tools model cannot easily provide: drills that benefit from repetition outside of lesson context, and pre-packaged musical phrases to play over a looper.

**Exercises tab**

Four technique exercises are present: Chromatic Warm-Up, Spider Exercise, One-Minute Changes, Alternate Picking. All four are well-written with clear rules, target tempos, and common-mistake sections. The One-Minute Changes exercise in particular is pedagogically precise — the scoring table (Under 20 / 20–35 / 35–50 / 50+) gives a player an objective benchmark that the lesson format cannot provide. The Spider Exercise's explanation of *why* it works — cross-string coordination versus single-string strength — shows the same "explain the mechanism, not just the drill" quality seen in the best lesson content.

The exercise formatting is plain text inline — no separate lesson cards, no navigation. The scrollable pane approach is correct for this content type. Drills are scanned and returned to, not read linearly.

**Gap:** Only technique exercises exist. The CURRICULUM presumably has scale and chord exercise categories. A player working through Track 6 (pentatonic) has no corresponding scale exercises in the Practice screen. When those categories arrive, the grouping headers (technique / scale / chord) will pay off. For now, the Exercises tab feels sparse below the fold — a single category with four items. Worth noting that the tab promises more than it currently delivers.

**Licks Library tab**

Six licks across five scale categories: two pentatonic, one blues scale, one major pentatonic, one natural minor, one Dorian.

The lick content quality is notably high. Two standouts:

*Box 1 Ascending Run* — the "What to Listen For" section is exactly right. Rather than just describing the pattern, it explains the harmonic tension: "The G note creates slight tension over the Am chord — it is the b7 in that context. Over the G chord it becomes the root." This is the kind of ear-training content that distinguishes a good lesson from a tab library.

*Dorian Groove Phrase* — the backing progression is labelled "i – IV (the Dorian fingerprint)" and the "Why This Works" section directly connects the Dm–G movement to the mode's defining characteristic. The suggestion to play it as a rhythm-melody hybrid with a swing feel is a detail most resources skip entirely.

The looper setup instructions in both licks (tempo, chord order, bars per chord) are immediately actionable. A player can follow these exactly without any additional context.

**Gap — category coverage:** Phrygian, Lydian, and Mixolydian are completely absent. A player who finishes Track 10 and wants to practice Mixolydian has no corresponding lick. The modes track without matching lick content is an incomplete loop. These three categories need at least one entry each before the Practice screen can be considered complete alongside the modes curriculum.

**Gap — volume:** Six licks total is a starting library, not a library. The pentatonic category alone could justify four or five entries covering bends, hammer-ons, the b.b. King box, and the classic blues turnaround. The architecture is in place; the content depth needs to grow with use.

---

## Strumming Lesson

The previous review listed rhythm and strumming as absent. The `strumming_basics` lesson in Track 03 addresses this. The content is strong: the pendulum motion explanation, the ghost strum concept, and the specific warning about "stopping the hand between strokes" are exactly the corrections that need to be made in writing for a self-directed learner.

The ASCII count-strum grid (Count: 1  and  2  and  3  and  4  and / Strum: D  D  U  D  U  D  U) is an effective workaround for the absence of a dedicated rhythm diagram type. It communicates clearly within the text format's constraints.

One observation: Patterns 3 and 4 share the same ASCII representation in the lesson, which will confuse a careful reader. The pattern descriptions suggest they differ (Pattern 3 is written compactly as "D DU UDU"; Pattern 4 is "the same written out in full") but the ASCII grids appear identical. This should be reviewed and either the distinction clarified or the patterns merged.

---

## Modes Track (Track 10)

Reading this track in full for this review: it is the best track in the app.

The `modes_intro` lesson handles the classic pedagogy problem — two contradictory teaching approaches (relative vs. parallel) — by giving both names, explaining what each is for, and explicitly saying "you need both." That is the right call and is rarely done this cleanly in beginner-intermediate resources.

The `modes_in_context` lesson's table of "progression feel → likely mode → why" is the most immediately useful single reference item in the entire app. "Major I – bVII = Mixolydian because bVII major a whole step below I" gives a player a pattern-recognition shortcut that would otherwise take years of listening to develop consciously.

The closing line — "Modes are not formulas — they are colours. The theory helps you find them on the neck; your ear tells you when they sound right." — is the best sentence in the app.

---

## Song Analysis Track (Track 11)

The three-analysis `putting_it_together` lesson holds up. The *Brown Eyed Girl* / *Paranoid* / *Another Brick in the Wall* sequence is well-chosen: one clean major, one natural minor, one Dorian. Each analysis follows the same six-question framework laid out at the top, modelling the workflow rather than just describing it.

The *Paranoid* analysis is still the strongest — the observation about the absence of a conventional V chord and its effect on the song's energy level is a genuine harmonic insight, not a formula applied mechanically.

The summary table at the end ("What chord feels like home → The tonic" etc.) is a useful quick-reference format that should appear in more lessons that teach processes rather than facts.

---

## Target Audience Assessment — Revised

The previous assessment identified three user types. Updated view:

**Best fit (unchanged):** Intermediate players, developer/technical-musician overlap, keyboard-driven workflow preference.

**Secondary fit — now stronger:** Advanced beginners who have just moved past chord shapes. The strumming lesson, practice exercises, and lick library now provide practical material to bridge the gap between "I know the chord shapes" and "I sound musical." This was missing before.

**Still not well-served:** Advanced players. The ceiling at Track 11 remains. No jazz harmony, no secondary dominants, no modulation. This is a scope decision, not a flaw, but the app has no way to acknowledge or redirect these users. A brief note on the welcome screen ("Advanced players: the curriculum covers theory through modes and song analysis; jazz harmony and extended chord substitution are not covered") would manage expectations cleanly.

---

## Recommendations Summary

**High priority — complete the Practice screen:**
1. Add scale exercises to the Exercises tab (pentatonic, natural minor, major scale at minimum) — currently all exercises are technique-only
2. Add Phrygian, Lydian, and Mixolydian licks to the Licks Library — the modes track is incomplete without matching practice material

**Medium priority — content precision:**
3. Clarify Patterns 3 and 4 in the `strumming_basics` lesson — the ASCII grids are currently identical, which contradicts the text descriptions
4. Add 2–3 more pentatonic licks covering bends, the blues turnaround, and position-2 vocabulary — the pentatonic category is the highest-use and currently has only 2 entries

**Low priority — navigation:**
5. Consider a section navigation mechanism within the Reference tab as content continues to grow — currently a linear scroll through a large amount of information
6. Add a brief note on the welcome screen about the curriculum ceiling (theory through modes; jazz/advanced harmony not covered) to set expectations for advanced players

---

## Verdict

Guitar TUI has crossed from "excellent lesson viewer with reference gaps" to a genuinely complete theory companion for its target audience. The reference section is now thorough. The welcome screen orients rather than confuses. The Practice screen introduces a mode of use — drilling and lick practice — that the lesson format cannot serve.

The modes and song analysis tracks are the app's strongest content, and they are also the most advanced. That the best writing is in the hardest material is unusual for an educational tool and reflects well on the Instructor's judgment about where the most conceptual work was needed.

The remaining gaps are volume gaps, not architecture gaps: more licks, more exercises, more scale categories in Practice. The structure to hold all of that is in place. The app is ready to receive more content without any further infrastructure work.

**Recommended for:** Intermediate guitarists with a keyboard-driven workflow who want both a structured theory curriculum and a practical reference they can reach for mid-session. The addition of the Practice screen extends the recommendation to players who also want something to *play* — not just read — during a theory session.
