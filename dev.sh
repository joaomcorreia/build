#!/bin/bash
# Development server shortcut for Build Platform (Linux/Mac)
# Usage: ./dev.sh [command] [args...]

cd "$(dirname "$0")"

PYTHON_CMD="C:/projects/build/build/.venv/Scripts/python.exe"
SETTINGS="--settings=build_project.settings_dev"

if [ $# -eq 0 ]; then
    echo "🚀 Starting Django development server..."
    $PYTHON_CMD manage.py runserver 8000 $SETTINGS
elif [ "$1" = "shell" ]; then
    echo "🐍 Starting Django shell..."
    $PYTHON_CMD manage.py shell $SETTINGS
elif [ "$1" = "migrate" ]; then
    echo "📊 Running migrations..."
    $PYTHON_CMD manage.py migrate $SETTINGS
elif [ "$1" = "makemigrations" ]; then
    echo "🛠️ Creating migrations..."
    $PYTHON_CMD manage.py makemigrations $SETTINGS
elif [ "$1" = "createsuperuser" ]; then
    echo "👤 Creating admin user..."
    $PYTHON_CMD manage.py create_email_admin $SETTINGS
elif [ "$1" = "collectstatic" ]; then
    echo "📁 Collecting static files..."
    $PYTHON_CMD manage.py collectstatic --noinput $SETTINGS
else
    echo "🔧 Running custom command: $*"
    $PYTHON_CMD manage.py "$@" $SETTINGS
fi

echo ""
echo "💡 Available shortcuts:"
echo "   ./dev.sh                  - Start development server"
echo "   ./dev.sh shell           - Django shell"
echo "   ./dev.sh migrate         - Run migrations"
echo "   ./dev.sh makemigrations  - Create migrations"
echo "   ./dev.sh createsuperuser - Create admin user"
echo "   ./dev.sh collectstatic   - Collect static files"
echo "   ./dev.sh [any_command]   - Run any Django command"