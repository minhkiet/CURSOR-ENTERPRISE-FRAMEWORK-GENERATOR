@echo off
:: ============================================================
:: CEF Vue App - Quick Dev Launcher
:: Version: 1.0.0
:: ============================================================
:: One-command to start Vue dev server with hot reload
:: ============================================================

cd /d "%~dp0"

:: Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install from: https://nodejs.org/
    pause
    exit /b 1
)

:: Install deps if node_modules missing
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)

:: Start dev server
echo.
echo ================================================
echo   Starting CEF Vue App Dev Server...
echo ================================================
echo.
echo   Local:   http://localhost:5173
echo.
echo   Press Ctrl+C to stop
echo.
npm run dev
