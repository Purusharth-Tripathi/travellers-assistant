#!/bin/bash
# Render startup script for Traveller's Assistant

# Activate virtual environment if it exists
if [ -d "/opt/render/project/src/.venv" ]; then
    source /opt/render/project/src/.venv/bin/activate
fi

# Run the Flask app
cd backend && python3 app.py
