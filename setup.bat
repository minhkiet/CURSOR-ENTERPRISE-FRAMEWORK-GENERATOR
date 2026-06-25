@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: Cursor Enterprise Framework Generator - Cross-Project Setup
:: Framework Version: 4.1.0
:: ============================================================
:: Installs skills, rules, memory, knowledge, prompts, workflows,
:: and templates into %USERPROFILE%\.cursor\ for cross-project
:: use in Cursor IDE / Claude Code / Windsurf / Cline / Roo Code.
:: ============================================================

set "SOURCE_DIR=%~dp0"
set "USER_CURSOR_HOME=%USERPROFILE%\.cursor"
set "USER_SKILLS=%USERPROFILE%\.cursor\skills"
set "USER_RULES=%USERPROFILE%\.cursor\rules"
set "USER_MEMORY=%USERPROFILE%\.cursor\memory"
set "USER_KNOWLEDGE=%USERPROFILE%\.cursor\knowledge"
set "USER_PROMPTS=%USERPROFILE%\.cursor\prompts"
set "USER_WORKFLOWS=%USERPROFILE%\.cursor\workflows"
set "USER_TEMPLATES=%USERPROFILE%\.cursor\templates"

:: Default mode is skip-if-exists; pass --force to overwrite.
set "FORCE=0"
if /i "%1"=="--force" set "FORCE=1"
if /i "%1"=="-f" set "FORCE=1"
set "SKIP_CURSOR_CHECK=0"
if /i "%1"=="--no-cursor-check" set "SKIP_CURSOR_CHECK=1"
if /i "%2"=="--no-cursor-check" set "SKIP_CURSOR_CHECK=1"

:: Normalize trailing backslash
if "%SOURCE_DIR:~-1%"=="\" set "SOURCE_DIR=%SOURCE_DIR:~0,-1%"

echo.
echo ============================================================
echo   Cursor Enterprise Framework v4.1.0 - Cross-Project Setup
echo ============================================================
echo.
echo   Source:        %SOURCE_DIR%
echo   User profile:  %USERPROFILE%
echo   Mode:          %FORCE_MODE%
if %FORCE%==1 (echo   Force mode:    ENABLED - will overwrite existing) else (echo   Force mode:    disabled - use --force to overwrite)
echo.

:: ----------------------------------------------------------
:: Step 1: Detect if Cursor is running
:: ----------------------------------------------------------
echo [1/8] Checking for running Cursor instances...

