#!/bin/sh
set -e

poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head

poetry run python -m app.api
