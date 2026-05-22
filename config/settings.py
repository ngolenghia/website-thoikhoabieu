import dj_database_url
import os
from pathlib import Path
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env (chỉ dùng khi chạy local)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- BẢO MẬT ---
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-71r=u61dn4!(7+@wdka=x2dllmfww=r_s!&r22f2*cf*)*^cbl')

# DEBUG: Trên Azure sẽ lấy từ Environment Variables (mặc định False)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Cho phép tất cả host để Azure không chặn request
ALLOWED_HOSTS = ['*']

# Sửa lỗi 403 CSRF khi chạy trên domain của Azure
CSRF_TRUSTED_ORIGINS = [
    'https://vku-timetable-lenghiagroup-f9gsdyaaaghmhzfy.southeastasia-01.azurewebsites.net'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # Hỗ trợ file tĩnh
    'django.contrib.staticfiles',
    'schedule',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Phải nằm ngay sau SecurityMiddleware
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# --- CẤU HÌNH DATABASE (FIX LỖI NO SUCH TABLE) ---
# Nếu chạy trên Azure Linux, SQLite phải nằm trong /home để dữ liệu được lưu vĩnh viễn
if os.environ.get('WEBSITE_HOSTNAME'):
    db_path = os.path.join('/home', 'db.sqlite3')
else:
    db_path = os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{db_path}',
        conn_max_age=600
    )
}

# Password validation - Tắt kiểm tra phức tạp để bạn dễ tạo admin khi test
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# --- FILE TĨNH (CSS, JS, Images) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise phục vụ file tĩnh trên Azure
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL (Lấy từ biến môi trường Azure Configuration)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')

# ĐIỀU HƯỚNG
LOGIN_URL = 'login'
LOGOUT_URL = 'login'
LOGIN_REDIRECT_URL = 'manage'
LOGOUT_REDIRECT_URL = 'login'