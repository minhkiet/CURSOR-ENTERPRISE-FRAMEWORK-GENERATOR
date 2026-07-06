@echo off
:: ============================================================
:: CEF Vue App - Development Server (Debug Mode)
:: ============================================================
:: Starts Vite dev server with hot reload
:: Usage:
::   debug.bat          - Start with default settings
::   debug.bat 5173     - Start on specific port
:: ============================================================

cd /d "%~dp0"

set "PORT=%~1"
if "%PORT%"=="" set "PORT=5173"

:: Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install from: https://nodejs.org/
    pause
    exit /b 1
)

:: Install deps if needed
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo.
echo ================================================
echo   CEF Vue App - Dev Server
echo ================================================
echo.
echo   Local:    http://localhost:%PORT%
echo   Network:  http://192.168.1.1:%PORT%
echo.
echo   Press Ctrl+C to stop the server
echo ================================================
echo.

:: Start dev server
npm run dev -- --port %PORT%
