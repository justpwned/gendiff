install:
	poetry install

build:
	poetry build

package-install: build
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

gendiff:
	poetry run gendiff

.PHONY: gendiff