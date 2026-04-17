import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv() # Loads your OpenRouter key and DB credentials from .env

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-fallback-temp-key")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --- 1. Installed Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Required Packages
    'rest_framework',
    'corsheaders',
    
    # Your App
    'books',
]

# --- 2. Middleware (CORS must be at the top) ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Put this first!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# --- 3. Database (Requirement: MySQL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'book_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password', # Replace with your local password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# --- 4. CORS & REST Framework ---
CORS_ALLOW_ALL_ORIGINS = True  # Set to False and use CORS_ALLOWED_ORIGINS in production

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Change for security later
    ]
}

# --- 5. Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' 
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'