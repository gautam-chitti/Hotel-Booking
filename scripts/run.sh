#!/bin/bash

set -e

echo "Starting the System"

# Activate virtual environment
source ../.venv/Scripts/activate

cd ..
# Launch FastAPI with auto-reload (dev mode)
echo "🌐 Launching FastAPI server at http://127.0.0.1:8000 ..."
uvicorn src.api.main:app --reload
