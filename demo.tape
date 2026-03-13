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

# Tree is focused on mount. Cursor starts on "Introduction".
# Navigate down to 06. Pentatonic Scale (7 steps past Introduction)
Tab
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
Sleep 200ms
Down
Sleep 300ms
Enter          # expand 06. Pentatonic Scale
Sleep 400ms
Down           # → Minor Pentatonic Scale — Position 1
Enter          # open lesson
Tab
Sleep 2s

# Scroll through the lesson content
Tab
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

# Go to Exercises and Licks Tabs
Shift + Tab
Right
Sleep 2s
Down
Down
Right
Sleep 1s
Down
Down

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

# ── Exercises / Licks ───────────────────────────────────────────────────────────
Type "4"
Tab
Enter
Sleep 200ms
Down
Sleep 200ms
Down
Sleep 200ms
Enter
Sleep 200ms
Down
Sleep 200ms
Enter
Sleep 200ms
Down
Sleep 200ms
Enter
Sleep 200ms
Tab
Sleep 200ms
Down
Sleep 200ms
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
