@echo off
echo 🤖 RAG System - Project Startup
echo ================================
echo.

echo 📋 Prerequisites Check:
echo.

echo 🔍 Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

echo 🔍 Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found! Please install Node.js 18+
    pause
    exit /b 1
) else (
    echo ✅ Node.js found
)

echo 🔍 Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Ollama not found - you'll need to install it
    echo 📥 Download from: https://ollama.ai/download
    echo.
) else (
    echo ✅ Ollama found
)

echo.
echo 🚀 Starting RAG System...
echo.

echo 📝 Step 1: Starting Backend...
start "RAG Backend" cmd /k "cd backend && python run.py"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo 📝 Step 2: Starting Frontend...
start "RAG Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Both services are starting!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo 💡 Keep both terminal windows open
echo 🚪 Close this window when done
echo.
pause
