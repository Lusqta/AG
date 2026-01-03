@echo off
title Dealership CRM
cd /d "%~dp0"

:: Check if venv exists
if not exist "venv" (
    echo [ERROR] Virtual environment 'venv' not found!
    echo Please run 'python -m venv venv' and install requirements.
    pause
    exit /b
)

:: Activate venv and run server
call venv\Scripts\activate
echo Starting Dealership CRM...
echo Access at: http://127.0.0.1:8000
echo.
python manage.py runserver 127.0.0.1:8000
pause
