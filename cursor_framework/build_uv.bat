@echo off
REM =============================================================================
REM Cursor Enterprise Framework — Fast Setup & Verification with UV
REM =============================================================================

echo [INFO] Checking for uv package manager...
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARNING] uv not found on PATH.
    echo Installing uv via PowerShell installer...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

echo [INFO] uv version:
uv --version

echo.
echo [INFO] Creating virtual environment (.venv)...
uv venv .venv
call .venv\Scripts\activate.bat

echo.
echo [INFO] Installing cursor-framework and dependencies...
uv pip install -e ".[all]"

echo.
echo [INFO] Running automated test suite...
python -m unittest discover -s tests -v

echo.
echo [INFO] Testing Vibe Coding Tool Detection...
python -m cursor_framework vibe detect

echo.
echo [INFO] Testing Redis Observability Status...
python -m cursor_framework redis status

echo.
echo [INFO] Testing Prefect Automation Status...
python -m cursor_framework prefect list

echo.
echo =============================================================================
echo [SUCCESS] cursor-framework environment is ready and verified!
echo =============================================================================
pause
