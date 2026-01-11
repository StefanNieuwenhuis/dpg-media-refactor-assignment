# Makefile for DPG Media Refactor Test - Gilded Rose Kata

# --------------------------------------------------
# Configuration
# --------------------------------------------------

# Python interpreter
PYTHON := python
PIP := $(PYTHON) -m pip

# Project directories
SRC_DIR := .
TEST_DIR := tests

# Virtual environment
VENV := .venv
VENV_BIN := .venv/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_PYTHON) -m pip
VENV_PYTEST := $(VENV_BIN)/pytest

# Detect OS for platform-specific commands
ifeq ($(OS),Windows_NT)
	VENV_BIN := $(VENV)/Scripts
	VENV_PYTHON := $(VENV_BIN)/python.exe
	VENV_PYTEST := $(VENV_BIN)/pytest.exe
	RM := del /Q
	RM_RF := rmdir /S /Q
else
	RM := rm -f
	RM_RF := rm -rf
endif

# Colors for output (Unix/Linux/Mac only)
ifndef OS
	RED := \033[0;31m
	GREEN := \033[0;32m
	YELLOW := \033[0;33m
	BLUE := \033[0;34m
	NC := \033[0m # No Color
else
	RED :=
	GREEN :=
	YELLOW :=
	BLUE :=
	NC :=
endif

# --------------------------------------------------
# Default target
# --------------------------------------------------

.DEFAULT_GOAL := help

# --------------------------------------------------
# Phony targets
# --------------------------------------------------

.PHONY: help setup install test test-verbose test-coverage test-html \
		test-watch clean clean-pyc clean-test clean-venv clean-all \
		init verify

# --------------------------------------------------
# Help target
# --------------------------------------------------

help:
	@echo "$(BLUE)DPG Media Refactor Test - Gilded Rose Kata"
	@echo "$(BLUE)Makefile commands$(NC)"
	@echo "$(BLUE)--------------------------------------------------$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; /^setup|^install|^init/ {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Testing Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; /^test/ {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
		@echo "$(GREEN)Running Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; /^demo|^run|^interactive/ {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Cleanup Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; /^clean/ {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; /^verify|^coverage|^list/ {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'


# --------------------------------------------------
# Setup targets
# --------------------------------------------------

init: ## Complete first-time setup (virtual environment + install dependencies + verify)
	@echo "$(BLUE)Initializing Gilded Rose Kata project...$(NC)"
	@$(MAKE) setup
	@$(MAKE) install
	@$(MAKE) verify
	@echo "$(GREEN)✓ Setup complete! Run 'make test' to verify.$(NC)"

setup: ## Create virtual environment
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	@$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✓ Virtual environment created at $(VENV)$(NC)"

install: $(VENV) ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@$(VENV_PIP) install --upgrade pip
	@$(VENV_PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

# --------------------------------------------------
# Testing targets
# --------------------------------------------------
test: $(VENV) ## Run all tests
	@echo "$(BLUE)Running all tests...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ -v

test-verbose: $(VENV) ## Run tests verbose
	@echo "$(BLUE)Running tests (verbose)...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ -vv

test-coverage: $(VENV) ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ --cov=$(SRC_DIR) --cov-report=term-missing

test-html: $(VENV) ## Run tests and generate HTML coverage report
	@echo "$(BLUE)Generating HTML coverage report...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ --cov=$(SRC_DIR) --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

test-watch: $(VENV) ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	@$(VENV_BIN)/ptw $(TEST_DIR)/ -v

test-fast: $(VENV) ## Run tests and stop at first failure
	@echo "$(BLUE)Running tests (fail fast)...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ -v -x

test-last-failed: $(VENV) ## Re-run only last failed tests
	@echo "$(BLUE)Re-running last failed tests...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ -v --lf

test-specific: $(VENV) ## Run specific test (usage: make test-specific TEST=test_name)
	@echo "$(BLUE)Running specific test: $(TEST)...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ -v -k "$(TEST)"

# --------------------------------------------------
# Cleaning targets
# --------------------------------------------------
clean: clean-pyc clean-test ## Remove all generated files
	@echo "$(GREEN)✓ Cleaned all generated files$(NC)"

clean-pyc: ## Remove Python cache files
	@echo "$(BLUE)Removing Python cache files...$(NC)"
	@find . -type d -name __pycache__ -exec $(RM_RF) {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -exec $(RM) {} + 2>/dev/null || true
	@find . -type f -name "*.pyo" -exec $(RM) {} + 2>/dev/null || true
	@find . -type f -name "*.pyd" -exec $(RM) {} + 2>/dev/null || true

clean-test: ## Remove test and coverage artifacts
	@echo "$(BLUE)Removing test artifacts...$(NC)"
	@$(RM_RF) .pytest_cache 2>/dev/null || true
	@$(RM_RF) htmlcov 2>/dev/null || true
	@$(RM) .coverage 2>/dev/null || true
	@$(RM_RF) .tox 2>/dev/null || true

clean-venv: ## Remove virtual environment
	@echo "$(BLUE)Removing virtual environment...$(NC)"
	@$(RM_RF) $(VENV)
	@echo "$(GREEN)✓ Virtual environment removed$(NC)"

clean-all: clean clean-venv ## Remove everything (including venv)
	@echo "$(GREEN)✓ Complete cleanup finished$(NC)"

# --------------------------------------------------
# Utility targets
# --------------------------------------------------
verify: ## Verify setup is correct
	@echo "$(BLUE)Verifying setup...$(NC)"
	@echo "  Checking Python version..."
	@$(VENV_PYTHON) --version
	@echo "  Checking pip..."
	@$(VENV_PIP) --version
	@echo "  Checking pytest..."
	@$(VENV_PYTEST) --version
	@echo "  Checking project structure..."
	@test -f $(SRC_DIR)/gilded_rose.py && echo "    ✓ $(SRC_DIR)/gilded_rose.py exists" || echo "    ✗ $(SRC_DIR)/gilded_rose.py missing"
	@test -f $(TEST_DIR)/test_gilded_rose.py && echo "    ✓ $(TEST_DIR)/test_gilded_rose.py exists" || echo "    ✗ $(TEST_DIR)/test_gilded_rose.py missing"
	@echo "$(GREEN)✓ Verification complete$(NC)"

coverage-report: test-html ## Alias for test-html (generate coverage report)

list-tests: $(VENV) ## List all available tests
	@echo "$(BLUE)Available tests:$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/ --collect-only -q