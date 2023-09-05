lint:
	poetry run mypy ./upy
	poetry run flake8 upy
	poetry run pylint ./upy

format:
	poetry run isort ./upy
	poetry run black ./upy
