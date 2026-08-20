@echo off
REM Cursor Framework - Quick Utils Batch File
REM Usage: framework.bat <command>

setlocal enabledelayedexpansion

set "FRAMEWORK_ROOT=.cursor"
set "PYTHON=python"

REM Find Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    where python3 >nul 2>&1
    if %ERRORLEVEL% equ 0 set "PYTHON=python3"
)

if "%~1"=="" goto help
if "%~1"=="warm" goto warm
if "%~1"=="stats" goto stats
if "%~1"=="scan" goto scan
if "%~1"=="index" goto index
if "%~1"=="clear" goto clear
if "%~1"=="dashboard" goto dashboard
if "%~1"=="graph" goto graph
goto help

:warm
echo Warming framework cache...
%PYTHON% -m cursor_framework warm --root %FRAMEWORK_ROOT%
goto end

:stats
echo Fetching framework statistics...
%PYTHON% -m cursor_framework stats --root %FRAMEWORK_ROOT%
goto end

:scan
echo Scanning .cursor/ directory...
%PYTHON% -m cursor_framework scan --root %FRAMEWORK_ROOT%
goto end

:index
echo Rebuilding framework index...
%PYTHON% -m cursor_framework index --root %FRAMEWORK_ROOT%
goto end

:clear
echo Clearing framework cache...
if "%~2"=="-f" (
    %PYTHON% -m cursor_framework clear-cache --root %FRAMEWORK_ROOT% --force
) else (
    echo Dry-run mode. Use 'framework.bat clear -f' to actually delete.
    %PYTHON% -m cursor_framework clear-cache --root %FRAMEWORK_ROOT%
)
goto end

:dashboard
echo Starting dashboard server on port 8765...
echo Open http://localhost:8765 in your browser.
start http://localhost:8765
%PYTHON% -m cursor_framework serve --root %FRAMEWORK_ROOT% --port 8765
goto end

:graph
echo Starting graph server on port 8766...
echo Open http://localhost:8766 in your browser.
start http://localhost:8766
%PYTHON% -m cursor_framework serve-graph --root %FRAMEWORK_ROOT% --port 8766
goto end

:help
echo.
echo ================================================
echo   Cursor Framework - Quick Utils
echo ================================================
echo.
echo Available commands:
echo   warm       - Warm framework cache
echo   stats     - Show framework statistics
echo   scan      - Scan .cursor/ directory
echo   index     - Rebuild index
echo   clear     - Clear cache (add -f to force)
echo   dashboard - Open framework dashboard
echo   graph     - Open skill dependency graph
echo.
echo Examples:
echo   framework.bat warm
echo   framework.bat stats
echo   framework.bat clear -f
echo.

:end
endlocal
