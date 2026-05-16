@echo off
REM Flight Scheduler - Quick Start Setup for Windows
REM This script will set up and run the flight scheduler locally

echo.
echo ========================================
echo Flight Scheduler - Local Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [2/5] Creating virtual environment...
    python -m venv .venv
) else (
    echo [2/5] Virtual environment already exists
)

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r backend\requirements-dev.txt

REM Check if .env exists, if not create from template
if not exist ".env" (
    echo [5/5] Creating .env file from template...
    copy .env.example .env
    echo Created .env - using SQLite for local development
) else (
    echo [5/5] .env file already exists
)

REM Initialize database
echo.
echo ========================================
echo Initializing database with seed data...
echo ========================================
cd backend
python seed_data.py
if errorlevel 1 (
    echo [WARNING] seed_data.py execution had issues
) else (
    echo Database initialized successfully
)

REM Start the server
echo.
echo ========================================
echo Starting Flight Scheduler Backend
echo ========================================
echo.
echo Server will run on: http://localhost:5000
echo Frontend: Open browser to http://localhost:5000/index.html
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

REM Keep window open if there's an error
if errorlevel 1 (
    pause
)
