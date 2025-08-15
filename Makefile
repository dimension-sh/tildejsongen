.PHONY: tests
tests:
	uv run pytest

.PHONY: lint
lint:
	uv run ruff check --output-format=github --select=E9,F63,F7,F82 --target-version=py39 .
	uv run ruff check --output-format=github --target-version=py39 .
