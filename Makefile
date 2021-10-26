install:
	poetry install

build:
	poetry build

package-install: build
	python3 -m pip install --user dist/*.whl --force-reinstall

gendiff:
	poetry run gendiff

.PHONY: gendiff