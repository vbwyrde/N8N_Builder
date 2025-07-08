@echo off
REM Quick stop batch file for n8n + Stable URL Proxy

echo Stopping n8n + Stable URL Proxy services...
cd /d "%~dp0"

REM Run the PowerShell script
powershell -ExecutionPolicy Bypass -File "Stop-N8N-Stable-Fixed.ps1"

echo.
echo Press any key to exit...
pause >nul
