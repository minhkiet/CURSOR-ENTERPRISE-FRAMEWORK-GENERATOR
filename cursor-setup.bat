@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: Cursor Enterprise Framework - GUI Setup Launcher
:: Launches setup.bat with --gui-picker for easy folder selection
:: ============================================================

echo.
echo ============================================================
echo   Cursor Enterprise Framework - GUI Setup
echo ============================================================
echo.
echo   This will launch the Cursor Enterprise Framework setup
echo   with a graphical folder picker to select where you want
echo   to install the framework.
echo.

:: Check if running as administrator (sometimes needed for some folders)
net session >nul 2>&1
if %errorlevel%==0 (
    echo   [INFO] Running with administrator privileges.
) else (
    echo   [INFO] Running with standard user privileges.
)
echo.

:: Launch setup.bat with GUI picker
set "SETUP_SCRIPT=%~dp0setup.bat"
if not exist "%SETUP_SCRIPT%" (
    echo [ERROR] setup.bat not found in the same directory.
    echo   Please run this script from the framework folder.
    pause
    exit /b 1
)

echo [LAUNCH] Starting setup with folder picker...
echo.
call "%SETUP_SCRIPT%" --gui-picker

set "SETUP_EXIT=%errorlevel%"

if %SETUP_EXIT% equ 0 (
    echo.
    echo ============================================================
    echo   Setup completed successfully!
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo   Setup was cancelled or failed.
    echo ============================================================
)

pause
exit /b %SETUP_EXIT%
