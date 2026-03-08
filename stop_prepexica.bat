@echo off
title LexClerk - Stop Perplexica
color 0c
echo =============================================
echo     Stopping Perplexica
echo =============================================
echo.

docker stop perplexica

if %errorlevel% equ 0 (
    echo ✅ Perplexica stopped successfully.
) else (
    echo No running Perplexica container found.
)

echo.
pause