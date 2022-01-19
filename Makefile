build:
	rm -rf dist/*;  python3 -m build

distribute: build
	python3 -m twine upload --repository pypi dist/*

test:
	pytest -s tests/