@echo off
REM Universal Converter Installation Script for Windows
REM This script installs Universal Converter and its dependencies

echo Universal Converter Installation Script for Windows
echo ===================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv universal-converter-env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Please ensure you have the venv module installed
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call universal-converter-env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

REM Create launch script
echo Creating launch script...
(
echo @echo off
echo cd /d "%%~dp0"
echo call universal-converter-env\Scripts\activate.bat
echo python main.py %%*
echo pause
) > run_universal_converter.bat

echo Installation completed successfully!
echo.
echo How to run Universal Converter:
echo   Method 1: Double-click run_universal_converter.bat
echo   Method 2: Run 'python main.py' from the activated environment
echo.
echo Optional dependencies for enhanced functionality:
echo   - FFmpeg: Download from https://ffmpeg.org/download.html
echo     Add ffmpeg.exe to your system PATH for video/audio conversion
echo   - LibreOffice: Download from https://www.libreoffice.org/
echo     Required for advanced document conversions
echo   - Pandoc: Download from https://pandoc.org/installing.html
echo     Enhanced document format support
echo   - wkhtmltopdf: Download from https://wkhtmltopdf.org/downloads.html
echo     Better PDF generation from HTML/code
echo.
echo Notes:
echo   - The application is installed in: %CD%
echo   - Virtual environment: %CD%\universal-converter-env
echo   - To uninstall, simply delete this folder
echo.
echo If you encounter issues:
echo   1. Make sure Python 3.8+ is installed and in PATH
echo   2. Install Visual C++ Redistributable if needed
echo   3. Try running: pip install -r requirements.txt
echo.
echo Happy converting!
pause