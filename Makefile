all: release

release:
	echo "Package build + upload to pypi.org"
	python3 setup.py sdist bdist_wheel

	twine check dist/*

	twine upload --repository pypi dist/*

delete:
	rm -rf dist/*
	rm -rf build/*
	rm -rf *.egg-info