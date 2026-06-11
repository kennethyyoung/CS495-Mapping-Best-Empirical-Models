# ──────────────────────────────────────────────
# Cross-platform Makefile (macOS / Windows+Git Bash)
# Python 3.13 · Poetry · venv
# ──────────────────────────────────────────────

PYTHON_VERSION := 3.13
VENV_DIR       := .venv

# OS detection
ifeq ($(OS),Windows_NT)
    PYTHON  := python
    VENV_BIN := $(VENV_DIR)/Scripts
    RM_RF   := rmdir /s /q
    SEP     := \\
else
    PYTHON  := python3
    VENV_BIN := $(VENV_DIR)/bin
    RM_RF   := rm -rf
    SEP     := /
endif

POETRY := $(VENV_BIN)$(SEP)poetry

.DEFAULT_GOAL := help

# ── Targets ──────────────────────────────────

.PHONY: help venv install update lock clean reset lint format test check stats validate figures

help: ## Show this help
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'
	@echo ""

venv: ## Create Python $(PYTHON_VERSION) virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_BIN)$(SEP)python -m pip install --upgrade pip
	$(VENV_BIN)$(SEP)pip install poetry
	@echo "Virtual environment created at $(VENV_DIR)"

install: venv ## Install project dependencies via Poetry
	$(POETRY) install
	@echo "Dependencies installed."

update: ## Update dependencies to latest compatible versions
	$(POETRY) update

lock: ## Regenerate poetry.lock without installing
	$(POETRY) lock

clean: ## Remove venv, caches, and build artifacts
	$(RM_RF) $(VENV_DIR)
	$(RM_RF) .mypy_cache .pytest_cache .ruff_cache __pycache__
	$(RM_RF) dist
	@echo "Cleaned."

reset: clean install ## Clean everything then reinstall

lint: ## Run ruff linter
	$(POETRY) run ruff check .

format: ## Run ruff formatter
	$(POETRY) run ruff format .

test: ## Run tests with pytest
	$(POETRY) run pytest

check: lint test ## Run lint + tests

# ── Analysis workflows ───────────────────────

stats: ## Reproduce coding-reliability figures (Cohen's kappa, Gwet's AC1) from committed data
	$(POETRY) run python analysis/pass3-fe-taxonomy/stats.py

validate: ## Validate Pass-3 data integrity
	$(POETRY) run python analysis/pass3-fe-taxonomy/validate_pass3.py

figures: ## Regenerate report figures, then fold them into outputs/report/figures/
	$(POETRY) run python analysis/figures/report/make_fig3_4_winners.py
	$(POETRY) run python analysis/figures/report/make_fig5_fe_prevalence.py
	$(POETRY) run python analysis/figures/report/make_fig6_paired.py
	$(POETRY) run jupyter nbconvert --to notebook --execute --inplace notebooks/02_reanalysis.ipynb
	$(POETRY) run python scripts/sync_report_figures.py
