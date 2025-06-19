@echo off
REM Quick stop batch file for n8n + nGrok automation

echo Stopping n8n + nGrok services...
cd /d "%~dp0"

REM Run the PowerShell script
powershell -ExecutionPolicy Bypass -File "Stop-N8N-NgRok.ps1"

echo.
echo Press any key to exit...
pause >nul
