import os
from pathlib import Path

# پیدا کردن مسیر اصلی پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# کلید امنیتی برای محیط لوکال
SECRET_KEY = 'django-insecure-local-development-key-for-research-dashboard'

# فعال کردن وضعیت دباگ برای دیدن دقیق ارورها روی لوکال
DEBUG = True

# هاست‌های مجاز برای سیستم لوکال
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# برنامه‌های فعال در پروژه
INSTALLED_APPS = [
    'dashboard',  # برنامه اصلی داشبورد شما
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# میدل‌ورهای استاندارد جنگو
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# تنظیمات مربوط به قالب‌های HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # خودکار پوشه templates داخل dashboard را شناسایی می‌کند
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

WSGI_APPLICATION = 'core.wsgi.application'


# ==============================================================================
# تنظیمات دیتابیس (لوکال و سریع بدون نیاز به اینترنت نئون)
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# اعتبارسنجی رمز عبور کاربران
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# تنظیمات زبان و زمان پروژه
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# تنظیمات فایل‌های استاتیک (CSS و فایلهای جاوا اسکریپت)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# تنظیمات مدیریت مسیرهای ریدایرکت لاگین و لاگ‌اوت (حل مشکل ۴۰۴ قبلی)
# ==============================================================================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'dashboard_home'  # هدایت مستقیم به صفحه اصلی بعد از لاگین موفق
LOGOUT_REDIRECT_URL = 'login_view'     # هدایت به صفحه لاگین بعد از خروج