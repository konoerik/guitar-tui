# Contributing to Guitar TUI

Thank you for your interest in contributing. This is a small, focused project — contributions are welcome, but please read this first so your effort isn't wasted.

## What kind of contributions are welcome

- **Bug reports** — something renders incorrectly, crashes, or behaves unexpectedly
- **Content corrections** — a chord voicing is wrong, a scale position has an error, lesson prose is inaccurate
- **Small fixes** — typos, broken links, off-by-one errors in diagrams
- **Feature proposals** — open an issue before writing code; the roadmap is deliberate and not everything fits

## What is out of scope

- Copyrighted note sequences or transcriptions
- Audio playback (deferred by design — see architecture notes)
- User-configurable content paths or plugin systems
- Python < 3.12 support

## Reporting a bug

Open a GitHub issue and include:

- OS and terminal emulator (e.g. macOS 14, iTerm2)
- Python version (`python --version`)
- How you installed the app (`uv tool install`, `pip install`, cloned repo)
- What you expected vs. what happened
- If a diagram rendered incorrectly, paste the diagram YAML from the lesson file

## Suggesting content changes

Content lives in `guitar_tui/content/` (lessons, exercises, licks) and `guitar_tui/data/` (YAML chord/scale data). The schema contract is in `schemas/`. If you spot an error in a chord voicing or scale pattern, open an issue with the correct value and a reference — a reputable source, a published book, or a clear theoretical derivation.

## Submitting a pull request

1. Fork the repository and create a branch from `main`
2. Install dependencies: `uv sync`
3. Make your changes
4. Run the test suite: `uv run pytest` — all tests must pass
5. Open a PR with a clear description of what changed and why

For anything beyond a small fix, open an issue first so we can discuss whether it fits before you invest the time.

## Development setup

```bash
git clone https://github.com/konoerik/guitar-tui
cd guitar-tui
uv sync
uv run guitar-tui          # run the app
uv run pytest              # run tests
uv run textual run --dev guitar_tui/app.py   # run with Textual devtools
```
