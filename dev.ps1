# PowerShell script for Build Platform development
# Usage: .\dev.ps1 [command] [args...]

param(
    [string]$Command = "runserver",
    [string[]]$Args = @()
)

$pythonPath = "C:/projects/build/build/.venv/Scripts/python.exe"
$settings = "--settings=build_project.settings_dev"

Push-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

switch ($Command) {
    "runserver" {
        Write-Host "🚀 Starting Django development server..." -ForegroundColor Green
        & $pythonPath manage.py runserver 8000 $settings
    }
    "shell" {
        Write-Host "🐍 Starting Django shell..." -ForegroundColor Green
        & $pythonPath manage.py shell $settings
    }
    "migrate" {
        Write-Host "📊 Running migrations..." -ForegroundColor Green
        & $pythonPath manage.py migrate $settings
    }
    "makemigrations" {
        Write-Host "🛠️ Creating migrations..." -ForegroundColor Green
        & $pythonPath manage.py makemigrations $settings
    }
    "createsuperuser" {
        Write-Host "👤 Creating admin user..." -ForegroundColor Green
        & $pythonPath manage.py create_email_admin $settings
    }
    "collectstatic" {
        Write-Host "📁 Collecting static files..." -ForegroundColor Green
        & $pythonPath manage.py collectstatic --noinput $settings
    }
    default {
        Write-Host "🔧 Running custom command: $Command $Args" -ForegroundColor Green
        & $pythonPath manage.py $Command @Args $settings
    }
}

Pop-Location

Write-Host ""
Write-Host "💡 Available shortcuts:" -ForegroundColor Yellow
Write-Host "   .\dev.ps1                    - Start development server"
Write-Host "   .\dev.ps1 shell             - Django shell"
Write-Host "   .\dev.ps1 migrate           - Run migrations"
Write-Host "   .\dev.ps1 makemigrations    - Create migrations"
Write-Host "   .\dev.ps1 createsuperuser   - Create admin user"
Write-Host "   .\dev.ps1 collectstatic     - Collect static files"
Write-Host "   .\dev.ps1 [any_command]     - Run any Django command"