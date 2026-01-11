.PHONY: up build
up:
  docker compose --env-file .env.development up -d

build:
  docker compose --env-file .env.development up --build