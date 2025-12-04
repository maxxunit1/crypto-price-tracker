@echo off
chcp 65001 > nul
title Crypto Price Tracker - Launcher

echo.
echo ===============================================
echo 💎 CRYPTO PRICE TRACKER - LAUNCHER
echo ===============================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo ⚠️ IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo ⚡ Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if requirements are installed
if not exist "venv\Lib\site-packages\customtkinter\" (
    echo 📥 Installing dependencies...
    echo This may take 30-60 seconds on first run...
    echo.
    python -m pip install --upgrade pip > nul 2>&1
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
    echo.
) else (
    REM Check if requirements.txt was updated
    pip install -r requirements.txt --quiet > nul 2>&1
)

echo 🚀 Starting Crypto Price Tracker...
echo.
echo ===============================================
echo.

REM Run the application
python crypto_tracker.py

REM If app crashes, show error
if errorlevel 1 (
    echo.
    echo ===============================================
    echo ❌ Application exited with error
    echo ===============================================
    echo.
    pause
)
