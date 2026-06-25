@echo off
:: ============================================================
:: CEF Vue App - Preview Only (No Deploy)
:: Version: 1.0.0
:: ============================================================
:: One-command to preview built app locally
:: ============================================================

cd /d "%~dp0"

:: Check dist folder
if not exist "dist" (
    echo [ERROR] No dist folder found!
    echo Please run 'run.bat' to build first.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   CEF Vue App - Preview Mode
echo ================================================
echo.
echo   Opening preview at: http://localhost:4173
echo.
echo   Press Ctrl+C to stop
echo.
npm run preview
