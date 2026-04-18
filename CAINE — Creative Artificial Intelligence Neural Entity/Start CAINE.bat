@echo off
chcp 65001 >nul 2>&1
title CAINE — Creative Artificial Intelligence Neural Entity

REM Check if Python 3.12 is available.
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Python 3.12 not found.
    echo     Run the install.bat file first.
    echo.
    pause
    exit /b 1
)

REM Check if the torch is installed.
py -3.12 -c "import torch" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Dependencies not found.
    echo     Run the install.bat file first.
    echo.
    pause
    exit /b 1
)

REM Open the Caine menu.
py -3.12 caine_launcher.py
