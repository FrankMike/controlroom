#!/bin/sh

source ../.venv/bin/activate
pip install -r requirements.txt
exec gunicorn controlroomproject.wsgi -c controlroomproject/gunicorn_settings.py