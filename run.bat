@echo off
echo Amalthea Image Tagging Software
echo ==============================

cd /d %~dp0

echo Checking dependencies...
pip show Pillow >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies.
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
) else (
    echo Dependencies already installed.
)

echo Checking for images folder...
if not exist images\ (
    echo Creating images directory...
    mkdir images
    if %ERRORLEVEL% NEQ 0 (
        echo Warning: Could not create images directory.
    ) else (
        echo Images directory created successfully.
        echo Place your images in the 'images' folder to get started.
    )
) else (
    echo Images directory already exists.
)

echo Starting Amalthea...
set PYTHONPATH=%PYTHONPATH%;%CD%
python src\main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running Amalthea. 
    echo Please check that Python is installed correctly.
    pause
)