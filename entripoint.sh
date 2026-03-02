#!/bin/sh

echo "Running database migrations"
uv run alembic upgrade head

echo "Starting API server..."
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000