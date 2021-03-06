install:
	poetry install

build: install
	poetry build

package-install: build
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest -vv

gendiff:
	poetry run gendiff

latest-gendiff: package-install
	poetry run gendiff

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

.PHONY: gendiff
