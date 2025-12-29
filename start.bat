@echo off
REM ====================================================================
REM Liver Disease Prediction System - Startup Script (Windows Batch)
REM ====================================================================
REM This script starts both backend and frontend servers automatically
REM Compatible with: Windows Command Prompt (cmd.exe)
REM ====================================================================

title Liver Disease Prediction System
color 0A

echo ========================================================
echo        Liver Disease Prediction System
echo               Starting Servers...
echo ========================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check for virtual environment
set "VENV_PATH=%~dp0.venv"
set "PYTHON_CMD=python"
set "ACTIVATE_CMD="

if exist "%VENV_PATH%\Scripts\python.exe" (
    echo [OK] Virtual environment found
    set "PYTHON_CMD=%VENV_PATH%\Scripts\python.exe"
    set "ACTIVATE_CMD=%VENV_PATH%\Scripts\activate.bat"
) else (
    echo [INFO] No virtual environment found, using system Python
)
echo.

REM Check if Python is installed
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
%PYTHON_CMD% --version
echo.

REM Check dependencies
echo [INFO] Checking dependencies...
%PYTHON_CMD% -c "import fastapi, uvicorn, sklearn, pandas, numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] Some dependencies missing. Installing...
    %PYTHON_CMD% -m pip install fastapi uvicorn pydantic scikit-learn pandas numpy
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo [OK] All dependencies installed
echo.

REM Start Backend Server in new window
echo [INFO] Starting Backend Server (Port 5000)...
if defined ACTIVATE_CMD (
    start "Backend Server - Port 5000" cmd /k "cd /d "%~dp0Backend" && call "%ACTIVATE_CMD%" && python main.py"
) else (
    start "Backend Server - Port 5000" cmd /k "cd /d "%~dp0Backend" && "%PYTHON_CMD%" main.py"
)
timeout /t 3 /nobreak >nul

echo [OK] Backend running on http://localhost:5000
echo.

REM Start Frontend Server in new window
echo [INFO] Starting Frontend Server (Port 8000)...
if defined ACTIVATE_CMD (
    start "Frontend Server - Port 8000" cmd /k "cd /d "%~dp0frontend" && call "%ACTIVATE_CMD%" && python -m http.server 8000"
) else (
    start "Frontend Server - Port 8000" cmd /k "cd /d "%~dp0frontend" && "%PYTHON_CMD%" -m http.server 8000"
)
timeout /t 2 /nobreak >nul

echo [OK] Frontend running on http://localhost:8000
echo.

echo ========================================================
echo [SUCCESS] System is ready!
echo.
echo Access the application:
echo    Frontend: http://localhost:8000
echo    Backend API: http://localhost:5000
echo    API Docs: http://localhost:5000/docs
echo.
echo Two new windows have opened:
echo    1. Backend Server (Port 5000)
echo    2. Frontend Server (Port 8000)
echo.
echo Close those windows to stop the servers
echo ========================================================
echo.

REM Open browser
timeout /t 2 /nobreak >nul
start http://localhost:8000

echo Press any key to close this window...
pause >nul
