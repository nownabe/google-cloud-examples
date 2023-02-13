# docmatcher backend

## Generate protobuf python code

```sh
buf generate proto
```

## Dev server

Start docker-compose:

```sh
docker-compose up
```

You have to create instance and database the first time:

```sh
poetry run python tools/setup_spanner_emulator.py
```

Run server:

```sh
poetry run uvicorn api_main:app --host 0.0.0.0 --port 3001 --reload
```
