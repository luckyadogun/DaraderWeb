#!/bin/sh

echo "collect static files"
python manage.py collectstatic --noinput

echo "apply database migrations"
python manage.py migrate

echo "starting server"
gunicorn --port=$PORT project.wsgi:application