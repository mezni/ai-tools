.PHONY: test lint format

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .
