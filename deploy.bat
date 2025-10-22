@echo off
REM Build and Deploy Script for Build Platform (Windows)
REM Usage: deploy.bat [environment]
REM Environments: dev, staging, production

setlocal

set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=dev

echo 🚀 Starting deployment for environment: %ENVIRONMENT%

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ✗ Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Environment-specific configurations
if "%ENVIRONMENT%"=="dev" (
    set COMPOSE_FILE=docker-compose.dev.yml
    echo ✓ Using development configuration
) else if "%ENVIRONMENT%"=="staging" (
    set COMPOSE_FILE=docker-compose.yml
    set DEBUG=False
    echo ✓ Using staging configuration
) else if "%ENVIRONMENT%"=="production" (
    set COMPOSE_FILE=docker-compose.yml
    set DEBUG=False
    echo ✓ Using production configuration
) else (
    echo ✗ Unknown environment: %ENVIRONMENT%
    echo ⚠ Available environments: dev, staging, production
    exit /b 1
)

REM Build and start services
echo ✓ Building Docker images...
docker-compose -f %COMPOSE_FILE% build

echo ✓ Starting services...
docker-compose -f %COMPOSE_FILE% up -d

REM Wait for database to be ready
echo ✓ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Run migrations
echo ✓ Running database migrations...
docker-compose -f %COMPOSE_FILE% exec -T web python manage.py migrate_schemas --shared

REM Create public tenant if it doesn't exist
echo ✓ Setting up public tenant...
docker-compose -f %COMPOSE_FILE% exec -T web python manage.py create_public_tenant --domain=build.justcodeworks.eu 2>nul || echo Public tenant already exists

REM Collect static files (for production)
if not "%ENVIRONMENT%"=="dev" (
    echo ✓ Collecting static files...
    docker-compose -f %COMPOSE_FILE% exec -T web python manage.py collectstatic --noinput
)

REM Show running containers
echo ✓ Deployment complete! Running containers:
docker-compose -f %COMPOSE_FILE% ps

REM Show logs
echo ⚠ Showing recent logs (last 50 lines):
docker-compose -f %COMPOSE_FILE% logs --tail=50

echo ✓ Access the application at:
if "%ENVIRONMENT%"=="dev" (
    echo   🌐 http://localhost:8000
) else (
    echo   🌐 https://build.justcodeworks.eu
)

echo.
echo ⚠ To view logs: docker-compose -f %COMPOSE_FILE% logs -f
echo ⚠ To stop services: docker-compose -f %COMPOSE_FILE% down
echo.
echo ⚠ Don't forget to create a superuser:
echo ⚠ docker-compose -f %COMPOSE_FILE% exec web python manage.py createsuperuser

endlocal