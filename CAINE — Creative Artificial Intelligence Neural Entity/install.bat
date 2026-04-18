@echo off
chcp 65001 >nul 2>&1
title CAINE - Installer

echo.
echo ================================================
echo   CAINE - INSTALLER
echo   Do this only once.
echo ================================================
echo.

REM 1. Check and install Python 3.12
echo [1/5] Checking Python 3.12...
py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python 3.12 is already installed.
    goto python_ok
)

echo Python 3.12 not found. Downloading installer...
echo (Please wait, this may take a few minutes.)
echo.

REM Download the Python 3.12 installer with curl (available on Windows 10+).
curl -L --ssl-no-revoke -o "%temp%\python312_installer.exe" https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe
if %errorlevel% neq 0 (
    echo.
    echo [!] Failed to download Python. Check your internet connection.
    echo     Manually install from:
    echo     https://www.python.org/downloads/release/python-3129/
    echo     IMPORTANT: Check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing Python 3.12...
"%temp%\python312_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1
if %errorlevel% neq 0 (
    echo.
    echo [!] Python installation failed.
    echo     Try installing manually at:
    echo     https://www.python.org/downloads/release/python-3129/
    pause
    exit /b 1
)

REM Update the current session's PATH to recognize the newly installed py.
set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"

py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Python is installed, but it hasn't been recognized yet.
    echo     Close this terminal, open a new one, and run install.bat again.
    pause
    exit /b 1
)
echo [OK] Python 3.12 installed successfully.

:python_ok
py -3.12 --version
echo.

REM 2. Update pip
echo [2/5] Updating pip...
py -3.12 -m pip install --upgrade pip --quiet
echo [OK] pip updated.
echo.

REM 3. Install PyTorch
echo [3/5] Installing PyTorch...
echo (This may take several minutes, Torch has ~2GB.)
echo.
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo NVIDIA GPU detected. Installing CUDA version...
    py -3.12 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --quiet
) else (
    echo GPU not detected. Installing CPU version...
    py -3.12 -m pip install torch torchvision torchaudio --quiet
)
if %errorlevel% neq 0 (
    echo [!] Error installing PyTorch. Check your internet connection.
    pause
    exit /b 1
)
echo [OK] PyTorch installed.
echo.

REM 4. Installs additional dependencies.
echo [4/5] Installing additional dependencies...
py -3.12 -m pip install transformers diffusers accelerate --quiet
py -3.12 -m pip install Pillow --quiet
py -3.12 -m pip install pygame==2.6.1 --quiet
py -3.12 -m pip install duckduckgo-search requests --quiet
py -3.12 -m pip install groq --quiet
if %errorlevel% neq 0 (
    echo [!] Error installing dependencies. Please try again.
    pause
    exit /b 1
)
echo [OK] Installed dependencies.
echo.

REM 5. Check installation
echo [5/5] Checking installation...
py -3.12 -c "import torch, transformers, diffusers, PIL, pygame; print('[OK] Todas as libs funcionando.')"
if %errorlevel% neq 0 (
    echo [!] Verification failed. Try running the installer again.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   INSTALLATION COMPLETE!
echo   Now use the start.bat file to open Caine.
echo ================================================
echo.
pause
