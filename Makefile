format:
	poetry run isort .
	poetry run black .

format-check:
	poetry run isort . --check-only
	poetry run black . --check 

typecheck:
	poetry run mypy -p indoNLP --no-incremental

test:
	poetry run pytest --cov=indoNLP/ -v
