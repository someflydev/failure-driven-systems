FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY services/api ./services/api

RUN groupadd --system opledger \
    && useradd --system --gid opledger --home-dir /app --shell /usr/sbin/nologin opledger \
    && chown -R opledger:opledger /app

USER opledger

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3).read()"

CMD ["uv", "run", "--no-sync", "uvicorn", "opledger_api.main:app", "--app-dir", "services/api", "--host", "0.0.0.0", "--port", "8000"]
