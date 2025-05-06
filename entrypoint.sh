#!/bin/sh

python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic --noinput --clear

gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
