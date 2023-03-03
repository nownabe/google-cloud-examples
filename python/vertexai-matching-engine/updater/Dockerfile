FROM python:3.9-slim

ENV POETRY_NO_INTERACTION=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR  /app

RUN pip install --no-cache-dir --disable-pip-version-check poetry

COPY poetry.toml /app/
COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN poetry install --only main

COPY . /app

CMD ["poetry", "run", "python", "main.py"]