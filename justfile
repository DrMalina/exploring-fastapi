default:
    just --list

dev:
    poetry run fastapi dev src/main.py

prod:
   poetry run fastapi run src/main.py

lint:
    poetry run ruff src --fix

lint-check:
    poetry run ruff check src

format:
    poetry run ruff format src
