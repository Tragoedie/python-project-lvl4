MANAGE := poetry run python manage.py

install:
	poetry install

test:
	$(MANAGE) test

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

check: lint test

lint:
	poetry run flake8 task_manager

db-clean:
	@rm db.sqlite3 || true

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

shell:
	$(MANAGE) shell

run:
	$(MANAGE) runserver
