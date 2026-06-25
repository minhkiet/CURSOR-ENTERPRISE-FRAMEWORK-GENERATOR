@echo off
:: ============================================================
:: CEF Vue App - Build & Deploy (All-in-One)
:: Version: 1.0.0
:: ============================================================
:: One-command: build + deploy to Vercel
:: Usage:
::   run.bat          - Build + deploy to preview
::   run.bat prod     - Build + deploy to production
:: ============================================================

cd /d "%~dp0"
set "MODE=%~1"

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
)

echo.
echo ================================================
echo   CEF Vue App - Build & Deploy
echo ================================================
echo.

:: Step 1: Build
echo [1/2] Building production...
call npm run build
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo       Build complete!
echo.

:: Step 2: Deploy
echo [2/2] Deploying...
if /i "%MODE%"=="prod" (
    echo       Deploying to PRODUCTION...
    call npx vercel --prod
) else (
    echo       Deploying to PREVIEW...
    call npx vercel
)

echo.
echo ================================================
echo   Done!
echo ================================================
echo.
pause
