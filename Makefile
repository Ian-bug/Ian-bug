.PHONY: help install install-dev test lint format type-check clean run update-readme pre-commit-install

help:
	@echo "Ian-bug Profile Updater - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install           - Install runtime dependencies"
	@echo "  make install-dev       - Install development dependencies"
	@echo "  make test              - Run tests"
	@echo "  make test-cov          - Run tests with coverage report"
	@echo "  make lint              - Run flake8 linting"
	@echo "  make format            - Format code with black"
	@echo "  make type-check        - Run mypy type checking"
	@echo "  make clean             - Clean up temporary files"
	@echo "  make run               - Run the update_readme.py script"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make all               - Run format, lint, type-check, and test"

install:
	pip install -r .github/scripts/requirements.txt

install-dev:
	pip install -r .github/scripts/requirements-dev.txt
	pip install pre-commit

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=.github/scripts/update_readme --cov-report=html --cov-report=term

lint:
	flake8 .github/scripts/update_readme.py

format:
	black .github/scripts/update_readme.py

type-check:
	mypy .github/scripts/update_readme.py --ignore-missing-imports

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache

run:
	python .github/scripts/update_readme.py

pre-commit-install:
	pre-commit install

all: format lint type-check test
	@echo "All checks passed!"
