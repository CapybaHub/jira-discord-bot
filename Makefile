ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)


perms:
	sudo chown -hR ${USER}:${USER} .

build:
	docker-compose build

up:
	docker-compose up

reup:
	docker-compose up --build

enter:
	docker-compose exec $(ARG) bash

setup_precommit:
	pre-commit install

setup_install:
	bash scripts/setup-install.sh

setup_venv:
	bash scripts/setup-venv.sh

startapp:
	bash scripts/start-app.sh $(ARG)

run:
	bash scripts/docker-run.sh $(ARG)

migrations:
	bash scripts/docker-run.sh python manage.py makemigrations $(ARG)

migrate:
	bash scripts/docker-run.sh python manage.py migrate

shell:
	bash scripts/docker-run.sh python manage.py shell

show_urls:
	bash scripts/docker-run.sh python manage.py show_urls

test:
	bash scripts/docker-run.sh pytest -n 4

coverage:
	bash scripts/docker-run.sh pytest --cov=apps --cov=lib

coverage_html:
	bash scripts/docker-run.sh pytest --cov=apps --cov=lib --cov-report html

seed: migrate
	bash scripts/docker-run.sh python manage.py seed

enable_test_user: migrate
	bash scripts/docker-run.sh python manage.py enable_test_user

disable_test_user: migrate
	bash scripts/docker-run.sh python manage.py disable_test_user

superuser:
	bash scripts/docker-run.sh python manage.py createsuperuser --email admin@capyba.com

initial_setup: migrate superuser seed

collectstatic:
	bash scripts/docker-run.sh python manage.py collectstatic

generate_schema:
	mkdir -p tmp/docs
	bash scripts/docker-run.sh python manage.py generateschema --format openapi-json > tmp/docs/openapi.json
