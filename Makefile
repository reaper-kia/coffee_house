.PHONY: up down down-v build restart logs ps shell db-shell test lint format tree migration migrate downgrade

migration:
	docker compose exec app alembic revision --autogenerate -m "$(name)"

migrate:
	docker compose exec app alembic upgrade head

downgrade:
	docker compose exec app alembic downgrade -1

up:
	docker compose up --build -d

down:
	docker compose down

down-v:
	docker compose down -v

build:
	docker compose build

restart:
	docker compose down
	docker compose up --build

logs:
	docker compose logs -f

ps:
	docker compose ps

shell:
	docker compose exec app bash

db-shell:
	docker compose exec db psql -U coffee_house -d coffee_house
test:
	docker compose exec app pytest

lint:
	docker compose exec app ruff check .

format:
	docker compose exec app ruff format .

tree:
	tree -I "__pycache__|.git|.venv|venv|.pytest_cache|.mypy_cache|.ruff_cache"
