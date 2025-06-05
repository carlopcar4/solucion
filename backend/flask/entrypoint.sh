#!/bin/bash
set -e

until pg_isready -h "$DB_HOST" -U "$DB_USERNAME"; do
    sleep 1
done

bundle exec rails db:create
bundle exec rails decidim:install:migrations
bundle exec rails db:migrate
bundle exec rails db:seed

exec "$@"