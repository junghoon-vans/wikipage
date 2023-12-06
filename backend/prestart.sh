#! /usr/bin/env bash

echo "Running migrations"
alembic upgrade head

echo "Inserting initial data"
python app/db/init_db.py --path /app/init_table.sql
