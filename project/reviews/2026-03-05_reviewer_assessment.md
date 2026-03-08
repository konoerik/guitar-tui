# Guitar TUI — Reviewer Assessment
*Technology column evaluation — Guitar Magazine*
*Date: 2026-03-05*
*Reviewer persona: Guitar magazine technology columnist*
*App state: M6 — 75+ lessons across 11 tracks (Tracks 1–11 complete)*

---

## First-Run Experience

The welcome screen is the weakest first impression in the app. "Music Theory at Your Fingertips" followed by three numbered menu items tells me almost nothing. A guitarist who has just installed this does not know whether it's aimed at absolute beginners or working musicians brushing up on theory. There is no "start here" directive, no summary of the content scope, and no sense of what to expect from 75+ lessons. Compare this to how the lessons themselves open — immediately engaging, with a clear premise and context. That energy needs to appear on the welcome screen too.

The navigation model is clean and logical once discovered. The tree structure in the Lessons view is well-organised. The Tools screen is functional. But the welcome screen should do more work to orient the user.

---

## Content Quality

This is where the app genuinely shines. The writing quality is consistently high across all tracks reviewed, and it holds up through the more demanding later material.

**What works well:**

**Clarity of explanation.** The blues scale lesson is a standout example of how to do this right. It doesn't just tell you what the b5 is — it immediately tells you what to *do* with it: use it as a passing tone, bend through it, avoid resting on it. That "avoid resting on it" warning is exactly the kind of practical guidance that separates a useful lesson from a theory dump.

**Diagram integration.** Diagrams appear at exactly the right moments — they follow the text explanation rather than replace it. The arpeggio check tab in the G chord lesson (plucking each string individually to test clarity) is genuinely pedagogically sound and something most beginners' resources skip.

**Theory accuracy.** The intervals table, chord construction, mode explanations, and song analysis examples all appear correct. The Dorian analysis of *Another Brick in the Wall* — identifying the major IV as the Dorian fingerprint — is precise and well-handled. The *Paranoid* analysis correctly identifies E Aeolian and explains why the absence of a conventional V chord produces its relentless quality. That's a level of depth a magazine reader would actually find useful.

**Sequencing.** The learning path from open chords → theory basics → barre chords → pentatonic scales → natural minor → major scale → 7th chords → modes → song analysis is genuinely well-designed. Prerequisites are clearly tracked. The cross-references between tracks (e.g., CAGED connecting back to pentatonic positions) demonstrate real curriculum thinking.

**The CAGED lesson** is a good example of the app's best instincts — it doesn't try to teach all five shapes at once, explicitly says not to, and explains *why* the system matters for lead guitar. That's the right call.

---

## Language and Wording

The tone is measured and precise without being academic. It reads like a knowledgeable teacher rather than a textbook. Sentence length is well-controlled. Almost nothing needs cutting.

**A few specific observations:**

- "Practise" (British spelling) appears consistently across lessons — fine if intentional, but worth flagging if the target audience is primarily American.
- Most lessons end cleanly but somewhat abruptly. The final paragraph often summarises what was just covered rather than pointing the reader forward. "That is the goal: turning theory into perception" (from *Putting It Together*) is one of the stronger closers in the app — more lessons should aspire to that kind of landing.
- The 12-bar blues lesson's "Why This Matters" section is excellent. It explicitly connects the lesson to what comes next (the pentatonic track) without requiring the reader to guess. This contextual linking should appear in more lessons.
- The *Fretboard* lesson's "Why It Matters" closer is also good — brief, forward-looking. This pattern of ending with a "why this connects to everything else" paragraph is one the app should apply consistently.

**One concern:** The orientation track (Track 01) teaches how to *read the app's diagrams*, not how to hold a guitar or produce a clean note. That is a reasonable scope decision, but the welcome screen should explicitly state this. A player who has never held a guitar will be lost the moment they try to act on Track 02 — the app assumes some basic physical knowledge.

---

## Reference Tables

This is where the app falls short of its potential.

**What exists:**
- Tools screen: full-neck scale view with key/quality selector, position cycling ([ and ])
- Diatonic chord strip: one text line showing `I: Am  │  II: Bdim  │  III: C …`

**What the chord strip does:** It names the diatonic chords for the selected key. That's useful. But it's a single line of text at the bottom of a screen. It cannot be interacted with, no voicings are shown, and the chord names alone tell only part of the story. A guitarist looking up "what chords are in the key of D?" will get the answer — but cannot click on any of those chord names to see a diagram.

