# docmatcher backend

## Generate protobuf python code

```sh
buf generate proto
```

## Run dev server

```sh
poetry run uvicorn api_main:app --host 0.0.0.0 --port 3001 --reload
```
