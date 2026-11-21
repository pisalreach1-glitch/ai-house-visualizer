@echo off
title Sal AI Studio - Generative AI for Architecture & Interior Design
echo ======================================================================
echo             🏛️  WELCOME TO SAL AI STUDIO (PRO v1.0)
echo      Generative AI Platform for Architects & Interior Designers
echo ======================================================================
echo.
echo [1/2] Starting Sal AI Studio Server on http://localhost:8080 ...
start "" "http://localhost:8080"
python server.py
pause
