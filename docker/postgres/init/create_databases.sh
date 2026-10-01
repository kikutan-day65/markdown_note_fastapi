#!/bin/bash

set -e
set -u

psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" <<-EOSQL

    \echo "Creating app_user"
    CREATE USER $DB_USERNAME WITH PASSWORD '$DB_PASSWORD';

    \echo "Creating database: $DEV_DB"
    CREATE DATABASE $DEV_DB OWNER $DB_USERNAME;

    \echo "Creating database: $TEST_DB"
    CREATE DATABASE $TEST_DB OWNER $DB_USERNAME;

EOSQL