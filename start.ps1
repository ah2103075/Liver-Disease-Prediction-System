# ====================================================================
# Liver Disease Prediction System - Startup Script (PowerShell)
# ====================================================================
# This script starts both backend and frontend servers automatically
# Compatible with: Windows PowerShell, PowerShell Core
# ====================================================================

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "      Liver Disease Prediction System" -ForegroundColor Cyan
Write-Host "            Starting Servers..." -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""

# Change to script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check for virtual environment
$venvPath = Join-Path $ScriptDir ".venv"
$pythonCmd = "python"
$activateScript = ""

if (Test-Path $venvPath) {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    $activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
    $pythonCmd = Join-Path $venvPath "Scripts\python.exe"
} else {
    Write-Host "ℹ️  No virtual environment found, using system Python" -ForegroundColor Yellow
}
Write-Host ""

# Check if Python is installed
try {
    if (Test-Path $pythonCmd) {
        $pythonVersion = & $pythonCmd --version 2>&1
    } else {
        $pythonVersion = python --version 2>&1
        $pythonCmd = "python"
    }
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check dependencies
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
$dependenciesCheck = & $pythonCmd -c "import fastapi, uvicorn, sklearn, pandas, numpy" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Some dependencies are missing. Installing..." -ForegroundColor Yellow
    & $pythonCmd -m pip install fastapi uvicorn pydantic scikit-learn pandas numpy
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "✅ All dependencies installed" -ForegroundColor Green
Write-Host ""

# Start Backend Server
Write-Host "🚀 Starting Backend Server (Port 5000)..." -ForegroundColor Cyan
$backendPath = Join-Path $ScriptDir "Backend"
if ($activateScript -and (Test-Path $activateScript)) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; & '$activateScript'; python main.py" -WindowStyle Normal
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; & '$pythonCmd' main.py" -WindowStyle Normal
}
Start-Sleep -Seconds 3

Write-Host "✅ Backend running on http://localhost:5000" -ForegroundColor Green
Write-Host ""

# Start Frontend Server
Write-Host "🌐 Starting Frontend Server (Port 8000)..." -ForegroundColor Cyan
$frontendPath = Join-Path $ScriptDir "frontend"
if ($activateScript -and (Test-Path $activateScript)) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; & '$activateScript'; python -m http.server 8000" -WindowStyle Normal
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; & '$pythonCmd' -m http.server 8000" -WindowStyle Normal
}
Start-Sleep -Seconds 2

Write-Host "✅ Frontend running on http://localhost:8000" -ForegroundColor Green
Write-Host ""

Write-Host "========================================================" -ForegroundColor Green
Write-Host "🎉 System is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Access the application:" -ForegroundColor Cyan
Write-Host "   🌐 Frontend: http://localhost:8000" -ForegroundColor White
Write-Host "   🔌 Backend API: http://localhost:5000" -ForegroundColor White
Write-Host "   📚 API Docs: http://localhost:5000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Two new PowerShell windows have opened:" -ForegroundColor Yellow
Write-Host "   1. Backend Server (Port 5000)" -ForegroundColor White
Write-Host "   2. Frontend Server (Port 8000)" -ForegroundColor White
Write-Host ""
Write-Host "Close those windows to stop the servers" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""

# Open browser
Start-Sleep -Seconds 1
Start-Process "http://localhost:8000"

Write-Host "Press any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
