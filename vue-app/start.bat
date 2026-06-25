@echo off
echo ================================================
echo CEF Landing Vue App - Setup
echo ================================================
echo.

cd /d "%~dp0"

echo Checking Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js found:
node --version
echo.

echo Installing dependencies...
call npm install

if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo Setup complete!
    echo ================================================
    echo.
    echo To start development server:
    echo   npm run dev
    echo.
    echo To build for production:
    echo   npm run build
    echo.
) else (
    echo.
    echo [ERROR] Failed to install dependencies
    echo.
)

pause
