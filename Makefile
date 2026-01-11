.PHONY: up build down down-v
up:
	docker compose --env-file .env.development up -d

build:
	docker compose --env-file .env.development up --build

down:
	docker compose --env-file .env.development down

down-v:
	docker compose --env-file .env.development down -v