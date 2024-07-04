# Exploring FastAPI
This repo is an investigation of FastAPI development flow.

Based on personal experience and resources such as:
- [Netflix's Dispatch](https://github.com/Netflix/dispatch)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [FastAPI Production Template](https://github.com/zhanymkanov/fastapi_production_template)
- [Bunnybook](https://github.com/pietrobassi/bunnybook)
- [Litestar Fullstack Reference Application](https://github.com/litestar-org/litestar-fullstack)

// TODO: Update desc

## Local Development

### Setup just
MacOS:
```shell
brew install just
```

Debian/Ubuntu:
```shell
apt install just
````

Others: [link](https://github.com/casey/just?tab=readme-ov-file#packages)

### Setup poetry
```shell
pip install poetry
```

Other ways: [link](https://python-poetry.org/docs/#installation)

### Setup Postgres (16.3)
```shell
just up
```
### Copy the environment file and install dependencies
1. `cp .env.example .env`
2. `poetry install`

### Run the uvicorn server
In default `dev` mode
```shell
just dev
```

### Linters
Lint the code
```shell
just lint
```

### Formatters
Format the code
```shell
just fmt
```

### Migrations
- Create an automatic migration based on DB models changes
```shell
just mm *migration_name*
```
- Run migrations
```shell
just migrate
```
- Downgrade migrations
```shell
just downgrade downgrade -1  # or -2 or base or hash of the migration
```

### Tests
Run tests
```shell
just test
```

## Deployment
TBD
