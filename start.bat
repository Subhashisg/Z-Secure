@echo off
echo ===============================================
echo    EncryptPro v2 - Enterprise Image Security
echo ===============================================
echo.

echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Installing dependencies...
pip install -r requirements.txt

echo [INFO] Checking camera permissions...
echo Please allow camera access when prompted by your browser.
echo.

echo [INFO] Starting EncryptPro v2...
echo.
echo The application will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
