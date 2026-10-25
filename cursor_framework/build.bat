@echo off
REM ============================================================
REM Cursor Framework Build Script
REM ============================================================
REM 
REM Usage:
REM   build.bat              - Build in development mode
REM   build.bat install      - Install package
REM   build.bat clean       - Clean build artifacts
REM   build.bat test        - Run tests
REM   build.bat dist        - Create distribution package
REM
REM ============================================================

setlocal enabledelayedexpansion

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM Remove trailing backslash if present
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Go up one level to project root (script is in cursor_framework subfolder)
for %%i in ("%SCRIPT_DIR%") do set "PROJECT_ROOT=%%~dpi"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

REM Framework dir is the script dir
set "FRAMEWORK_DIR=%SCRIPT_DIR%"

cd /d "%PROJECT_ROOT%"

echo.
echo ============================================================
echo   Cursor Framework Build Script
echo ============================================================
echo.

REM Parse command
set "CMD=%1"
if "%CMD%"=="" set "CMD=dev"

if "%CMD%"=="install" goto :install
if "%CMD%"=="clean" goto :clean
if "%CMD%"=="test" goto :test
if "%CMD%"=="dist" goto :dist
if "%CMD%"=="dev" goto :dev
if "%CMD%"=="warm" goto :warm
if "%CMD%"=="dashboard" goto :dashboard
goto :usage

:usage
echo Usage: build.bat [command]
echo.
echo Commands:
echo   dev      - Development mode (default)
echo   install  - Install package in editable mode
echo   clean    - Clean build artifacts
echo   test     - Run tests
echo   dist     - Create distribution package
echo   warm     - Warm up cache and index
echo   dashboard - Start dashboard server
echo.
goto :end

:dev
echo [DEV] Installing in development mode...
cd /d "%FRAMEWORK_DIR%"
python -m pip install -e . --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install in dev mode
    goto :end
)
echo [OK] Development mode ready
echo.
echo Running warm-up...
cd /d "%PROJECT_ROOT%"
python -m cursor_framework warm --root ".cursor"
goto :end

:install
echo [INSTALL] Installing package...
cd /d "%FRAMEWORK_DIR%"
python -m pip install .
if errorlevel 1 (
    echo [ERROR] Installation failed
    goto :end
)
echo [OK] Package installed successfully
goto :end

:clean
echo [CLEAN] Removing build artifacts...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.egg-info" rmdir /s /q "*.egg-info"
if exist "cursor_framework.egg-info" rmdir /s /q "cursor_framework.egg-info"
if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
if exist "htmlcov" rmdir /s /q "htmlcov"
if exist ".coverage" del /q ".coverage" 2>nul
echo [OK] Clean complete
goto :end

:test
echo [TEST] Running tests...
if not exist "tests" (
    echo [WARN] No tests folder found
    goto :end
)
python -m pytest tests/ -v --tb=short
if errorlevel 1 (
    echo [WARN] Some tests failed
)
goto :end

:dist
echo [DIST] Creating distribution package...
cd /d "%FRAMEWORK_DIR%"
python -m pip install --upgrade build --quiet
python -m build
if errorlevel 1 (
    echo [ERROR] Build failed
    goto :end
)
echo [OK] Distribution created in dist\
dir /b dist\*.whl dist\*.tar.gz 2>nul
goto :end

:warm
echo [WARM] Warming up framework cache and index...
python -m cursor_framework warm --root ".cursor"
echo.
echo [OK] Warm-up complete
goto :end

:dashboard
echo [DASHBOARD] Starting dashboard server...
echo.
echo Open: http://127.0.0.1:8765
echo Press Ctrl+C to stop
echo.
python -m cursor_framework serve --root ".cursor"
goto :end

:end
echo.
echo ============================================================
echo   Build complete
echo ============================================================
echo.
endlocal
