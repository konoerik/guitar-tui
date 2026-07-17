# Guitar TUI — demo recording
# Run: vhs demo.tape
# Requires: vhs (brew install vhs)

Output demo.gif

Set Shell "fish"
Set FontSize 15
Set Width 1400
Set Height 950
Set Theme "Catppuccin Mocha"
Set PlaybackSpeed 1
Set TypingSpeed 80ms

# ── Setup (hidden): fresh config dir so the demo starts first-run ─────────────
Hide
Type "set -x GUITAR_TUI_CONFIG_DIR (mktemp -d); clear"
Enter
Sleep 500ms
Show

# ── Launch ────────────────────────────────────────────────────────────────────
Type "uv run guitar-tui"
Sleep 500ms
Enter
Sleep 3s

# ── Welcome screen ────────────────────────────────────────────────────────────
Sleep 3s

# ── Lessons screen ────────────────────────────────────────────────────────────
Type "2"
Sleep 1s

# Content body is focused on mount; two Tabs reach the track tree.
Tab
Sleep 200ms
Tab
Sleep 200ms
# Cursor starts on "Introduction". Down 7 → 06. The Pentatonic Scale
# (separator, then tracks 01–06).
Down
Sleep 200ms
Down
Sleep 200ms
Down
Sleep 200ms
Down
Sleep 200ms
Down
Sleep 200ms
Down
Sleep 200ms
Down
Sleep 300ms
Enter          # expand 06. The Pentatonic Scale
Sleep 400ms
Down           # → Minor Pentatonic Scale — Position 1
Sleep 300ms
Enter          # open lesson (focus returns to the lesson body)
Sleep 2s

# Scroll through the lesson content
Down
Down
Down
Down
Down
Sleep 1s
Down
Down
Down
Down
Down
Sleep 2s

# Exercises and Licks tabs (Shift+Tab focuses the tab bar, Right switches)
Shift+Tab
Sleep 300ms
Right
Sleep 2s
Right
Sleep 1s
Tab            # focus the licks body
Down
Down
Sleep 2s

# ── Tools / Key View ──────────────────────────────────────────────────────────
Type "3"
Sleep 2s

# Cycle scale positions
Type "]"
Sleep 800ms
Type "]"
Sleep 800ms
Type "]"
Sleep 800ms
Type "["
Sleep 800ms

# Step through diatonic chord strip
Type "."
Sleep 600ms
Type "."
Sleep 600ms
Type "."
Sleep 600ms
Type ","
Sleep 600ms

Sleep 2s

# ── Practice: exercises and licks ─────────────────────────────────────────────
Type "4"
Sleep 1s
Tab
Sleep 200ms
Tab
Sleep 200ms
Down           # separator
Sleep 200ms
Down           # → Exercises
Sleep 300ms
Enter          # expand Exercises
Sleep 400ms
Down           # → Warm-ups
Sleep 300ms
Enter          # expand Warm-ups
Sleep 400ms
Down           # → first warm-up
Sleep 300ms
Enter          # load it
Sleep 2s
Down
Sleep 200ms
Down
Sleep 2s

# ── Back to welcome ───────────────────────────────────────────────────────────
Escape
Sleep 2s

# ── Quit ──────────────────────────────────────────────────────────────────────
Type "q"
Sleep 500ms
