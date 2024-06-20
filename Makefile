# Makefile

.PHONY: help format lint test clean install deps venv create_venv activate_venv deactivate_venv

help:
	@echo "Help command..."
	@echo "Available targets:"
	@echo "  format          - Format the codebase using ruff and isort"
	@echo "  lint            - Run static analysis with mypy and ruff"
	@echo "  test            - Run all tests with pytest"
	@echo "  clean           - Clean up build artifacts"
	@echo "  install         - Install the package"
	@echo "  deps            - Install dependencies"
	@echo ""
	@echo "@Rights owned by Md. Almas Ali 2024"

format:
	@ruff format .
	@isort .

lint:
	@mypy --strict .
	@ruff check .

test:
	@pytest

clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf .ruff_cache
	@rm -rf .pytest_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf .venv

install:
	@pip install .

deps:
	@pip install -r requirements.txt

