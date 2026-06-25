@echo off
chcp 65001 >nul 2>&1
echo.
echo  ÉÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ»
echo  º   CEF Web - Deploy to Vercel              º
echo  ÈÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ¼
echo.

cd /d "%~dp0"

echo [1/3] Checking Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo   [ERROR] Node.js is not installed!
    echo   Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo   [OK] Node.js found

echo.
echo [2/3] Installing dependencies (if needed)...
call npm install --silent 2>nul
if %errorlevel% neq 0 (
    echo   [WARNING] npm install had issues, continuing anyway...
)

echo.
echo [3/3] Building and deploying to Vercel...
echo.
call npm run deploy:prod

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Deployment failed!
    pause
    exit /b 1
)

echo.
echo  ÉÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ»
    echo  º   Deployment completed successfully!   º
    echo  ÈÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ¼
echo.
pause
