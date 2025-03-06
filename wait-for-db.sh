#!/bin/bash
set -e

host="${DB_HOST:-db}"
port="${DB_PORT:-5432}"

echo "Waiting for database at $host:$port..."

until nc -z "$host" "$port"; do
    echo "#####################################################"
  sleep 10
done

echo "Database is ready."
exec "$@"
