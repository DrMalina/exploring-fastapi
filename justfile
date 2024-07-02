default:
    just --list

dev:
    poetry run fastapi dev src/main.py

prod:
   poetry run fastapi run src/main.py

mm *args:
  poetry run alembic revision --autogenerate -m "{{args}}"

migrate:
  poetry run alembic upgrade head

downgrade *args:
  poetry run alembic downgrade {{args}}

lint:
    poetry run ruff src --fix

lint-c:
    poetry run ruff check src

fmt:
    poetry run ruff format src

test-i *args:
    poetry run pytest tests/integration {{args}}

# docker
up:
  docker-compose up -d

down:
  docker-compose down

kill *args:
  docker-compose kill {{args}}

build:
  docker-compose build

ps:
  docker-compose ps