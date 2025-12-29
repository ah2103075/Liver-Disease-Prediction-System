#!/bin/bash

# ====================================================================
# Liver Disease Prediction System - Startup Script (Bash)
# ====================================================================
# This script starts both backend and frontend servers automatically
# Compatible with: Git Bash, WSL, Linux, macOS
# ====================================================================

echo "🫀 Liver Disease Prediction System - Starting..."
echo "================================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check for virtual environment
VENV_PATH="$SCRIPT_DIR/.venv"
if [ -d "$VENV_PATH" ]; then
    echo -e "${GREEN}✅ Virtual environment found${NC}"
    if [ -f "$VENV_PATH/Scripts/python" ]; then
        # Windows Git Bash
        PYTHON_CMD="$VENV_PATH/Scripts/python"
    elif [ -f "$VENV_PATH/bin/python" ]; then
        # Linux/Mac
        PYTHON_CMD="$VENV_PATH/bin/python"
    fi
else
    echo -e "${YELLOW}ℹ️  No virtual environment found, detecting system Python${NC}"
    # Try multiple Python commands for Windows compatibility
    if command -v py &> /dev/null; then
        PYTHON_CMD="py"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python is not installed!${NC}"
        echo "Please install Python 3.8+ from https://www.python.org/"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Python found: $($PYTHON_CMD --version 2>&1)${NC}"
echo ""

# Check if required packages are installed
echo "📦 Checking dependencies..."
$PYTHON_CMD -c "import fastapi, uvicorn, sklearn, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Some dependencies are missing. Installing...${NC}"
    $PYTHON_CMD -m pip install fastapi uvicorn pydantic scikit-learn pandas numpy
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies!${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ All dependencies installed${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT SIGTERM

# Start Backend Server
echo "🚀 Starting Backend Server (Port 5000)..."
cd Backend
$PYTHON_CMD main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${RED}❌ Backend failed to start!${NC}"
    echo "Check Backend/main.py for errors"
    exit 1
fi

echo -e "${GREEN}✅ Backend running on http://localhost:5000${NC}"
echo ""

# Start Frontend Server
echo "🌐 Starting Frontend Server (Port 8000)..."
cd frontend
$PYTHON_CMD -m http.server 8000 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 2

# Check if frontend is running
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${RED}❌ Frontend failed to start!${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo -e "${GREEN}✅ Frontend running on http://localhost:8000${NC}"
echo ""
echo "================================================"
echo -e "${GREEN}🎉 System is ready!${NC}"
echo ""
echo "📋 Access the application:"
echo "   🌐 Frontend: http://localhost:8000"
echo "   🔌 Backend API: http://localhost:5000"
echo "   📚 API Docs: http://localhost:5000/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo "================================================"

# Open browser (if xdg-open is available)
if command -v xdg-open &> /dev/null; then
    sleep 1
    xdg-open http://localhost:8000 2>/dev/null &
elif command -v open &> /dev/null; then
    sleep 1
    open http://localhost:8000 2>/dev/null &
fi

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID
