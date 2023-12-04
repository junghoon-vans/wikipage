#! /usr/bin/env bash

echo "Running migrations"
alembic upgrade head
