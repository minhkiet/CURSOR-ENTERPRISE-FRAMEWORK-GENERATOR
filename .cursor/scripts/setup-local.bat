@echo off
REM =============================================================================
REM CURSOR ENTERPRISE FRAMEWORK - SETUP LOCAL
REM =============================================================================
REM Quick launcher for setup-local.ps1
REM =============================================================================

setlocal

set "SCRIPT_DIR=%~dp0"
set "SOURCE_ROOT=D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
set "SETUP_SCRIPT=%SOURCE_ROOT%\.cursor\scripts\setup-local.ps1"

if "%~1"=="" (
    echo.
    echo ============================================
    echo   CURSOR ENTERPRISE - LOCAL SETUP
    echo ============================================
    echo.
    echo Usage:
    echo   setup-local.bat [ProjectPath] [Options]
    echo.
    echo Options:
    echo   -List       List all projects
    echo   -DryRun     Preview without installing
    echo   -Force      Overwrite existing .cursor
    echo   -Backup     Backup before overwriting
    echo.
    echo Examples:
    echo   setup-local.bat "D:\Projects\MyApp"
    echo   setup-local.bat -List
    echo   setup-local.bat "D:\Projects\MyApp" -Force
    echo.
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%SETUP_SCRIPT%" %*

endlocal
