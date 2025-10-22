@echo off
REM Development server shortcut for Build Platform
REM Usage: dev.bat [command] [args...]

cd /d "%~dp0"

if "%1"=="" (
    echo 🚀 Starting Django development server...
    C:/projects/build/build/.venv/Scripts/python.exe manage.py runserver 8000 --settings=build_project.settings_dev
) else if "%1"=="shell" (
    echo 🐍 Starting Django shell...
    C:/projects/build/build/.venv/Scripts/python.exe manage.py shell --settings=build_project.settings_dev
) else if "%1"=="migrate" (
    echo 📊 Running migrations...
    C:/projects/build/build/.venv/Scripts/python.exe manage.py migrate --settings=build_project.settings_dev
) else if "%1"=="makemigrations" (
    echo 🛠️ Creating migrations...
    C:/projects/build/build/.venv/Scripts/python.exe manage.py makemigrations --settings=build_project.settings_dev
) else if "%1"=="createsuperuser" (
    echo 👤 Creating admin user...
    C:/projects/build/build/.venv/Scripts/python.exe manage.py create_email_admin --settings=build_project.settings_dev
) else if "%1"=="collectstatic" (
    echo 📁 Collecting static files...
    C:/projects/build/build/.venv/Scripts/python.exe manage.py collectstatic --noinput --settings=build_project.settings_dev
) else (
    echo 🔧 Running custom command: %*
    C:/projects/build/build/.venv/Scripts/python.exe manage.py %* --settings=build_project.settings_dev
)

echo.
echo 💡 Available shortcuts:
echo    dev                    - Start development server
echo    dev shell             - Django shell
echo    dev migrate           - Run migrations
echo    dev makemigrations    - Create migrations
echo    dev createsuperuser   - Create admin user
echo    dev collectstatic     - Collect static files
echo    dev [any_command]     - Run any Django command