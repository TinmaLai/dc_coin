@echo off
set FLASK_ENV=production
gunicorn "run:app" --config config/production.py
