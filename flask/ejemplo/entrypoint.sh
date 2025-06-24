#!/bin/bash
set -e


echo "Creando y migrando la base de datos..."
bundle exec yarn install
bundle exec rails db:create
bundle exec rails db:migrate
bundle exec bin/shakapacker

echo "Iniciando el servidor Puma..."
exec bundle exec puma -C config/puma.rb