#! /usr/bin/env bash

echo "Waiting for postgres..."
python /app/app/backend_pre_start.py

echo "Running migrations"
alembic upgrade head
