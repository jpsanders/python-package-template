SRC := src
TESTS := tests
ROOT_EC_FILES := $(wildcard *.yaml *.yml *.md) .github
PACKAGE := python_template
DOCKER_IMAGE := python-template:latest

.PHONY: help
help:
	@echo "Available targets:"
	@egrep "^([a-zA-Z_-]+):.*" $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":"}; {printf "    \033[36m%s\n\033[0m", $$1}'
	@echo ""
	@echo "Hints:"
	@echo "    Use '-n' to do a dry run"
	@echo "    Use '-k' to ignore failed targets and keep going"

.PHONY: create-egg-base
create-egg-base:
	@echo
	mkdir -p build/egg_base

.PHONY: init
init: create-egg-base
	@echo
	pip install -e .

.PHONY: init-dev
init-dev: create-egg-base
	@echo
	pip install -e .[dev]

.PHONY: ec
ec:
	@echo
	@echo --- Editorconfig linting checks ---
	ec ${SRC} ${TESTS} ${ROOT_EC_FILES}

.PHONY: ruff-format
ruff-format:
	@echo
	@echo --- Ruff format auto-fix ---
	ruff format --config pyproject.toml ${SRC} ${TESTS}

.PHONY: ruff-format-check
ruff-format-check:
	@echo
	@echo --- Ruff format check ---
	ruff format --config pyproject.toml --check ${SRC} ${TESTS}

.PHONY: ruff-lint-check
ruff-lint-check:
	@echo
	@echo --- Ruff lint check ---
	ruff check --config pyproject.toml ${SRC} ${TESTS}

.PHONY: ruff-lint
ruff-lint:
	@echo
	@echo --- Ruff lint auto-fix ---
	ruff check --config pyproject.toml --fix ${SRC} ${TESTS}

.PHONY: mypy
mypy:
	@echo
	@echo --- Mypy type checks ---
	mypy ${SRC} ${TESTS}

.PHONY: pytest
pytest: create-egg-base
	@echo
	@echo --- Pytest ---
	pytest --cov ${SRC}/${PACKAGE} --cov-report html:build/coverage --cov-report term ${TESTS}

.PHONY: bandit
bandit:
	@echo
	@echo --- Bandit security checks ---
	bandit -c pyproject.toml -f custom -r ${SRC} ${TESTS}

.PHONY: build
build: clean create-egg-base
	@echo
	@echo --- Build package wheel ---
	python -m build -o build/dist

.PHONY: build-docker
build-docker:
	@echo
	@echo --- Docker build image ---
	docker build -t ${DOCKER_IMAGE} --no-cache .

.PHONY: clean
clean:
	@echo
	rm -rf build/
	find ${SRC} ${TESTS} | grep -E "(\.egg-info|__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

# Run all checking tools
.PHONY: checks
checks: ec ruff-lint-check ruff-format-check mypy bandit pytest

# Run all auto-fix tools
.PHONY: format
format: ruff-lint ruff-format
