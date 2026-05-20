"""
Django settings for config project.
"""
import dj_database_url
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv() 

# Build paths 
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-fallback-key')

# ĐỂ DEBUG = FALSE KHI CHẠY TRÊN AZURE
DEBUG = False


ALLOWED_HOSTS = ['vku-timetable-lenghiagroup-f9gsdyaaaghmhzfy.southeastasia-01.azurewebsites.net', '127.0.0.1', 'localhost']

# --- SỬA LỖI 403 TRÊN AZURE ---
CSRF_TRUSTED_ORIGINS = ['https://vku-timetable-lenghiagroup-f9gsdyaaaghmhzfy.southeastasia-01.azurewebsites.net']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME) 


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'schedule',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Giúp phục vụ file giao diện
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True


# --- CẤU HÌNH FILE GIAO DIỆN (STATIC) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# SỬA DÒNG NÀY ĐỂ HIỆN GIAO DIỆN ADMIN CHUẨN ĐÉT
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- EMAIL ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')
DEFAULT_FROM_EMAIL = 'Hệ thống Lịch học VKU <noreply@vku.udn.vn>'

# --- ĐIỀU HƯỚNG ---
LOGIN_URL = 'login'
LOGOUT_URL = 'login'
LOGIN_REDIRECT_URL = 'home' 
LOGOUT_REDIRECT_URL = 'login'