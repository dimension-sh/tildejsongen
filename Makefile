.PHONY: tests
tests:
	python3 -m poetry run pytest 

.PHONY: lint
lint:
	python3 -m ruff check --output-format=github --select=E9,F63,F7,F82 --target-version=py39 .
	python3 -m ruff check --output-format=github --target-version=py39 .
