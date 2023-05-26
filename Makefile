.PHONY: package release

all: package

# Packaging
package:
	rm -f dist/*
	python3 setup.py sdist bdist_wheel

install: package
	python3 -m pip install --no-deps --force dist/*.whl

release: package
	twine upload --repository pypi dist/*

release-test: package
	twine upload --repository testpypi dist/*

clean:
	rm -rf dist build



# Testing
reviewCode:
	sourcery review pyspacemouse --in-place

install-dev:
	python3 -m pip install --force --editable .

run-demo:
	python3 ./examples/basicExample.py



fixRelativeLinkDocs:
	sed  's/\.\/docs/\./g'  README.md > docs/README.md
	sed  's/\.\/docs/\./g'  CONTRIBUTING.md > docs/CONTRIBUTING.md

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