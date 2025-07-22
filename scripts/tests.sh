#!/bin/bash

# Exit on error
set -e

echo "Activating virtual environment..."
source ../.venv/Scripts/activate
cd ..

echo "Running all tests with coverage..."
pytest --cov=src --cov-report=term-missing

echo "Running mypy for type checking..."
mypy src

echo "Displaying coverage summary..."
coverage report --fail-under=70
