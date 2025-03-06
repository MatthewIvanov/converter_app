#!/bin/bash 

echo "Applying database migrations..."
alembic upgrade head

echo "Starting application..."
exec gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
