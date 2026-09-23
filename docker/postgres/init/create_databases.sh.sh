#!/bin/bash

set -e
set -u

psql -v ON_ERROR_STOP=1 \
--username "$POSTGRES_USER" \
--dbname "$POSTGRES_DB" <<-EOSQL

    \echo "Creating database: $DEV_DB"
    CREATE DATABASE $DEV_DB;

    \echo "Creating database: $TEST_DB"
    CREATE DATABASE $TEST_DB;

EOSQL
