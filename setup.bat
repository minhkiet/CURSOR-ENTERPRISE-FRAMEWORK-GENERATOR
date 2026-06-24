@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: Cursor Enterprise Framework Generator — Setup Script
:: Installs skills, rules, and memory into ~/.cursor/ for
:: cross-project use in Cursor IDE.
:: ============================================================

set "SOURCE_DIR=%~dp0"
set "USER_CURSOR_HOME=%USERPROFILE%\.cursor"
set "USER_SKILLS=%USERPROFILE%\.cursor\skills"
set "USER_RULES=%USERPROFILE%\.cursor\rules"
set "USER_MEMORY=%USERPROFILE%\.cursor\memory"

:: Normalize trailing backslash
if "%SOURCE_DIR:~-1%"=="\" set "SOURCE_DIR=%SOURCE_DIR:~0,-1%"

echo.
echo ============================================================
echo   Cursor Enterprise Framework — Cross-Project Setup
echo ============================================================
echo.
echo Source:      %SOURCE_DIR%
echo Dest Skills: %USER_SKILLS%
echo Dest Rules:  %USER_RULES%
echo Dest Memory: %USER_MEMORY%
echo.

:: ----------------------------------------------------------
:: Step 1: Detect if Cursor is running
:: ----------------------------------------------------------
echo [1/5] Checking for running Cursor instances...

tasklist /fi "imagename eq Cursor.exe" /nh 2>nul | findstr /i "Cursor.exe" >nul
if %errorlevel% equ 0 (
    echo   WARNING: Cursor appears to be running.
    echo   It is recommended to close Cursor before setup,
    echo   then restart it after installation completes.
    echo.
    set /p CONTINUE="   Continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo   Setup cancelled.
        exit /b 1
    )
)
echo   OK.

:: ----------------------------------------------------------
:: Step 2: Create destination directories
:: ----------------------------------------------------------
echo.
echo [2/5] Creating destination directories...

for %%D in ("%USER_SKILLS%" "%USER_RULES%" "%USER_MEMORY%") do (
    if not exist %%D (
        mkdir %%D 2>nul
        if !errorlevel! equ 0 (
            echo   Created: %%~D
        ) else (
            echo   FAILED to create: %%~D
            exit /b 1
        )
    ) else (
        echo   Exists:  %%~D
    )
)

:: ----------------------------------------------------------
:: Step 3: Sync skills (cross-project reusable)
::    Source:      .cursor\skills\
::    Destination: %USERPROFILE%\.cursor\skills\
:: ----------------------------------------------------------
echo.
echo [3/5] Syncing skills to ~/.cursor/skills/...

set "SKILLS_SOURCE=%SOURCE_DIR%\.cursor\skills"
if not exist "%SKILLS_SOURCE%" (
    echo   No skills directory found at source. Skipping.
) else (
    set COPIED=0
    set SKIPPED=0

    for /d %%S in ("%SKILLS_SOURCE%\*") do (
        set "SKILL_NAME=%%~nxS"
        set "DEST=%USER_SKILLS%\!SKILL_NAME!"

        if exist "!DEST!" (
            echo   !SKILL_NAME!  — already exists in ~/.cursor/skills/
            echo             Use --force to overwrite existing skills.
            set /a SKIPPED+=1
        ) else (
            robocopy "%%S" "!DEST!" /E /NFL /NDL /NJH /NJS >nul 2>&1
            if exist "!DEST!\SKILL.md" (
                echo   !SKILL_NAME!  — installed
                set /a COPIED+=1
            ) else (
                echo   !SKILL_NAME!  — SKILL.md not found, skipping
            )
        )
    )

    echo.
    echo   Installed: !COPIED! skill^(s^)
    if !SKIPPED! gtr 0 echo   Skipped:  !SKIPPED! skill^(s^) (already exist)
)

:: ----------------------------------------------------------
:: Step 4: Sync rules (cross-project reusable)
::    Source:      .cursor\rules\
::    Destination: %USERPROFILE%\.cursor\rules\
:: ----------------------------------------------------------
echo.
echo [4/5] Syncing rules to ~/.cursor/rules/...

set "RULES_SOURCE=%SOURCE_DIR%\.cursor\rules"
if not exist "%RULES_SOURCE%" (
    echo   No rules directory found at source. Skipping.
) else (
    set COPIED_RULES=0
    set SKIPPED_RULES=0

    for %%R in ("%RULES_SOURCE%\*.mdc") do (
        set "RULE_NAME=%%~nxR"
        set "DEST=%USER_RULES%\!RULE_NAME!"

        if exist "!DEST!" (
            echo   !RULE_NAME!  — already exists in ~/.cursor/rules/
            set /a SKIPPED_RULES+=1
        ) else (
            copy /Y "%%R" "!DEST!" >nul 2>&1
            if !errorlevel! equ 0 (
                echo   !RULE_NAME!  — installed
                set /a COPIED_RULES+=1
            ) else (
                echo   !RULE_NAME!  — FAILED
            )
        )
    )

    echo.
    echo   Installed: !COPIED_RULES! rule^(s^)
    if !SKIPPED_RULES! gtr 0 echo   Skipped:  !SKIPPED_RULES! rule^(s^) (already exist)
)

:: ----------------------------------------------------------
:: Step 5: Sync memory files (optional cross-project context)
::    Source:      .cursor\memory\
::    Destination: %USERPROFILE%\.cursor\memory\
:: ----------------------------------------------------------
echo.
echo [5/5] Syncing memory files to ~/.cursor/memory/...

set "MEMORY_SOURCE=%SOURCE_DIR%\.cursor\memory"
if not exist "%MEMORY_SOURCE%" (
    echo   No memory directory found at source. Skipping.
) else (
    set COPIED_MEM=0
    for %%M in ("%MEMORY_SOURCE%\*.md") do (
        set "MEM_NAME=%%~nxM"
        set "DEST=%USER_MEMORY%\!MEM_NAME!"
        copy /Y "%%M" "!DEST!" >nul 2>&1
        if !errorlevel! equ 0 (
            echo   !MEM_NAME!  — installed
            set /a COPIED_MEM+=1
        )
    )
    if !COPIED_MEM! equ 0 (
        echo   No memory files to sync.
    ) else (
        echo   Installed: !COPIED_MEM! memory file^(s^)
    )
)

:: ----------------------------------------------------------
:: Done
:: ----------------------------------------------------------
echo.
echo ============================================================
echo   Setup complete!
echo ============================================================
echo.
echo   Restart Cursor IDE to load the newly installed skills
echo   and rules. New chat sessions will automatically pick
echo   up the rules and skills based on your queries.
echo.
echo   Installed skills are available globally across all your
echo   Cursor projects and workspaces.
echo.
echo   Tip: Run this script again to pick up framework updates.
echo.
exit /b 0
