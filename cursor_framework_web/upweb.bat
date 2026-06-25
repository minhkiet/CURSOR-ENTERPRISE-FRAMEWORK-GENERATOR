@echo off
echo ================================================
echo CEF Landing Vue App - Deploy to Vercel
echo ================================================
echo.

cd /d "%~dp0"

echo Checking Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo Step 1: Building production...
echo.

call npm run build

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Deploying to Vercel...
echo.

where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    call npm install -g vercel
)

echo.
echo Running vercel deploy...
vercel --prod

echo.
echo ================================================
echo Deployment process completed!
echo ================================================
echo.

pause
