#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Setting up Olympics Analysis Webapp..."

# Create Python virtual environment
python -m venv venv
echo "Virtual environment created."

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required Python packages
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "Python dependencies installed."
else
    echo "requirements.txt not found. Skipping Python dependencies installation."
fi

# Install frontend dependencies if package.json exists
if [ -f package.json ]; then
    if command -v npm >/dev/null 2>&1; then
        npm install
        echo "Frontend dependencies installed."
    else
        echo "npm not found. Please install Node.js and npm."
    fi
fi

echo "Setup complete."