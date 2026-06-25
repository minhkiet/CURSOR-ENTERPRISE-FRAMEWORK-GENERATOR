@echo off
:: ============================================================
:: CEF - Quick Setup (Install Framework to User Profile)
:: Version: 4.2.0
:: ============================================================
:: One-command to install/update Cursor Enterprise Framework
:: ============================================================
:: Usage:
::   setup-user.bat              - Install/Update
::   setup-user.bat --force      - Force overwrite
:: ============================================================

cd /d "%~dp0"

echo.
echo ================================================
echo   CEF Framework - User Setup
echo ================================================
echo.

:: Run the main setup with no-cursor-check for convenience
if "%~1"=="--force" (
    echo [INFO] Force mode enabled
    call setup.bat --force --no-cursor-check
) else (
    call setup.bat --no-cursor-check
)

echo.
echo ================================================
echo   Setup complete!
echo ================================================
echo.
pause
