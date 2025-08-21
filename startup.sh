#!/bin/bash

# Install dependencies
echo "Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the Flask application with Gunicorn
echo "Starting Flask application with Gunicorn..."
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app