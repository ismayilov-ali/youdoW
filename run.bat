@echo off
title YouDow Desktop App
python app.py
if %errorlevel% neq 0 (
    echo.
    echo Xeta bas verdi. Zehmet olmasa 'install_requirements.bat' faylini ise salin.
    pause
)

