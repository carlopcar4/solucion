#!/bin/bash
set -e

until pg_isready -h "$DB_HOST" -U "$DB_USERNAME"; do
    sleep 1
done

bundle exec rails db:create db:migrate

exec "$@"