default:
    just --list

dev:
    poetry run fastapi dev src/main.py

prod:
   poetry run fastapi run src/main.py