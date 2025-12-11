#!/bin/bash

# Start Celery Worker in background
celery -A worker.tasks worker --loglevel=info &

# Start FastAPI Backend
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
