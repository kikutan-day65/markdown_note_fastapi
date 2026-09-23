#!/bin/bash

set -e
set -u

USERNAME=$1
PASSWORD=${USERNAME}${RANDOM}

# Check whether the PostgreSQL user already exists.
if psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    -tAc "SELECT 1 FROM pg_roles WHERE rolname='${USERNAME}'" \
    | grep -q 1; then

    echo "User '${USERNAME}' already exists."
    exit 1
fi

echo "Creating user '${USERNAME}'..."

# Create the PostgreSQL user and grant database-level privileges.
psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" <<-EOSQL

    CREATE USER ${USERNAME} WITH PASSWORD '${PASSWORD}';

    GRANT ALL PRIVILEGES ON DATABASE $DEV_DB TO ${USERNAME};
    GRANT ALL PRIVILEGES ON DATABASE $TEST_DB TO ${USERNAME};

EOSQL

# Grant privileges on the public schema in the development database.
psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$DEV_DB" <<-EOSQL

    GRANT ALL PRIVILEGES ON SCHEMA public TO ${USERNAME};

EOSQL

# Grant privileges on the public schema in the test database.
psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$TEST_DB" <<-EOSQL

    GRANT ALL PRIVILEGES ON SCHEMA public TO ${USERNAME};

EOSQL

echo "User '${USERNAME}' created."
echo "Password: ${PASSWORD}"

{
    echo "USERNAME: ${USERNAME}"
    echo "PASSWORD: ${PASSWORD}"
    echo "created at: $(date)"
    echo "--------------------"
} >> /utils/logs/create_user.log

exit 0