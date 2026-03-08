@echo off
title LexClerk - Start Perplexica
color 0a
echo =============================================
echo     Starting Perplexica for LexClerk v1.2
echo     (Docker - One Click)
echo =============================================
echo.

:: Try to start existing container first
docker start perplexica >nul 2>&1

if %errorlevel% neq 0 (
    echo [First-time setup] Creating and starting Perplexica container...
    docker run -d -p 3000:3000 -v perplexica-data:/home/perplexica/data --name perplexica itzcrazykns1337/perplexica:latest
    echo.
    echo ✅ New container created and started!
) else (
    echo ✅ Perplexica was already created and has been started.
)

echo.
echo 🌐 Perplexica is now running at: http://localhost:3000
echo.
echo First time? Open the link above and finish the quick setup (add your API keys).
echo.
pause