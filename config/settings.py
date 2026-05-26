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

# DEBUG: Trên Azure mặc định sẽ là False để bảo mật
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Cho phép tất cả host để Azure không chặn request
ALLOWED_HOSTS = ['*']

# --- QUAN TRỌNG: FIX LỖI 403 FORBIDDEN ---
CSRF_TRUSTED_ORIGINS = [
    'https://vku-timetable-lenghiagroup-f9gsdyaaaghmhzfy.southeastasia-01.azurewebsites.net',
    'http://vku-timetable-lenghiagroup-f9gsdyaaaghmhzfy.southeastasia-01.azurewebsites.net'
]

# Ép bảo mật Cookie trên môi trường HTTPS của Azure
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = False  # Đảm bảo dùng Cookie để lưu Token

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

# --- CẤU HÌNH DATABASE ---
# Sử dụng SQLite nằm ngay trong thư mục project để đảm bảo quyền truy cập
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}',
        conn_max_age=600
    )
}

# Password validation - Tắt để dễ tạo admin
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# --- FILE TĨNH (CSS, JS, Images) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise phục vụ file tĩnh
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL
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

# Mở file schedule/views.py
def manage(request):
  
# Chèn dòng này vào ngay sau dòng "def tên_hàm(request):"
loi_chup_anh_bao_cao = "Ket qua la: " + 2026  # TypeError: cộng chuỗi với số
   