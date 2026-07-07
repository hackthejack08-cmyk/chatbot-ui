@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-bytebot.ps1"
echo.
echo If the browser did not open, visit:
echo http://127.0.0.1:8028/chat.html
echo.
pause
