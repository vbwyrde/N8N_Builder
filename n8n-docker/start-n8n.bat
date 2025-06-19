@echo off
REM Quick start batch file for n8n + nGrok automation

echo Starting n8n + nGrok automation...
cd /d "%~dp0"

REM Check if PowerShell execution policy allows scripts
powershell -Command "Get-ExecutionPolicy" | findstr /i "restricted" >nul
if %errorlevel% equ 0 (
    echo.
    echo WARNING: PowerShell execution policy is Restricted
    echo You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo.
    pause
)

REM Run the PowerShell script
powershell -ExecutionPolicy Bypass -File "Start-N8N-NgRok.ps1"

echo.
echo Press any key to exit...
pause >nul
