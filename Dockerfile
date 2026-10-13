FROM python:3.12 AS base

COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /bin/uv
ENV UV_PROJECT_ENVIRONMENT=/usr/local UV_COMPILE_BYTECODE=1

WORKDIR /src
COPY pyproject.toml uv.lock ./

FROM base AS test
RUN uv sync --locked --no-install-project
COPY moonbot ./moonbot
COPY tests ./tests
CMD ["pytest", "tests", "--e2e"]

FROM base
RUN uv sync --locked --no-install-project --no-dev
COPY moonbot ./moonbot
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "moonbot.app.app:app"]
