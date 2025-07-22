#!/bin/sh
set -e

# Run migrations
python manage.py migrate --noinput

# Collect static files (optional, uncomment if needed)
# python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn worklog.wsgi:application --bind 0.0.0.0:8000 