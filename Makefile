.PHONY: up build down down-v superuser
up:
	docker compose --env-file .env.development up -d

build:
	docker compose --env-file .env.development up --build

down:
	docker compose --env-file .env.development down

down-v:
	docker compose --env-file .env.development down -v

superuser:
	docker compose --env-file .env.development exec backend python manage.py createsuperuser