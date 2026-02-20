#!/bin/sh
set -e

echo "Waiting for database..."
python manage.py migrate --no-input

echo "Collecting static files..."
python manage.py collectstatic --no-input

exec "$@"
