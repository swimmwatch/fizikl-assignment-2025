SHELL := /bin/bash

SRC_DIR=.

RUNNER=poetry run

#############
## Linters ##
#############

flake:
	$(RUNNER) flake8 --toml-config formatters-cfg.toml $(SRC_DIR)

black:
	$(RUNNER) black --config formatters-cfg.toml $(SRC_DIR)

black-lint:
	$(RUNNER) black --check --config formatters-cfg.toml $(SRC_DIR)

isort:
	$(RUNNER) isort --settings-path formatters-cfg.toml $(SRC_DIR)

format: black isort

lint: flake black-lint

#############
## Django ##
#############

shell:
	$(RUNNER) python manage.py shell

makemigrations:
	$(RUNNER) python manage.py makemigrations

check-migrations:
	$(RUNNER) python manage.py makemigrations --check --dry-run

check-deploy:
	$(RUNNER) python manage.py check --deploy

###########
## Tests ##
###########

test:
	$(RUNNER) pytest --junitxml=backend-test-report.xml --cov --cov-report term --cov-report xml:coverage.xml -n 4 --reruns 10 $(SRC_DIR)

########################
## Python Environment ##
########################

install:
	poetry install --no-root

lock:
	poetry lock --no-update