if %SKIP_CURSOR_CHECK%==1 (
    echo   SKIPPED ^(--no-cursor-check^).
    echo   OK.
) else (
    tasklist /fi "imagename eq Cursor.exe" /nh 2>nul | findstr /i "Cursor.exe" >nul
    if !errorlevel! equ 0 (
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
)

:: ----------------------------------------------------------
:: Step 2: Create destination directories
:: ----------------------------------------------------------
echo.
echo [2/8] Creating destination directories...

for %%D in ("%USER_SKILLS%" "%USER_RULES%" "%USER_MEMORY%" "%USER_KNOWLEDGE%" "%USER_PROMPTS%" "%USER_WORKFLOWS%" "%USER_TEMPLATES%") do (
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
echo [3/8] Syncing skills to ~/.cursor/skills/...

set "SKILLS_SOURCE=%SOURCE_DIR%\.cursor\skills"
if not exist "%SKILLS_SOURCE%" (
    echo   No skills directory found at source. Skipping.
) else (
    set COPIED=0
    set SKIPPED=0

    for /d %%S in ("%SKILLS_SOURCE%\*") do (
        set "SKILL_NAME=%%~nxS"
        set "DEST=%USER_SKILLS%\!SKILL_NAME!"
        call :sync_skill_dir "%%S" "!SKILL_NAME!" "!DEST!"
    )

    :: Also copy top-level .mdc skills (single-file skills)
    for %%S in ("%SKILLS_SOURCE%\*.mdc") do (
        set "SKILL_NAME=%%~nxS"
        set "DEST=%USER_SKILLS%\!SKILL_NAME!"
        call :sync_skill_file "%%S" "!SKILL_NAME!" "!DEST!"
    )

    echo.
    echo   Installed: !COPIED! skill^(s^)
    if !SKIPPED! gtr 0 echo   Skipped:  !SKIPPED! skill^(s^) (use --force to overwrite)
)

goto :after_step3

:sync_skill_dir
:: %~1 = source, %~2 = name, %~3 = dest
if "%~2"=="reverse-skill" goto :sync_skill_specialized
if exist "%~3" goto :sync_skill_exists
robocopy "%~1" "%~3" /E /NFL /NDL /NJH /NJS /NC /NS >nul 2>&1
if exist "%~3\SKILL.md" (
    echo   %~2  - installed
    set /a COPIED+=1
) else (
    echo   %~2  - SKILL.md not found, skipping
)
goto :eof

:sync_skill_specialized
echo   %~2  - skipped (specialized package, opt-in)
goto :eof

:sync_skill_exists
if %FORCE%==1 (
    robocopy "%~1" "%~3" /E /NFL /NDL /NJH /NJS /NC /NS >nul 2>&1
    if exist "%~3\SKILL.md" (
        echo   %~2  - updated
        set /a COPIED+=1
    ) else (
        echo   %~2  - SKILL.md not found, skipping
    )
) else (
    echo   %~2  - already exists (use --force to overwrite)
    set /a SKIPPED+=1
)
goto :eof

:sync_skill_file
:: %~1 = source file, %~2 = name, %~3 = dest file
if exist "%~3" goto :sync_skill_file_exists
copy /Y "%~1" "%~3" >nul 2>&1
echo   %~2  - installed
set /a COPIED+=1
goto :eof

:sync_skill_file_exists
if %FORCE%==1 (
    copy /Y "%~1" "%~3" >nul 2>&1
    echo   %~2  - updated
    set /a COPIED+=1
) else (
    set /a SKIPPED+=1
)
goto :eof

:after_step3

:: ----------------------------------------------------------
:: Step 4: Sync rules (cross-project reusable)
::    Source:      .cursor\rules\
::    Destination: %USERPROFILE%\.cursor\rules\
:: ----------------------------------------------------------
echo.
echo [4/8] Syncing rules to ~/.cursor/rules/...

set "RULES_SOURCE=%SOURCE_DIR%\.cursor\rules"
if not exist "%RULES_SOURCE%" (
    echo   No rules directory found at source. Skipping.
) else (
    set COPIED_RULES=0
    set SKIPPED_RULES=0

    for %%R in ("%RULES_SOURCE%\*.mdc") do (
        set "RULE_NAME=%%~nxR"
        set "DEST=%USER_RULES%\!RULE_NAME!"
        call :sync_rule "%%R" "!RULE_NAME!" "!DEST!"
    )

    echo.
    echo   Installed: !COPIED_RULES! rule^(s^)
    if !SKIPPED_RULES! gtr 0 echo   Skipped:  !SKIPPED_RULES! rule^(s^) (use --force to overwrite)
)

goto :after_step4

:sync_rule
:: %~1 = source file, %~2 = name, %~3 = dest file
if exist "%~3" goto :sync_rule_exists
copy /Y "%~1" "%~3" >nul 2>&1
if !errorlevel! equ 0 (
    echo   %~2  - installed
    set /a COPIED_RULES+=1
) else (
    echo   %~2  - FAILED
)
goto :eof

:sync_rule_exists
if %FORCE%==1 (
    copy /Y "%~1" "%~3" >nul 2>&1
    echo   %~2  - updated
    set /a COPIED_RULES+=1
) else (
    set /a SKIPPED_RULES+=1
)
goto :eof

:after_step4

:: ----------------------------------------------------------
:: Step 5: Sync memory files (cross-project context)
::    Source:      .cursor\memory\*.md
::    Destination: %USERPROFILE%\.cursor\memory\*.md
:: ----------------------------------------------------------
echo.
echo [5/8] Syncing memory files to ~/.cursor/memory/...

set "MEMORY_SOURCE=%SOURCE_DIR%\.cursor\memory"
if not exist "%MEMORY_SOURCE%" (
    echo   No memory directory found at source. Skipping.
) else (
    set COPIED_MEM=0
    set SKIPPED_MEM=0
    for %%M in ("%MEMORY_SOURCE%\*.md") do (
        set "MEM_NAME=%%~nxM"
        set "DEST=%USER_MEMORY%\!MEM_NAME!"
        call :sync_memory_md "%%M" "!MEM_NAME!" "!DEST!"
    )
    if !COPIED_MEM! equ 0 (
        if !SKIPPED_MEM! gtr 0 (
            echo   Skipped: !SKIPPED_MEM! memory file^(s^) already exist
        ) else (
            echo   No memory files to sync.
        )
    ) else (
        echo   Installed: !COPIED_MEM! memory file^(s^)
    )

    :: Also copy technology-stack.json (the only valid JSON memory file)
    if exist "%MEMORY_SOURCE%\technology-stack.json" (
        if not exist "%USER_MEMORY%\technology-stack.json" (
            copy /Y "%MEMORY_SOURCE%\technology-stack.json" "%USER_MEMORY%\" >nul 2>&1
            echo   technology-stack.json  - installed
        ) else (
            if %FORCE%==1 (
                copy /Y "%MEMORY_SOURCE%\technology-stack.json" "%USER_MEMORY%\" >nul 2>&1
                echo   technology-stack.json  - updated
            )
        )
    )

    :: Create subdirectories for SQLite DBs (session-summary, decision-history, bug-history, architecture-history, schema)
    set "MEM_SUBDIRS=session-summary decision-history bug-history architecture-history schema"
    for %%D in (%MEM_SUBDIRS%) do (
        if not exist "%USER_MEMORY%\%%D" (
            mkdir "%USER_MEMORY%\%%D" 2>nul
        )
    )
)

goto :after_step5

:sync_memory_md
:: %~1 = source, %~2 = name, %~3 = dest
if exist "%~3" goto :sync_memory_md_exists
copy /Y "%~1" "%~3" >nul 2>&1
if !errorlevel! equ 0 (
    echo   %~2  - installed
    set /a COPIED_MEM+=1
)
goto :eof

:sync_memory_md_exists
if %FORCE%==1 (
    copy /Y "%~1" "%~3" >nul 2>&1
    echo   %~2  - updated
    set /a COPIED_MEM+=1
) else (
    set /a SKIPPED_MEM+=1
)
goto :eof

:after_step5

:: ----------------------------------------------------------
:: Step 6: Sync knowledge base (optional, large)
::    Source:      .cursor\knowledge\
::    Destination: %USERPROFILE%\.cursor\knowledge\
:: ----------------------------------------------------------
echo.
echo [6/8] Syncing knowledge base to ~/.cursor/knowledge/...

set "KNOWLEDGE_SOURCE=%SOURCE_DIR%\.cursor\knowledge"
if not exist "%KNOWLEDGE_SOURCE%" (
    echo   No knowledge directory found at source. Skipping.
) else (
    set COPIED_K=0
    set SKIPPED_K=0

    :: Per-domain directory copy (preserves structure)
    for /d %%K in ("%KNOWLEDGE_SOURCE%\*") do (
        set "DOMAIN=%%~nxK"
        set "DEST=%USER_KNOWLEDGE%\!DOMAIN!"
        set "K_SRC=%%K"
        call :sync_knowledge_domain "%%K" "!DOMAIN!" "!DEST!"
    )

    echo.
    echo   Installed: !COPIED_K! knowledge domain^(s^)
    if !SKIPPED_K! gtr 0 echo   Skipped:  !SKIPPED_K! knowledge domain^(s^) (use --force to overwrite)
)

goto :after_step6

:sync_knowledge_domain
:: %~1 = source path, %~2 = domain name, %~3 = dest path
:: Use ~ to strip surrounding quotes
if "%~2"=="reverse-routing" goto :sync_k_specialized
if exist "%~3" goto :sync_k_exists
robocopy "%~1" "%~3" /E /NFL /NDL /NJH /NJS /NC /NS >nul 2>&1
echo   %~2  - installed
set /a COPIED_K+=1
goto :eof

:sync_k_specialized
echo   %~2  - skipped (specialized knowledge)
goto :eof

:sync_k_exists
if %FORCE%==1 (
    robocopy "%~1" "%~3" /E /NFL /NDL /NJH /NJS /NC /NS >nul 2>&1
    echo   %~2  - updated
    set /a COPIED_K+=1
) else (
    set /a SKIPPED_K+=1
)
goto :eof

:after_step6

:: ----------------------------------------------------------
:: Step 7: Sync prompts + workflows + templates
::    Sources:     .cursor\prompts\, .cursor\workflows\, .cursor\templates\
::    Destinations: corresponding ~/.cursor/ subdirs
:: ----------------------------------------------------------
echo.
echo [7/8] Syncing prompts, workflows, and templates...

:: 7a. Prompts
set "PROMPTS_SOURCE=%SOURCE_DIR%\.cursor\prompts"
if exist "%PROMPTS_SOURCE%" (
    set COPIED_P=0
    set SKIPPED_P=0
    for %%P in ("%PROMPTS_SOURCE%\*.prompt.md") do (
        set "P_NAME=%%~nxP"
        set "DEST=%USER_PROMPTS%\!P_NAME!"
        call :sync_simple "%%P" "!DEST!" COPIED_P SKIPPED_P
    )
    echo   Prompts:    installed !COPIED_P!  skipped !SKIPPED_P!
) else (
    echo   Prompts:    source not found, skipping
)

:: 7b. Workflows
set "WORKFLOWS_SOURCE=%SOURCE_DIR%\.cursor\workflows"
if exist "%WORKFLOWS_SOURCE%" (
    set COPIED_W=0
    set SKIPPED_W=0
    for %%W in ("%WORKFLOWS_SOURCE%\*.md") do (
        set "W_NAME=%%~nxW"
        set "DEST=%USER_WORKFLOWS%\!W_NAME!"
        call :sync_simple "%%W" "!DEST!" COPIED_W SKIPPED_W
    )
    echo   Workflows:  installed !COPIED_W!  skipped !SKIPPED_W!
) else (
    echo   Workflows:  source not found, skipping
)

:: 7c. Templates
set "TEMPLATES_SOURCE=%SOURCE_DIR%\.cursor\templates"
if exist "%TEMPLATES_SOURCE%" (
    set COPIED_T=0
    set SKIPPED_T=0
    for %%T in ("%TEMPLATES_SOURCE%\*.md") do (
        set "T_NAME=%%~nxT"
        set "DEST=%USER_TEMPLATES%\!T_NAME!"
        call :sync_simple "%%T" "!DEST!" COPIED_T SKIPPED_T
    )
    echo   Templates:  installed !COPIED_T!  skipped !SKIPPED_T!
) else (
    echo   Templates:  source not found, skipping
)

:: ----------------------------------------------------------
:: Step 8: Optional - copy framework scripts (PowerShell)
::    Source:      .cursor\scripts\
::    Destination: %USERPROFILE%\.cursor\scripts\
:: ----------------------------------------------------------
echo.
echo [8/8] Syncing automation scripts to ~/.cursor/scripts/...

set "SCRIPTS_SOURCE=%SOURCE_DIR%\.cursor\scripts"
if not exist "%SCRIPTS_SOURCE%" (
    echo   No scripts directory found at source. Skipping.
) else (
    set "SCRIPTS_TARGET=!USER_CURSOR_HOME!\scripts"
    if not exist "!SCRIPTS_TARGET!" mkdir "!SCRIPTS_TARGET!" 2>nul

    set COPIED_S=0
    set SKIPPED_S=0
    :: Use dir /b /s to enumerate scripts (more reliable than for /r with delayed expansion)
    for /f "delims=" %%S in ('dir /b /s /a-d "%SCRIPTS_SOURCE%\*.ps1" 2^>nul') do (
        set "S_FULL=%%S"
        set "S_DEST=!SCRIPTS_TARGET!\!S_FULL:%SCRIPTS_SOURCE%\=!"
        for %%F in ("!S_DEST!") do set "S_DIR=%%~dpF"
        if not exist "!S_DIR!" mkdir "!S_DIR!" 2>nul
        call :sync_simple "%%S" "!S_DEST!" COPIED_S SKIPPED_S
    )
    echo   Installed: !COPIED_S! script^(s^)
    if !SKIPPED_S! gtr 0 echo   Skipped:  !SKIPPED_S! script^(s^)
)

goto :after_step8

:: Generic single-file sync subroutine.
:: %~1 = source file, %~2 = dest file,
:: %3 = name of counter env var for installed, %4 = name of counter env var for skipped
:sync_simple
if exist "%~2" goto :sync_simple_exists
copy /Y "%~1" "%~2" >nul 2>&1
set /a %3+=1
goto :eof

:sync_simple_exists
if %FORCE%==1 (
    copy /Y "%~1" "%~2" >nul 2>&1
    set /a %3+=1
) else (
    set /a %4+=1
)
goto :eof

:after_step8

:: ----------------------------------------------------------
:: Done
:: ----------------------------------------------------------
echo.
echo ============================================================
echo   Setup complete!
echo ============================================================
echo.
echo   Restart Cursor IDE to load the newly installed skills,
echo   rules, memory, knowledge, prompts, workflows, and templates.
echo.
echo   All components are now available globally across all
echo   your Cursor / Claude Code / Windsurf / Cline / Roo Code
echo   projects and workspaces.
echo.
echo   Tip: Run 'setup.bat --force' to overwrite existing
echo        components with the latest versions.
echo.
exit /b 0
