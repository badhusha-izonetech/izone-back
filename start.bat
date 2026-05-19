@echo off
set "PORT=%PORT%"
if "%PORT%"=="" set "PORT=8000"
echo Starting Izone Technologies Backend API on port %PORT%...
cd /d d:\izonesite\backend
call "%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --port %PORT%
