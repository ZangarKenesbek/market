.PHONY: build up down migrate createsuperuser

build:
	docker-compose --env-file .env.dev build

up:
	docker-compose --env-file .env.dev up -d

down:
	docker-compose --env-file .env.dev down

migrate:
	docker-compose --env-file .env.dev exec web python manage.py migrate

createsuperuser:
	docker-compose --env-file .env.dev exec web python manage.py createsuperuser