**What is missing that would be high-value:**

1. **Circle of fifths.** This is the single most requested reference item for guitarists learning theory. A static visual showing the 12 keys arranged in fifths, with major/relative minor pairs, would be an immediate addition. The knowledge is implicitly present in the app's data layer but completely unsurfaced for the user.

2. **Key signatures cheatsheet.** The `key_signatures.md` lesson covers this conceptually, but there is no quick-reference table a player can look up mid-session. A simple table: Key → Sharps/Flats → Notes in key, for all 12 major and 12 minor keys.

3. **Chord formula reference.** The extended_chords and seventh_chords data exists but is only accessible through lessons. A single-page reference showing formulas (maj7: 1–3–5–7, dom7: 1–3–5–b7, min7: 1–b3–5–b7, etc.) would be immediately useful as a lookup table during composition or learning.

4. **Tunings reference.** Six tunings exist in the data layer (standard, drop D, open G, open D, DADGAD, half-step down) and are completely hidden from the user. The Tools screen mentions "tuning reference" on the welcome screen but has no actual tuning display. This is an undelivered promise.

5. **Barre chord position finder.** Given the emphasis on barre chords and CAGED, a reference table showing "root note → fret number on low E → fret number on A" would be immediately practical. Many guitarists keep a version of this on a sticky note.

6. **Capo reference.** Basic: "capo at fret X, chord shape → actual chord sounding." This is one of the most common lookups for beginner-intermediate players and completely absent.

---

## Target Audience Assessment

**Best fit:** An intermediate player — someone who knows open chords and a few barre chords, wants to understand *why* their shapes work, and is comfortable in a terminal environment. The sweet spot is probably a developer or technically-minded musician who finds guitar apps aesthetically heavy and prefers keyboard-driven tools.

**Secondary fit:** Advanced beginners who have just moved past chord shapes and want structure for learning scales and theory.

**Not well-served:**
- *Absolute beginners* — the app starts at "here are your open chord shapes," not at "here is how to hold a pick." Some physical fundamentals context would help, even just a brief note in the welcome screen about prerequisites.
- *Advanced players* — the curriculum tops out at modes and basic song analysis. There is no jazz harmony, no secondary dominants, no modulation mechanics, no chord substitution. A working musician looking for deeper harmonic tools will hit the ceiling at Track 11.
- *Non-terminal users* — this is an inherent constraint of the format, not a criticism. The app knows what it is.

---

## Recommendations Summary

**High priority — reference gaps:**
1. Deliver on the welcome screen's promise of a "tuning reference" — surface the six tunings that already exist in the data
2. Add a circle of fifths reference view (even as a static text/ASCII representation)
3. Add key signatures quick-reference (one page: all 12 keys, their sharps/flats, and diatonic notes)
4. Add chord formula quick-reference (all chord types with their interval formulas in one view)

**Medium priority — content improvements:**
5. Make the diatonic chord strip in the Tools view interactive — selecting a chord should show a diagram
6. Add "What's Next" or bridging paragraphs to lessons that currently end without forward direction
7. Add a welcome screen note clarifying the physical prerequisites (assumes player can form basic shapes)
8. Add a capo reference table

**Low priority — scope expansion:**
9. Rhythm and strumming patterns are entirely absent — even a single beginner lesson would help Track 02-03 students
10. A barre chord position finder (root note → fret) would be a fast-access complement to the barre chords track

---

## Verdict

Guitar TUI delivers a genuinely well-written, accurately sequenced theory curriculum in a format that the target audience will appreciate. The lesson content quality is notably better than most free web resources — it is precise, practical, and consistently connects theory to the fingerboard. The song analysis track in particular is a standout: analysing *Paranoid* and *Another Brick in the Wall* using real harmonic analysis tools, not just chord names, is exactly the kind of applied theory that changes how players hear music.

The reference tooling is the gap. For a tool that bills itself as a theory reference, the lookups a guitarist reaches for mid-session — circle of fifths, key signatures, chord formulas, tunings — are either absent or buried. Filling these in would lift the app from "excellent lesson viewer" to a genuinely complete theory companion. The data infrastructure clearly exists; it just needs to be surfaced.

**Recommended for:** Intermediate guitarists with a keyboard-driven workflow who want structured theory study and a reference that does not require leaving the terminal.
