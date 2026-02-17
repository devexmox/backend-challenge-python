FROM python:3.12 AS base

ENV POETRY_HOME=/opt/poetry
ENV PATH="${PATH}:${POETRY_HOME}/bin"
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /src
COPY pyproject.toml poetry.lock* ./

FROM base AS test
RUN poetry config virtualenvs.create false &&\
    poetry install --no-interaction --no-root --with dev
COPY moonbot ./moonbot
COPY tests ./tests
CMD ["pytest", "tests", "--e2e"]

FROM base
RUN poetry config virtualenvs.create false &&\
    poetry install --no-interaction --no-root --without dev
COPY moonbot ./moonbot
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "moonbot.app.app:app"]
