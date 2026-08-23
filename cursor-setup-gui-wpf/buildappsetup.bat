@echo off
REM ============================================================
REM buildappsetup.bat
REM Cursor Enterprise Framework - Build Script
REM ============================================================
REM Purpose:
REM   1. Build the cursor-setup-gui-wpf project (Debug/Release)
REM   2. Create cursor-setup.zip from .cursor contents
REM   3. Copy MCP tools to .cursor/mcp
REM
REM Usage:
REM   buildappsetup.bat              (default: Release)
REM   buildappsetup.bat Debug        (build Debug)
REM   buildappsetup.bat Release      (build Release)
REM   buildappsetup.bat /clean       (clean bin/obj before build)
REM   buildappsetup.bat /help        (show this help)
REM
REM Outputs (in bin\<Config>\net8.0-windows\win-x64\):
REM   - cursor-setup-wpf.exe          (WPF installer app)
REM   - cursor-setup.zip              (framework archive)
REM   - Resources\vi.txt             (Vietnamese localization)
REM   - Resources\en.txt             (English localization)
REM
REM Requirements:
REM   - .NET 8 SDK installed
REM   - PowerShell available
REM ============================================================

setlocal EnableDelayedExpansion

REM ----- Configuration -----
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_DIR=%SCRIPT_DIR%"
set "BUILD_CONFIG=Release"
set "BUILD_RID=win-x64"
set "TFM=net8.0-windows"
set "OUTPUT_DIR=%PROJECT_DIR%\bin\%BUILD_CONFIG%\%TFM%\%BUILD_RID%"
set "ZIP_SCRIPT=%PROJECT_DIR%\build-zip.ps1"
set "COPY_MCP_SCRIPT=%PROJECT_DIR%\Copy-McpTools.ps1"

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

REM Update OUTPUT_DIR after config is parsed
set "OUTPUT_DIR=%PROJECT_DIR%\bin\%BUILD_CONFIG%\%TFM%\%BUILD_RID%"

REM ----- Header -----
echo.
echo ===========================================================
echo  Cursor Enterprise Framework - Build Script
echo ===========================================================
echo  Project   : %PROJECT_DIR%
echo  Config    : %BUILD_CONFIG%
echo  Output    : %OUTPUT_DIR%
echo  Clean     : %DO_CLEAN%
echo ===========================================================
echo.

REM ----- Step 0: Check prerequisites -----
echo [STEP 0] Checking prerequisites...

REM Check dotnet
where dotnet >nul 2>&1
if errorlevel 1 (
    echo [ERROR] dotnet CLI not found. Install .NET 8 SDK first.
    exit /b 1
)
for /f "delims=" %%v in ('dotnet --version 2^>nul') do set "DOTNET_VERSION=%%v"
echo   [OK] dotnet version: !DOTNET_VERSION!

REM Check PowerShell
where powershell >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell not found.
    exit /b 1
)
echo   [OK] PowerShell available.

REM Check project file
if not exist "%PROJECT_DIR%\CursorSetupWpf.csproj" (
    echo [ERROR] CursorSetupWpf.csproj not found.
    exit /b 1
)
echo   [OK] Project file found.

REM Check scripts
if not exist "%ZIP_SCRIPT%" (
    echo [ERROR] build-zip.ps1 not found.
    exit /b 1
)
echo   [OK] build-zip.ps1 found.

if not exist "%COPY_MCP_SCRIPT%" (
    echo [WARN] Copy-McpTools.ps1 not found.
)

echo.

REM ----- Step 1: Clean (optional) -----
if "%DO_CLEAN%"=="1" (
    echo [STEP 1] Cleaning previous builds...
    if exist "%PROJECT_DIR%\bin"    rd /s /q "%PROJECT_DIR%\bin"    2>nul
    if exist "%PROJECT_DIR%\obj"    rd /s /q "%PROJECT_DIR%\obj"    2>nul
    echo   [OK] Cleaned.
    echo.
)

REM ----- Step 2: Build WPF project -----
echo [STEP 2] Building WPF project...
echo.

