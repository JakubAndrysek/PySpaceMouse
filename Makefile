.PHONY: package release test lint format build clean version publish

all: package

# Packaging (using Hatch)
build:
	hatch build

package: build

build-clean:
	hatch clean
	hatch build

install: build
	python3 -m pip install --no-deps --force dist/*.whl

# Publishing (using Hatch)
publish: build
	hatch publish

publish-test: build
	hatch publish --repo test

# Legacy twine commands (deprecated, use publish/publish-test)
release: build
	twine upload --repository pypi dist/*

release-test: build
	twine upload --repository testpypi dist/*

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
	hatch env create
	python3 -m pip install --editable ".[dev]"

# Code Quality
lint:
	hatch run ruff check .

format:
	hatch run ruff format .

format-check:
	hatch run ruff format --check .

# Testing
test:
	hatch run test:pytest

test-cov:
	hatch run test:pytest --cov-report=html

run-demo:
	python3 ./examples/basicExample.py

# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files



fixRelativeLinkDocs:
	sed  's/\.\/docs/\./g'  README.md > docs/README.md
	sed  's/\.\/docs/\./g'  CONTRIBUTING.md > docs/CONTRIBUTING.md
	sed  's/\.\/docs/\./g'  troubleshooting.md > docs/troubleshooting.md

# Docs
docs-build: fixRelativeLinkDocs
	@echo "Building docs..."
	mkdocs build

docs-serve: fixRelativeLinkDocs
	@echo "Serving docs..."
	mkdocs serve

docs-deploy: fixRelativeLinkDocs
	@echo "Deploying docs..."
	mkdocs gh-deploy --force