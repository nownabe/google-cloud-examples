# docmatcher backend

## Generate protobuf python code

```sh
buf generate proto
```

## Dev server

### Run docker compose

Start docker-compose:

```sh
docker-compose up
```

### Setup

You have to run following commands only the first time.

```sh
poetry install
poetry run python tools/setup_spanner_emulator.py
poetry run python -m unidic download
```

### Run dev servers

Run servers:

```sh
poetry run uvicorn api_main:app --host 0.0.0.0 --port 3001 --reload
poetry run uvicorn vectorupdater_main:app --host 0.0.0.0 --port 3002 --reload
```
