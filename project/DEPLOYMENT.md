# Deployment Goals

## Priority 1 — GitHub public release

The repo is committed and structurally ready. Remaining work before making it public:

### Must-have
- [ ] Verify package data includes (content/, data/, ui/app.tcss) survive a `uv build` + install cycle — hatchling should include them by default but needs a test
- [x] Replace placeholder GitHub URL in README (`your-username/guitar-tui`) with the real repo URL once created
- [x] Add a `LICENSE` file (README references MIT but no LICENSE file exists)

### Nice-to-have before public launch
- [ ] Terminal size recommendation note in welcome screen + startup warning (see BACKLOG.md — terminal size section)
- [ ] A screenshot or screen recording in README — the ASCII art chord grid in the README is a placeholder; a real screenshot would dramatically improve first impressions
- [ ] `uv.lock` decision: currently in `.gitignore`; removing it would give reproducible installs. Acceptable either way for a public repo.

---

## Priority 2 — PyPI publication

Blocked on Priority 1 being stable. Steps when ready:

1. **Test the build**
   ```bash
   uv build
   uv pip install dist/guitar_tui-*.whl --target /tmp/test-install
   ```
   Confirm content/, data/, ui/app.tcss are present in the installed package.

2. **Version policy** — currently `0.1.0`. Suggested versioning:
   - `0.1.x` — bug fixes and content additions (current state)
   - `0.2.0` — next significant feature milestone (M7: Theory Web, or lesson→lick cross-refs)
   - `1.0.0` — when the curriculum is considered complete and the UI is stable

3. **PyPI publish**
   ```bash
   uv publish
   ```
   Requires a PyPI account and API token configured in `~/.config/uv/credentials`.

4. **Update README install instructions** from:
   ```bash
   uv tool install git+https://github.com/...
   ```
   to:
   ```bash
   uv tool install guitar-tui
   ```

---

## Deployment constraints (standing rules)

These apply to all future implementation work:

- **No binary bundling.** PyInstaller/Nuitka are not pursued — disproportionate effort, Textual incompatibility, wrong audience.
- **`uv tool install` is the primary install path.** All user-facing instructions assume uv or pipx. pip works but is not the first recommendation.
- **Data files live inside the package.** Content (Markdown lessons, lick files, exercises), YAML data, and the TCSS stylesheet must remain under `guitar_tui/` so hatchling includes them in the wheel automatically. Do not move content outside the package directory.
- **Python 3.12+ only.** No backwards-compatibility work for older versions.
- **Keep dependencies minimal.** Current four deps (textual, pyyaml, python-frontmatter, pydantic) cover everything. New dependencies require justification.
