FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_CACHE_DIR=/root/.cache/uv

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.12-slim-bookworm

RUN groupadd -r app && useradd -r -g app app
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder --chown=app:app /app /app
COPY --chown=app:app . /app
RUN rm -rf /app/.git /app/__pycache__ /app/.pytest_cache

USER app
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8080"]
