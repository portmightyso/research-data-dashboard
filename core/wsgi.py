import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()

# ---- تکه کد موقت برای ساخت خودکار اکانت استاد بدون نیاز به Shell ----
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # اینجا یوزرنیم و پسورد دلخواهت برای لاگین استاد را تنظیم کن
    if not User.objects.filter(username='prof_soroush').exists():
        User.objects.create_superuser('prof_soroush', 'prof@university.edu', 'YourSecurePassword123')
        print("=== Superuser created successfully! ===")
except Exception as e:
    print(f"=== Error creating superuser: {e} ===")