@echo off
:: ============================================================
:: CEF - Main Quick Launcher
:: Version: 4.2.0
:: ============================================================
:: Quick access to all CEF commands
:: ============================================================
:: Usage:
::   go.bat dev          - Start Vue dev server
::   go.bat build        - Build Vue app
::   go.bat deploy       - Build + Deploy to Vercel
::   go.bat setup        - Install framework to user profile
::   go.bat help         - Show this help
:: ============================================================

setlocal enabledelayedexpansion

set "CMD=%~1"

if "%CMD%"=="" set "CMD=help"
if "%CMD%"=="?" set "CMD=help"

goto :cmd_%CMD%

:cmd_help
echo.
echo ================================================
echo   CEF - Quick Launcher Help
echo ================================================
echo.
echo   Usage: go.bat [command]
echo.
echo   Commands:
echo     dev      - Start Vue dev server (localhost:5173)
echo     build    - Build Vue app for production
echo     preview  - Preview built app (localhost:4173)
echo     deploy   - Build + Deploy to Vercel (preview)
echo     deploy prod - Build + Deploy to Vercel (production)
echo     setup    - Install framework to user profile
echo     help     - Show this help
echo.
echo ================================================
echo   Vue App Commands (in cursor_framework_web folder):
echo ================================================
echo     go.bat dev     - Start dev server
echo     go.bat build   - Production build
echo     go.bat preview - Preview built app
echo.
goto :end

:cmd_dev
cd /d "%~dp0cursor_framework_web"
call go.bat
goto :end

:cmd_build
cd /d "%~dp0cursor_framework_web"
call npm run build
goto :end

:cmd_preview
cd /d "%~dp0cursor_framework_web"
call preview.bat
goto :end

:cmd_deploy
set "MODE=%~2"
if /i "%MODE%"=="prod" (
    cd /d "%~dp0cursor_framework_web"
    call run.bat prod
) else (
    cd /d "%~dp0cursor_framework_web"
    call run.bat
)
goto :end

:cmd_setup
call setup-user.bat
goto :end

:end
endlocal
