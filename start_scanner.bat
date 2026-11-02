@echo off
title RUTE Trade Scanner & Strategy Tester
cd /d "%~dp0"
echo ===================================================================
echo   Starting RUTE Trade Scanner & Strategy Tester (Pure Local)
echo   Accessible on Laptop: http://localhost:8080
echo ===================================================================
python server.py
pause
