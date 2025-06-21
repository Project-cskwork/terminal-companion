@echo off
title Terminal AI Companion - One-Click Setup and Run
echo Terminal AI Companion - One-Click Setup and Run
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found
echo.

REM Check if we have a Windows-style virtual environment
if not exist venv\Scripts\python.exe (
    echo Creating/recreating virtual environment for Windows...
    if exist venv rmdir /s /q venv
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment and install packages
echo Installing/updating packages...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed!
    pause
    exit /b 1
)
echo Packages installed successfully
echo.

REM Setup environment file if it doesn't exist
if not exist .env (
    if exist .env.example (
        echo Setting up environment...
        copy .env.example .env
        echo .env file created from example
        echo Please edit .env file and add your OpenAI API key
        echo.
        echo Opening .env file for editing...
        notepad .env
        echo.
        echo Press any key when you've finished editing .env file...
        pause
    ) else (
        echo .env.example not found
        pause
        exit /b 1
    )
) else (
    echo .env file already exists
    echo.
)

REM Check AI provider configuration
findstr /C:"AI_PROVIDER=ollama" .env >nul
if not errorlevel 1 (
    echo Using Ollama local AI - no API key required
) else (
    findstr /C:"your_openai_api_key_here" .env >nul
    if not errorlevel 1 (
        echo Warning: API key not configured in .env file
        echo Please edit .env file and set your API key for your chosen provider
        echo.
        choice /C YN /M "Do you want to edit .env file now"
        if errorlevel 2 (
            echo Continuing with current configuration...
        ) else (
            notepad .env
            echo Press any key to continue...
            pause
        )
        echo.
    )
)

REM Create logs directory
if not exist logs mkdir logs

REM Run the application
echo Starting Terminal AI Companion...
echo.
venv\Scripts\python.exe main.py

echo.
echo Terminal AI Companion has ended.
pause