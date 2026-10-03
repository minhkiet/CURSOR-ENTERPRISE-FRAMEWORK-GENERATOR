@echo off
REM ============================================================
REM buildappsetup.bat
REM Cursor Enterprise Framework - Build Script v4.4.0
REM ============================================================
REM Purpose:
REM   1. Check prerequisites (dotnet, scripts, MCP tools)
REM   2. Clean bin/obj (optional via /clean)
REM   3. Publish the cursor-setup-gui-wpf project (self-contained, single-file)
REM   4. Copy MCP tools to .cursor/mcp
REM   5. Create cursor-setup.zip from .cursor contents
REM   6. Verify all outputs exist
REM
REM Usage:
REM   buildappsetup.bat              (default: Release, self-contained)
REM   buildappsetup.bat Debug        (build Debug)
REM   buildappsetup.bat Release      (build Release)
REM   buildappsetup.bat /clean       (clean bin/obj before build)
REM   buildappsetup.bat /help        (show this help)
REM
REM Outputs (in bin\<Config>\net8.0-windows\win-x64\publish\):
REM   - ToolRunCursor.exe             (self-contained single-file WPF installer)
REM   - cursor-setup.zip              (framework archive)
REM   - Resources\vi.txt             (Vietnamese localization)
REM   - Resources\en.txt             (English localization)
REM   - cursor-setup-build.json      (build metadata)
REM
REM Requirements:
REM   - .NET 8 SDK installed
REM   - PowerShell available
REM   - tools/cursor-framework-mcp directory
REM   - tools/cursor-autopilot-mcp directory
REM   - tools/cursor-memory-mcp directory
REM ============================================================

setlocal EnableDelayedExpansion

REM ----- Configuration -----
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_DIR=%SCRIPT_DIR%"
set "BUILD_CONFIG=Release"
set "BUILD_RID=win-x64"
set "TFM=net8.0-windows"
set "REPO_ROOT=%PROJECT_DIR%\.."
set "TOOLS_DIR=%REPO_ROOT%\tools"
set "OUTPUT_DIR=%PROJECT_DIR%\bin\%BUILD_CONFIG%\%TFM%\%BUILD_RID%\publish"
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
set "OUTPUT_DIR=%PROJECT_DIR%\bin\%BUILD_CONFIG%\%TFM%\%BUILD_RID%\publish"

REM ----- Header -----
echo.
echo ===========================================================
echo  Cursor Enterprise Framework - Build Script v4.4.0
echo ===========================================================
echo  Project   : %PROJECT_DIR%
echo  Config    : %BUILD_CONFIG%
echo  Output     : %OUTPUT_DIR%
echo  Repo Root  : %REPO_ROOT%
echo  Tools Dir  : %TOOLS_DIR%
echo  Clean      : %DO_CLEAN%
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

REM Check required MCP tools directories
set "MCP_MISSING=0"
set "MCP_LIST=cursor-framework-mcp cursor-autopilot-mcp cursor-memory-mcp"
for %%M in (!MCP_LIST!) do (
    if not exist "%TOOLS_DIR%\%%M" (
        echo [WARN] %%M not found in tools\
        set "MCP_MISSING=1"
    ) else (
        for %%F in ("%TOOLS_DIR%\%%M") do echo   [OK] tools\%%~nxF\ exists
    )
)
if "!MCP_MISSING!"=="1" (
    echo [WARN] Some MCP tools are missing. Build may not include all tools.
)

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

REM ----- Step 2: Publish WPF project (self-contained, single-file) -----
echo [STEP 2] Publishing WPF project (self-contained single-file)...
echo.

pushd "%PROJECT_DIR%" >nul

REM Publish with self-contained + single-file so the .exe runs standalone
REM without requiring .NET runtime to be installed on the target machine.
dotnet publish "%PROJECT_DIR%\CursorSetupWpf.csproj" ^
    -c %BUILD_CONFIG% ^
    -r %BUILD_RID% ^
    --self-contained true ^
    -p:PublishSingleFile=true ^
    -p:IncludeNativeLibrariesForSelfExtract=true ^
    -p:EnableCompressionInSingleFile=true ^
    --nologo -v q
if errorlevel 1 (
    echo.
    echo [ERROR] dotnet publish failed!
    popd >nul
    exit /b 1
)

popd >nul

echo.
echo   [OK] Publish succeeded (self-contained, single-file).
echo.

REM ----- Step 3: Copy MCP tools -----
echo [STEP 3] Copying MCP tools to .cursor\mcp...

if exist "%COPY_MCP_SCRIPT%" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%COPY_MCP_SCRIPT%"
    if errorlevel 1 (
        echo   [WARN] MCP copy had issues, continuing...
    ) else (
        echo   [OK] MCP tools copied to .cursor\mcp.
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
echo.

REM ----- Step 5: Verify outputs -----
echo.
echo [STEP 5] Verifying outputs...
echo.

set "MISSING=0"

REM Check .exe in publish folder
if exist "%OUTPUT_DIR%\ToolRunCursor.exe" (
    for %%A in ("%OUTPUT_DIR%\ToolRunCursor.exe") do (
        set "ZS=%%~zA"
        set /a "ZM=ZS / 1048576"
        echo   [OK] ToolRunCursor.exe ^(!ZM! MB^)
    )
) else (
    echo   [MISSING] ToolRunCursor.exe  ^(expected in %OUTPUT_DIR%\^)
    set "MISSING=1"
)

REM Check .zip in publish folder
if exist "%OUTPUT_DIR%\cursor-setup.zip" (
    for %%A in ("%OUTPUT_DIR%\cursor-setup.zip") do (
        set "ZS=%%~zA"
        set /a "ZM=ZS / 1048576"
        echo   [OK] cursor-setup.zip ^(!ZM! MB^)
    )
) else (
    echo   [MISSING] cursor-setup.zip  ^(expected in %OUTPUT_DIR%\^)
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

REM Check build metadata
if exist "%OUTPUT_DIR%\cursor-setup-build.json" (
    echo   [OK] cursor-setup-build.json
) else (
    echo   [MISSING] cursor-setup-build.json
    set "MISSING=1"
)

REM Check .cursor\mcp
if exist "%REPO_ROOT%\.cursor\mcp" (
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
if exist "%OUTPUT_DIR%\ToolRunCursor.exe" (
    for %%A in ("%OUTPUT_DIR%\ToolRunCursor.exe") do (
        set "ZS=%%~zA"
        set /a "ZM=ZS / 1048576"
        echo    - ToolRunCursor.exe ^(!ZM! MB^) self-contained
    )
)
if exist "%OUTPUT_DIR%\cursor-setup.zip" (
    for %%A in ("%OUTPUT_DIR%\cursor-setup.zip") do (
        set "ZS=%%~zA"
        set /a "ZM=ZS / 1048576"
        echo    - cursor-setup.zip ^(!ZM! MB^)
    )
)
echo    - Resources\vi.txt
echo    - Resources\en.txt
echo    - cursor-setup-build.json
echo ===========================================================
echo.

endlocal
exit /b 0

:show_help
echo.
echo Usage:
echo   buildappsetup.bat              Build Release (self-contained)
echo   buildappsetup.bat Debug       Build Debug   (self-contained)
echo   buildappsetup.bat Release     Build Release (self-contained)
echo   buildappsetup.bat /clean      Clean before build
echo   buildappsetup.bat /help       Show this help
echo.
echo Outputs go to: bin\^\<Config^\>\net8.0-windows\win-x64\publish\
exit /b 0
