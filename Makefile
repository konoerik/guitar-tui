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
	@echo "  Package (future)"
	@echo "    build        Build distribution packages"

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

# ── Package (future) ──────────────────────────────────────────────────────────

.PHONY: build
build:
	$(UV) build
