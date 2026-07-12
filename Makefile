.DEFAULT_GOAL := help

UV := uv

# ── Help ──────────────────────────────────────────────────────────────────────

.PHONY: help
help:
	@echo "Guitar TUI — available targets"
	@echo ""
	@echo "  Setup"
	@echo "    setup        Install all dependencies (runs uv sync)"
	@echo ""
	@echo "  Run"
	@echo "    run          Launch the application"
	@echo "    dev          Launch with Textual devtools (live reload + inspector)"
	@echo ""
	@echo "  Test & verify"
	@echo "    test         Run the test suite"
	@echo "    check        Verify the package is importable"
	@echo ""
	@echo "  Clean"
	@echo "    clean        Remove venv, caches, and build artifacts"
	@echo "    clean-pyc    Remove compiled Python files only"
	@echo ""
	@echo "  Release"
	@echo "    version-check  Verify pyproject.toml and welcome.py versions agree"
	@echo "    build          Clean dist/ and build distribution packages"
	@echo "    publish        Upload dist/ to PyPI (token from .env)"
	@echo "    release        version-check + test + build + publish, then tag hint"

# ── Setup ─────────────────────────────────────────────────────────────────────

.PHONY: setup
setup:
	$(UV) sync

# ── Run ───────────────────────────────────────────────────────────────────────

.PHONY: run
run:
	$(UV) run guitar-tui

.PHONY: dev
dev:
	$(UV) run textual run --dev guitar_tui/app.py

# ── Test & verify ─────────────────────────────────────────────────────────────

.PHONY: test
test:
	$(UV) run pytest

.PHONY: check
check:
	$(UV) run python -c "import guitar_tui; print('OK:', guitar_tui.__version__)"

# ── Clean ─────────────────────────────────────────────────────────────────────

.PHONY: clean
clean: clean-pyc
	rm -rf .venv .pytest_cache dist

.PHONY: clean-pyc
clean-pyc:
	find . -path './.venv' -prune -o -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -path './.venv' -prune -o -type f -name '*.pyc'     -delete 2>/dev/null || true

# ── Release ───────────────────────────────────────────────────────────────────
# Flow: bump version in pyproject.toml AND welcome.py _INFO_TEXT, commit,
# then `make release`, then tag and push as the final output suggests.

VERSION := $(shell grep -m1 '^version' pyproject.toml | cut -d'"' -f2)

.PHONY: version-check
version-check:
	@grep -q 'v$(VERSION)' guitar_tui/ui/screens/welcome.py || \
		{ echo "ERROR: welcome.py _INFO_TEXT does not say v$(VERSION) — bump both version strings"; exit 1; }
	@echo "version OK: $(VERSION)"

.PHONY: build
build:
	rm -rf dist
	$(UV) build

.PHONY: publish
publish: version-check
	@test -f .env || { echo "ERROR: .env with UV_PUBLISH token not found (see .env.example)"; exit 1; }
	set -a; . ./.env; set +a; $(UV) publish

.PHONY: release
release: version-check test build publish
	@echo ""
	@echo "Released $(VERSION). Finish with:"
	@echo "  git tag v$(VERSION) && git push origin main --tags"
