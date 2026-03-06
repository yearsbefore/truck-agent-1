@echo off

echo Truck Engineering AI Agent - Starting...

if not exist "venv" (
    echo First run: creating virtual environment...
    python -m venv venv
)

if not exist "venv\.installed" (
    echo Installing dependencies, please wait...
    venv\Scripts\pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Dependency installation failed.
        pause
        exit /b 1
    )
    type nul > venv\.installed
)

if not exist "database\trucks.db" (
    echo Initializing database...
    venv\Scripts\python database\init_db.py
)

if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and fill in your API key.
    pause
    exit /b 1
)

echo Starting web app on http://127.0.0.1:8501 ...
venv\Scripts\python main.py
pause
