#!/bin/bash
# Flight Scheduler - Quick Start Setup for macOS/Linux
# This script will set up and run the flight scheduler locally

echo ""
echo "========================================"
echo "Flight Scheduler - Local Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Checking Python installation..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[2/5] Creating virtual environment..."
    python3 -m venv .venv
else
    echo "[2/5] Virtual environment already exists"
fi

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install -r backend/requirements-dev.txt

# Check if .env exists, if not create from template
if [ ! -f ".env" ]; then
    echo "[5/5] Creating .env file from template..."
    cp .env.example .env
    echo "Created .env - using SQLite for local development"
else
    echo "[5/5] .env file already exists"
fi

# Initialize database
echo ""
echo "========================================"
echo "Initializing database with seed data..."
echo "========================================"
cd backend
python3 seed_data.py
if [ $? -ne 0 ]; then
    echo "[WARNING] seed_data.py execution had issues"
else
    echo "Database initialized successfully"
fi

# Start the server
echo ""
echo "========================================"
echo "Starting Flight Scheduler Backend"
echo "========================================"
echo ""
echo "Server will run on: http://localhost:5000"
echo "Frontend: Open browser to http://localhost:5000/index.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
