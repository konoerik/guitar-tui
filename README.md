# Guitar TUI

A terminal application for guitar music theory. Structured lessons, interactive reference tools, and a licks library — entirely keyboard-driven, no browser required. Built on [Textual](https://github.com/Textualize/textual) and developed with [Claude Sonnet 4.6](https://anthropic.com).

![Guitar TUI demo](demo.gif)

## What's inside

- **78 lessons** across 11 tracks — open chords through modes and song analysis
- **Tools screen** — full-neck scale/key explorer, diatonic chord strip, reference tables (intervals, key signatures, barre positions, capo chart, tunings)
- **Practice screen** — technique exercises and a lick library with looper-ready phrases across 8 scale categories
- All content is plain Markdown with YAML frontmatter — readable without running the app

### Curriculum

| Phase | Tracks | Content |
|-------|--------|---------|
| 1 — Playing foundation | 1–3 | Notation · Open chords · First progressions |
| 2 — Vocabulary expansion | 4–9 | Theory · Barre chords · Pentatonic · Natural minor · Major scale · Seventh chords |
| 3 — Synthesis | 10–11 | Modes · Song analysis |

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Install

```bash
uv tool install git+https://github.com/konoerik/guitar-tui.git
guitar-tui
```

Or clone and run locally:

```bash
git clone https://github.com/konoerik/guitar-tui.git
cd guitar-tui
uv run guitar-tui
```

## Navigation

| Key | Action |
|-----|--------|
| `1` | Home |
| `2` | Lessons |
| `3` | Tools |
| `4` | Practice |
| `q` | Quit |
| `[` `]` | Previous / next scale position (Tools) |
| `,` `.` | Previous / next diatonic chord (Tools) |
| `Esc` | Back / deselect |

## Terminal requirements

Recommended size: **110 × 36 or larger**. Use a terminal emulator with a good monospace font (Ghostty, iTerm2, WezTerm, Alacritty all work well). Increase font size until the layout feels comfortable — there's no zoom button.

## Architecture

Four-layer model:

```
Data Layer     guitar_tui/data/        YAML chord/scale data
Engine Layer   guitar_tui/engine/      Diagram renderers (music-agnostic)
Content Layer  guitar_tui/loaders/     Lesson and lick parsers
TUI Layer      guitar_tui/ui/          Screens, widgets, stylesheet
```

The engine renders `DiagramSpec` objects and has no knowledge of chord names or scale theory. Music knowledge lives in the data layer and lesson content. Lessons are plain Markdown with YAML frontmatter and fenced `diagram` blocks — see `schemas/` for the full spec.

## Adding content

Lessons live in `guitar_tui/content/lessons/`, exercises in `guitar_tui/content/exercises/`, and licks in `guitar_tui/content/licks/`. Each is a Markdown file with YAML frontmatter — see `schemas/lesson_format.md` and `schemas/diagram_spec.md`.

## A personal note

I am building this app as a personal knowledge base for guitar music theory. Like so many folks out there, I've been playing guitar for two decades, but only in recent years I have tried to understand the theory behind all my beloved songs. It takes time and it takes effort. There are fantastic resources online, there are great videos on YouTube and there are great books on the topic - I do have several of them. With the advent of LLMs however, I can go one step further. Take those concepts, have them explained in various ways and have them presented in a way that works for me. So that's what I did.

That being said, I am not a music theory expert, so I am limited in my capacity to validate all the content for correctness. Nevertheless, I have tried my best (by using an instructor persona and a separate reviewer persona for the critique) and by examining the things I do understand. I will continue this effort as I ask Claude to generate more content and as I go through the content myself and become familiar with new topics by cross examining with other resources.

## License

MIT © 2026 Erikton Konomi
