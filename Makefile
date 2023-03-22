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
	sourcery review mkdoxy --in-place

install-dev:
	python3 -m pip install --force --editable .

run-demo:
	python3 ./examples/basicExample.py



# Documentation
docs-serve:
	mkdocs serve

docs-build: # results in site directory
	mkdocs build



