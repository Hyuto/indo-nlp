format:
	poetry run black .
	poetry run isort .

format-check:
	poetry run black . --check 
	poetry run isort . --check-only

typecheck:
	poetry run mypy -p indoNLP --no-incremental

test:
	poetry run pytest --cov=indoNLP/ -v
