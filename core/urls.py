from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')), # وصل کردن آدرس‌های داشبورد به روت اصلی سایت
]