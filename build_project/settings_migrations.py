# Migration creation settings - bypasses tenant complications
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'temp-key-for-migrations'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Simple database for migration creation
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Simple middleware
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

# All apps for migration creation
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    # Our apps
    'tenants',
    'accounts',
    'websites',
    'media_library', 
    'ai_tools',
]

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Tenant model
TENANT_MODEL = 'tenants.Client'

# Minimal settings
USE_TZ = True
ROOT_URLCONF = 'build_project.urls_dev'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

print("[MIGRATIONS] Using migration-only settings")