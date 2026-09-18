# syntax=docker/dockerfile:1

# --- builder: uv で依存関係を仮想環境に解決する ---
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# 依存定義だけを先にコピーし、レイヤーキャッシュを効かせる
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# アプリ本体を追加してから再度 sync（プロジェクト自体をインストール）
COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# --- runtime: uv を含まない最小構成で実行する ---
FROM python:3.13-slim-bookworm

WORKDIR /app

# builder で作った venv とアプリ本体だけをコピーする
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