pushd "%PROJECT_DIR%" >nul

REM Build with restore first
dotnet restore "%PROJECT_DIR%\CursorSetupWpf.csproj" -v q
if errorlevel 1 (
    echo [ERROR] dotnet restore failed!
    popd >nul
    exit /b 1
)

dotnet build "%PROJECT_DIR%\CursorSetupWpf.csproj" -c %BUILD_CONFIG% --nologo -v q
if errorlevel 1 (
    echo.
    echo [ERROR] dotnet build failed!
    popd >nul
    exit /b 1
)

popd >nul

echo.
echo   [OK] Build succeeded.
echo.

REM ----- Step 3: Copy MCP tools -----
echo [STEP 3] Copying MCP tools...

if exist "%COPY_MCP_SCRIPT%" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%COPY_MCP_SCRIPT%"
    if errorlevel 1 (
        echo   [WARN] MCP copy had issues, continuing...
    ) else (
        echo   [OK] MCP tools copied.
    )
) else (
    echo   [SKIP] Copy-McpTools.ps1 not found.
)
echo.

REM ----- Step 4: Create ZIP -----
echo [STEP 4] Creating cursor-setup.zip...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%ZIP_SCRIPT%" -Config %BUILD_CONFIG%
if errorlevel 1 (
    echo.
    echo [ERROR] ZIP creation failed!
    exit /b 1
)

REM ----- Step 5: Verify outputs -----
echo.
echo [STEP 5] Verifying outputs...
echo.

set "MISSING=0"

REM Check .exe
if exist "%OUTPUT_DIR%\cursor-setup-wpf.exe" (
    for %%A in ("%OUTPUT_DIR%\cursor-setup-wpf.exe") do echo   [OK] cursor-setup-wpf.exe
) else (
    echo   [MISSING] cursor-setup-wpf.exe
    set "MISSING=1"
)

REM Check .zip
if exist "%OUTPUT_DIR%\cursor-setup.zip" (
    for %%A in ("%OUTPUT_DIR%\cursor-setup.zip") do (
        set "ZS=%%~zA"
        set /a "ZM=ZS / 1048576"
        echo   [OK] cursor-setup.zip ^(!ZM! MB^)
    )
) else (
    echo   [MISSING] cursor-setup.zip
    set "MISSING=1"
)

REM Check Resources
if exist "%OUTPUT_DIR%\Resources\vi.txt" (
    echo   [OK] Resources\vi.txt
) else (
    echo   [MISSING] Resources\vi.txt
    set "MISSING=1"
)

if exist "%OUTPUT_DIR%\Resources\en.txt" (
    echo   [OK] Resources\en.txt
) else (
    echo   [MISSING] Resources\en.txt
    set "MISSING=1"
)

REM Check .cursor\mcp
if exist "%PROJECT_DIR%\.cursor\mcp" (
    echo   [OK] .cursor\mcp directory exists
) else (
    echo   [WARN] .cursor\mcp not found
)

echo.

if "%MISSING%"=="1" (
    echo [ERROR] Build completed but some files are missing!
    exit /b 1
)

REM ----- Summary -----
echo.
echo ===========================================================
echo  Build SUCCESS!
echo ===========================================================
echo  Output : %OUTPUT_DIR%
echo.
echo  Artifacts:
echo    - cursor-setup-wpf.exe
if exist "%OUTPUT_DIR%\cursor-setup.zip" (
    for %%A in ("%OUTPUT_DIR%\cursor-setup.zip") do (
        set "ZS=%%~zA"
        set /a "ZM=ZS / 1048576"
        echo    - cursor-setup.zip ^(!ZM! MB^)
    )
)
echo    - Resources\vi.txt
echo    - Resources\en.txt
echo ===========================================================
echo.

endlocal
exit /b 0

:show_help
echo.
echo Usage:
echo   buildappsetup.bat              Build Debug
echo   buildappsetup.bat Release      Build Release
echo   buildappsetup.bat /clean      Clean before build
echo   buildappsetup.bat /help       Show this help
echo.
exit /b 0
