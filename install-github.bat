@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: Quick Install from GitHub - Cursor Enterprise Framework
:: ============================================================
:: Usage:
::   install-github.bat                       - Use default repo
::   install-github.bat [repo-url]            - Use custom repo
::   install-github.bat [repo-url] [branch]   - Custom repo + branch
:: ============================================================

set "DEFAULT_REPO=https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR"
set "DEFAULT_BRANCH=main"
set "INSTALL_DIR=%TEMP%\cef-install"

:: Parse arguments
set "REPO_URL=%~1"
set "BRANCH=%~2"
if "%REPO_URL%"=="" set "REPO_URL=%DEFAULT_REPO%"
if "%BRANCH%"=="" set "BRANCH=%DEFAULT_BRANCH%"

echo.
echo ============================================================
echo   Cursor Enterprise Framework - Quick GitHub Install
echo ============================================================
echo.
echo   Repository: %REPO_URL%
echo   Branch:     %BRANCH%
echo   Target:     %USERPROFILE%\.cursor
echo.

:: Clean up previous install
if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%" 2>nul

:: Method 1: Try git clone first
echo [1/3] Attempting git clone...
where git >nul 2>&1
if !errorlevel! equ 0 (
    git clone --branch "%BRANCH%" --depth 1 "%REPO_URL%" "%INSTALL_DIR%" 2>nul
    if !errorlevel! equ 0 (
        echo   Clone successful!
        goto :run_setup
    )
)
echo   Git clone not available or failed.

:: Method 2: Download ZIP
echo.
echo [2/3] Attempting ZIP download...

:: Parse repo URL to extract user/repo path
set "REPO_PATH=%REPO_URL%"
set "REPO_PATH=!REPO_PATH:https://github.com/=!"
set "REPO_PATH=!REPO_PATH:http://github.com/=!"
set "REPO_PATH=!REPO_PATH:git@github.com:=!"
set "REPO_PATH=!REPO_PATH:.git=!"
set "REPO_PATH=!REPO_PATH:/=!"

:: Strip leading/trailing slashes
set "REPO_PATH=!REPO_PATH:~1!"
if "!REPO_PATH:~-1!"=="/" set "REPO_PATH=!REPO_PATH:~0,-1!"

set "ZIP_URL=https://github.com/!REPO_PATH!/archive/refs/heads/%BRANCH%.zip"
set "ZIP_FILE=%TEMP%\cef.zip"

echo   URL: !ZIP_URL!

powershell -Command "Invoke-WebRequest -Uri '!ZIP_URL!' -OutFile '!ZIP_FILE!' -ErrorAction SilentlyContinue"
if not exist "!ZIP_FILE!" (
    echo   Download failed.
    echo.
    echo [ERROR] Could not download from GitHub.
    echo   Please check:
    echo   - Internet connection
    echo   - Repository URL: %REPO_URL%
    echo   - Branch exists:  %BRANCH%
    exit /b 1
)

echo   Download successful!
echo.
echo [3/3] Extracting files...

powershell -Command "Expand-Archive -Path '!ZIP_FILE!' -DestinationPath '%INSTALL_DIR%' -Force"

:: Find and flatten the extracted folder (GitHub creates repo-branch/ subfolder)
for /d %%D in ("%INSTALL_DIR%\*") do (
    echo   Found folder: %%~nxD
    :: Move all contents out of the extracted subfolder
    for /f "delims=" %%F in ('dir /b "%%D" 2^>nul') do (
        xcopy /s /y "%%D\%%F" "%INSTALL_DIR%\" 2>nul
    )
    rmdir /s /q "%%D" 2>nul
)

echo   Extraction complete!

:run_setup
:: Run the setup, passing source dir via environment variable
echo.
echo [SETUP] Running setup from downloaded files...
set "CEF_SOURCE_DIR=%INSTALL_DIR%"
"%INSTALL_DIR%\setup.bat" --force --no-cursor-check

:: Cleanup
del /f /q "!ZIP_FILE!" 2>nul
rmdir /s /q "%INSTALL_DIR%" 2>nul

echo.
echo ============================================================
echo   Installation Complete!
echo ============================================================
echo.
echo   Please restart Cursor IDE to load the framework.
echo.
pause
