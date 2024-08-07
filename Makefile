APP_LIST ?= main pages users
.PHONY: collectstatic run test ci install install-dev migrations staticfiles

help:
	@echo "Available commands"
	@echo "ci - lints, migrations, tests, coverage"
	@echo "install - installs production requirements"
	@echo "isort - sorts all imports of the project"
	@echo "runserver - runs the development server"
	@echo "setup-test-data - erases the db and loads mock data"
	@echo "shellplus - runs the development shell"
	@echo "lint - check style with black, flake8, sort python with isort, and indent html"
	@echo "format - enforce a consistent code style across the codebase and sort python files with isort"

collectstatic:
	python manage.py collectstatic --noinput

clean:
	rm -rf __pycache__ .pytest_cache

check:
	python manage.py check

check-deploy:
	python manage.py check --deploy

css:
	sass static/assets/scss/soft-design-system.scss -s compressed static/assets/css/styles.min.css

install:
	poetry install

update:
	poetry update
	
setup_test_data:
	python manage.py setup_test_data
	
shellplus:
	python manage.py shell_plus --print-sql

shell:
	python manage.py shell

showmigrations:
	python manage.py showmigrations

makemigrations:
	python manage.py makemigrations

makemessages:
	django-admin makemessages --all

compilemessages:
	django-admin compilemessages 
	
migrate:
	python manage.py migrate

migrations-check:
	python manage.py makemigrations --check --dry-run

runserver:
	python manage.py runserver

build: install makemigrations migrate runserver

format:
	poetry run black .
	poetry run isort . --profile black
	git ls-files '*.html' | xargs djlint --reformat

lint:
	poetry run black --check --diff .
	poetry run isort . --check-only --profile black
	poetry run ruff check --fix .
	git ls-files '*.html' | xargs djlint --check

test: check migrations-check
	coverage run --source='.' manage.py test
	coverage html

security:
	poetry run bandit -r .
	poetry run safety check

ci: format lint security test

superuser:
	python manage.py createsuperuser

status:
	@echo "Nginx"
	@sudo systemctl status nginx

	@echo "Gunicorn Socket"
	@sudo systemctl status indie-gunicorn.socket

	@echo "Gunicorn Service"
	@sudo systemctl status indie-gunicorn.service


reload:
	@echo "reloading daemon..."
	@sudo systemctl daemon-reload

	@echo "🔌 restarting gunicorn socket..."
	@sudo systemctl restart indie-gunicorn.socket

	@echo "🦄 restarting gunicorn service..."
	@sudo systemctl restart indie-gunicorn.service
	
	@echo "⚙️ reloading nginx..."
	@sudo nginx -s reload
	
	@echo "All done! 💅💫💖"

logs:
	@sudo journalctl -fu indie-gunicorn.service
	

