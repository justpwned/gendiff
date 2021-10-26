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

test-coverage:
	poetry run pytest --cov=hexlet_python_package --cov-report xml

.PHONY: gendiff