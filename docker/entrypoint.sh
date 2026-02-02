#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL is up. Running migrations..."

/app/venv/bin/alembic upgrade head

echo "Migrations applied. Starting API..."

exec python -m src.app
