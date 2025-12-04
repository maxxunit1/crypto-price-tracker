@echo off
title Crypto Price Tracker

echo.
echo ========================================
echo   CRYPTO PRICE TRACKER - LAUNCHER
echo ========================================
echo.

REM Check Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Download from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo.

REM Create venv if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create venv
        pause
        exit /b 1
    )
    echo Virtual environment created!
    echo.
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate venv
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -q customtkinter aiohttp
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Starting Crypto Price Tracker...
echo.

REM Run app
python crypto_tracker.py

REM Keep window open if error
if errorlevel 1 (
    echo.
    echo Application exited with error
    pause
)
