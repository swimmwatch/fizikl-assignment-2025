-include .env

ENV_CONF = -f docker-compose.yml

ifeq (${ENV},local)
	ENV_CONF = -f docker-compose.yml -f docker-compose.local.yml
endif

SRC_DIR=src
BACKUPS_DIR=.backups

env ?= "local"
path ?= "none"

############
## Docker ##
############

pull:
	docker compose $(ENV_CONF) pull

push:
	docker compose $(ENV_CONF) push

build:
	docker compose $(ENV_CONF) build

up:
	docker compose $(ENV_CONF) up --detach --remove-orphans

restart:
	docker compose $(ENV_CONF) restart

down:
	docker compose $(ENV_CONF) down

createsuperuser:
	docker compose $(ENV_CONF) run --rm app python manage.py createsuperuser

migrate:
	docker compose $(ENV_CONF) run --rm app python manage.py migrate

collectstatic:
	docker compose $(ENV_CONF) exec app python manage.py collectstatic --noinput

tests:
	docker compose $(ENV_CONF) run --rm app make test

run:
	docker compose $(ENV_CONF) up --detach
