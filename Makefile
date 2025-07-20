.PHONY: help bump-patch bump-minor bump-major test lint format type-check clean install dev-install docker-build docker-run

help:
	@echo "Available targets:"
	@echo "  bump-patch    - Bump patch version (x.x.X)"
	@echo "  bump-minor    - Bump minor version (x.X.x)"
	@echo "  bump-major    - Bump major version (X.x.x)"
	@echo "  test          - Run all tests"
	@echo "  lint          - Run linting checks"
	@echo "  format        - Format code with black"
	@echo "  type-check    - Run type checking with mypy"
	@echo "  clean         - Clean build artifacts"
	@echo "  install       - Install production dependencies"
	@echo "  dev-install   - Install development dependencies"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run Docker container"

bump-patch:
	./tools/bumpr patch

bump-minor:
	./tools/bumpr minor

bump-major:
	./tools/bumpr major

test:
	@echo "Running tests..."
	python -m pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	@echo "Running linting..."
	flake8 src/ tests/
	pylint src/
	mypy src/

format:
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/

type-check:
	@echo "Running type checking..."
	mypy src/ --strict

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov/

install:
	@echo "Installing production dependencies..."
	pip install -e .

dev-install:
	@echo "Installing development dependencies..."
	pip install -e ".[dev]"

docker-build:
	@echo "Building Docker image..."
	docker build -t plc-sniffer:latest .

docker-run:
	@echo "Running Docker container..."
	docker compose up