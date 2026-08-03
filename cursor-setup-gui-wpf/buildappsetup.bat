@echo off
REM ============================================================
REM buildappsetup.bat
REM Cursor Enterprise Framework - Combined Build Script
REM ============================================================
REM Purpose:
REM   1. Build the cursor-setup-gui-wpf project (Debug/Release)
REM   2. Create the latest cursor-setup.zip from .cursor contents
REM   3. Place outputs in bin\<Config>\net8.0-windows\win-x64\
REM
REM Usage:
REM   buildappsetup.bat              (default: Debug + zip)
REM   buildappsetup.bat Release      (build Release + zip)
REM   buildappsetup.bat /clean       (clean bin/obj before build)
REM   buildappsetup.bat /help        (show this help)
REM
REM Outputs (in bin\<Config>\net8.0-windows\win-x64\):
REM   - cursor-setup-wpf.exe          (WPF installer app)
REM   - cursor-setup.zip              (framework archive, 24+ MB)
REM   - cursor-setup-build.json       (build metadata)
REM   - Resources\vi.txt              (Vietnamese localization)
REM   - Resources\en.txt              (English localization)
REM
REM Requirements:
REM   - .NET 8 SDK installed (dotnet on PATH)
REM   - PowerShell available
REM ============================================================

setlocal EnableExtensions EnableDelayedExpansion

REM ----- Configuration -----
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_DIR=%SCRIPT_DIR%"
set "BUILD_CONFIG=Debug"
set "BUILD_RID=win-x64"
set "TFM=net8.0-windows"
set "OUTPUT_DIR=%PROJECT_DIR%\bin\%BUILD_CONFIG%\%TFM%\%BUILD_RID%"
set "ZIP_SCRIPT=%PROJECT_DIR%\build-zip.ps1"
set "BUILD_LOG=%PROJECT_DIR%\build.log"

REM ----- Parse arguments -----
set "DO_CLEAN=0"
:parse_args
if "%~1"=="" goto :end_parse
if /i "%~1"=="Debug"   set "BUILD_CONFIG=Debug"   & shift & goto :parse_args
if /i "%~1"=="Release" set "BUILD_CONFIG=Release" & shift & goto :parse_args
if /i "%~1"=="/clean"  set "DO_CLEAN=1"           & shift & goto :parse_args
if /i "%~1"=="-clean"  set "DO_CLEAN=1"           & shift & goto :parse_args
if /i "%~1"=="/help"   goto :show_help
if /i "%~1"=="-help"   goto :show_help
if /i "%~1"=="/?"       goto :show_help
echo [WARN] Unknown argument: %~1
shift
goto :parse_args
:end_parse

REM ----- Header -----
echo.
echo ===========================================================
echo  Cursor Enterprise Framework - Combined Build
echo ===========================================================
echo  Project : %PROJECT_DIR%
echo  Config  : %BUILD_CONFIG%
echo  Output  : %OUTPUT_DIR%
echo  Clean   : %DO_CLEAN%
echo ===========================================================
echo.

REM ----- Step 0: Check prerequisites -----
echo [STEP 0] Checking prerequisites...

where dotnet >nul 2>&1
if errorlevel 1 (
    echo [ERROR] dotnet CLI not found on PATH. Install .NET 8 SDK first.
    exit /b 1
)
for /f "delims=" %%v in ('dotnet --version') do set "DOTNET_VERSION=%%v"
echo   [OK] dotnet version: %DOTNET_VERSION%

where powershell >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell not found on PATH.
    exit /b 1
)
echo   [OK] PowerShell available.

if not exist "%PROJECT_DIR%\CursorSetupWpf.csproj" (
    echo [ERROR] CursorSetupWpf.csproj not found at %PROJECT_DIR%
    exit /b 1
)
echo   [OK] Project file found.

if not exist "%ZIP_SCRIPT%" (
    echo [ERROR] build-zip.ps1 not found at %ZIP_SCRIPT%
    exit /b 1
)
echo   [OK] Packager script found.

echo.

REM ----- Step 1 (optional): Clean -----
if "%DO_CLEAN%"=="1" (
    echo [STEP 1] Cleaning previous build artifacts...
    if exist "%PROJECT_DIR%\bin"      rd /s /q "%PROJECT_DIR%\bin"
    if exist "%PROJECT_DIR%\obj"      rd /s /q "%PROJECT_DIR%\obj"
    echo   [OK] bin/ and obj/ cleaned.
    echo.
)

REM ----- Step 2: Build the WPF project -----
echo [STEP 2] Building cursor-setup-gui-wpf (%BUILD_CONFIG%)...
echo.
pushd "%PROJECT_DIR%"

dotnet build "%PROJECT_DIR%\CursorSetupWpf.csproj" -c %BUILD_CONFIG% --nologo
if errorlevel 1 (
    echo.
    echo [ERROR] dotnet build failed!
    popd
    exit /b 1
)

popd
echo.
echo   [OK] Build succeeded.
echo.

REM ----- Step 3: Verify output dir -----
if not exist "%OUTPUT_DIR%" (
    echo [ERROR] Output directory missing after build: %OUTPUT_DIR%
    exit /b 1
)

REM ----- Step 4: Create cursor-setup.zip -----
echo [STEP 4] Creating cursor-setup.zip...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%ZIP_SCRIPT%"
if errorlevel 1 (
    echo.
    echo [ERROR] cursor-setup.zip creation failed!
    exit /b 1
)

REM ----- Step 5: Verify outputs -----
echo.
echo [STEP 5] Verifying outputs...
set "MISSING=0"
for %%f in ("cursor-setup-wpf.exe" "cursor-setup.zip" "Resources\vi.txt" "Resources\en.txt") do (
    if not exist "%OUTPUT_DIR%\%%~f" (
        echo   [MISSING] %%~f
        set "MISSING=1"
    ) else (
        echo   [OK] %%~f
    )
)

if "%MISSING%"=="1" (
    echo [ERROR] Some expected outputs are missing!
    exit /b 1
)

REM ----- Summary -----
echo.
echo ===========================================================
echo  Build complete!
echo ===========================================================
echo  Output : %OUTPUT_DIR%
echo.
for %%f in ("cursor-setup.zip" "cursor-setup-wpf.exe") do (
    if exist "%OUTPUT_DIR%\%%~f" (
        for %%a in ("%OUTPUT_DIR%\%%~f") do (
            set "SZ=%%~za"
            set /a "SZ_MB=!SZ! / 1048576"
            echo   %%~f  -  !SZ_MB! MB
        )
    )
)
echo ===========================================================
echo.

endlocal
exit /b 0

:show_help
echo.
echo Usage:
echo   buildappsetup.bat              Build Debug + zip
echo   buildappsetup.bat Release      Build Release + zip
echo   buildappsetup.bat /clean       Clean bin/obj before build
echo   buildappsetup.bat /help        Show this help
echo.
exit /b 0