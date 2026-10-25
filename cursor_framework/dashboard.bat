@echo off
REM ============================================================
REM Cursor Framework Dashboard Launcher
REM ============================================================
REM 
REM Usage:
REM   dashboard.bat          - Start dashboard on port 8765
REM   dashboard.bat 8080     - Start dashboard on custom port
REM
REM Requirements:
REM   - Python 3.8+
REM   - pip install -e cursor_framework (or from parent directory)
REM
REM ============================================================

setlocal

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM Remove trailing backslash if present
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Go up one level to project root (script is in cursor_framework subfolder)
for %%i in ("%SCRIPT_DIR%") do set "PROJECT_ROOT=%%~dpi"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

set "CURSOR_ROOT=%PROJECT_ROOT%\.cursor"
set "MEMORY_PATH=%PROJECT_ROOT%\.cache\memory.json"

REM Get port from argument or use default
set "PORT=%1"
if "%PORT%"=="" set "PORT=8765"

echo.
echo ============================================================
echo   Cursor Framework - Live Dashboard
echo ============================================================
echo.
echo   Root:      %CURSOR_ROOT%
echo   Memory:    %MEMORY_PATH%
echo   Port:      %PORT%
echo.
echo   Open:      http://127.0.0.1:%PORT%
echo.
echo   Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

REM Create .cache folder if it doesn't exist
if not exist "%PROJECT_ROOT%\.cache" mkdir "%PROJECT_ROOT%\.cache"

REM Run the dashboard server
cd /d "%PROJECT_ROOT%"
python -m cursor_framework serve --root ".cursor" --memory-path ".cache\memory.json" --port %PORT%
