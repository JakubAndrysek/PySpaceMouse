.PHONY: package release test lint format build clean version publish

all: package

# Packaging (using Hatch)
build:
	hatch build

package: build

build-clean:
	hatch clean
	hatch build

# Publishing (using Hatch)
publish: build
	hatch publish

publish-test: build
	hatch publish --repo test

# Version management (using Hatch)
version:
	hatch version

version-patch:
	hatch version patch

version-minor:
	hatch version minor

version-major:
	hatch version major

# Clean
clean:
	hatch clean
	rm -rf dist build pyspacemouse.egg-info .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f .coverage coverage.xml

# Development
install-dev:
	hatch run pip install --editable ".[dev]"

# Code Quality
lint:
	hatch run ruff check .

format:
	hatch run ruff format .

format-check:
	hatch run ruff format --check .

# Testing
test: # FIXME!
	hatch run test:pytest

test-cov: # FIXME!
	hatch run test:pytest --cov-report=html

run-demo:
	hatch run python ./examples/01_basic.py

# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files


# Documentation, using mkdocs and mkdoxy
install-doxygen:
	@command -v doxygen >/dev/null || (echo "Please install doxygen (apt/dnf/brew)" && exit 1)

fixRelativeLinkDocs:
	sed  's/\.\/docs/\./g'  README.md > docs/README.md
	sed  's/\.\/docs/\./g'  CONTRIBUTING.md > docs/CONTRIBUTING.md
	sed  's/\.\/docs/\./g'  troubleshooting.md > docs/troubleshooting.md

# Docs
docs-build: install-doxygen fixRelativeLinkDocs
	@echo "Building docs..."
	hatch run dev:mkdocs build

docs-serve: install-doxygen fixRelativeLinkDocs
	@echo "Serving docs..."
	hatch run dev:mkdocs serve

docs-deploy: install-doxygen fixRelativeLinkDocs
	@echo "Deploying docs..."
	hatch run dev:mkdocs gh-deploy
