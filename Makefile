.PHONY: help install clean test lint format run dev-setup check-deps

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using Poetry
	poetry install

update: ## Update dependencies
	poetry update

clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

run: ## Run the main processing script
	poetry run python src/main.py

process-pdfs: ## Process all PDFs in the input directory
	poetry run python src/main.py --input-dir data/input --output-dir data/output

install-dev: ## Install package in development mode using pip
	pip install -e .

install-dev-extras: ## Install package with dev dependencies using pip
	pip install -e ".[dev]"

build: ## Build distribution packages
	python setup.py sdist bdist_wheel

check-setup: ## Check setup.py configuration
	python setup.py check

dist-clean: ## Clean distribution files
	rm -rf build/ dist/ *.egg-info/
