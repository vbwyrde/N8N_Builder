@echo off
REM Emergency shutdown script for N8N_Builder system
REM This script forcefully terminates all N8N_Builder related processes
REM To run this from PowerShell, use: & '.\shutdown.bat'

echo ========================================
echo N8N_Builder Emergency Shutdown
echo ========================================
echo To run this from PowerShell, use:  PS C:\Users\mabramsR\source\Cursor_Workspaces\N8N_Builder>.\Shutdown.bat
echo.

echo [INFO] Stopping N8N_Builder processes...

REM Kill Python processes running run.py
echo [INFO] Terminating run.py processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *run.py*" 2>nul
taskkill /F /IM python.exe /FI "COMMANDLINE eq *run.py*" 2>nul

REM Kill processes by port (N8N_Builder typically uses 8002, 8003, 8081)
echo [INFO] Freeing ports 8002, 8003, 8081...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8002') do (
    echo Killing process %%a on port 8002
    taskkill /F /PID %%a 2>nul
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8003') do (
    echo Killing process %%a on port 8003
    taskkill /F /PID %%a 2>nul
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8081') do (
    echo Killing process %%a on port 8081
    taskkill /F /PID %%a 2>nul
)

REM Kill any uvicorn processes
echo [INFO] Terminating uvicorn processes...
taskkill /F /IM python.exe /FI "COMMANDLINE eq *uvicorn*" 2>nul

REM Kill any FastAPI processes
echo [INFO] Terminating FastAPI processes...
taskkill /F /IM python.exe /FI "COMMANDLINE eq *fastapi*" 2>nul

REM Kill any Self-Healer dashboard processes
echo [INFO] Terminating Self-Healer dashboard processes...
taskkill /F /IM python.exe /FI "COMMANDLINE eq *dashboard*" 2>nul

echo.
echo [SUCCESS] Emergency shutdown complete!
echo [INFO] All N8N_Builder processes have been terminated.
echo [INFO] You can now safely restart the system with: python run.py
echo.

pause
