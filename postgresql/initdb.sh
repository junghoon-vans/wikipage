#!/usr/bin/env bash

apt-get update && apt-get install postgresql-14-pgoutput

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    ALTER SYSTEM SET wal_level to 'logical';
EOSQL
