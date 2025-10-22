@echo off
REM Quick Django server start
cd /d "%~dp0"
echo 🚀 Starting Build Platform development server...
C:/projects/build/build/.venv/Scripts/python.exe manage.py runserver 8000 --settings=build_project.settings_dev