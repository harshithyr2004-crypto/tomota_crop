@echo off
title TomatoGuard AI - Two-Stage Crop Health & Disease Portal
echo Starting TomatoGuard AI Backend and Frontend...
cd /d "%~dp0"
if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" "run_app.py"
) else (
    python "run_app.py"
)
pause
