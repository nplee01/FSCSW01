#!/usr/bin/env sh

# Entrypoint commands to run for backtest app's docker image
# Expects to be run in app home (where manage.py is)

# Wait for DB first, then create DB tables, then create app data, then run gunicorn wsgi server
python manage.py wait_for_db && \
python manage.py migrate && \
python manage.py appdata && \
gunicorn --bind 0.0.0.0:3000 --workers 5 backtest.wsgi:application
