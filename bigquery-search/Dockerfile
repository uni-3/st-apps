FROM python:3.11-slim AS builder
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_CACHE_DIR=/root/.cache/uv

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.11-slim
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app /app

COPY . /app/
RUN rm -rf /app/.git /app/__pycache__ /app/.pytest_cache

CMD ["streamlit", "run", "app.py", "--server.port", "8080"]
