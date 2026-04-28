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

.PHONY: help venv install update lock clean reset run lint format test check

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

run: ## Run the main application (edit as needed)
	$(VENV_BIN)$(SEP)python -m src.main

lint: ## Run ruff linter
	$(POETRY) run ruff check .

format: ## Run ruff formatter
	$(POETRY) run ruff format .

test: ## Run tests with pytest
	$(POETRY) run pytest

check: lint test ## Run lint + tests
