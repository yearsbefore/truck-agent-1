#!/bin/bash

echo "Truck Engineering AI Agent - Starting..."

# Create virtual environment if it does not exist
if [ ! -d "venv" ]; then
    echo "First run: creating virtual environment..."
    python3 -m venv venv
fi

# Install dependencies if not yet installed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies (one-time setup, please wait)..."
    venv/bin/pip install --upgrade pip
    venv/bin/pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Dependency installation failed."
        echo "Please send the error output above to your developer."
        read -p "Press Enter to exit..."
        exit 1
    fi
    touch venv/.installed
fi

# Initialize database if it does not exist
if [ ! -f "database/trucks.db" ]; then
    echo "Initializing database..."
    venv/bin/python database/init_db.py
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "  Please copy .env.example to .env"
    echo "  and fill in your OPENROUTER_API_KEY"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Starting web app on http://127.0.0.1:8501 ..."
venv/bin/python main.py
