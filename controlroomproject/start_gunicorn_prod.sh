#!/bin/bash

# Wait for database to be ready
python manage.py wait_for_db

# Run migrations
python manage.py migrate

# Start Gunicorn
gunicorn controlroomproject.wsgi:application --bind 0.0.0.0:8000