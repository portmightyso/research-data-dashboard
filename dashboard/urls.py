from django.urls import path
# ایمپورت کردن توابع درست بر اساس views.py جدید
from .views import (
    dashboard_view,
    register_view,
    login_view,
    logout_view,
    project_api,
    experiment_log_api
)

urlpatterns = [
    # مسیر اصلی داشبورد تحقیقاتی
    path('', dashboard_view, name='dashboard_view'),
    
    # مسیرهای احراز هویت دپارتمان
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    
    # مسیرهای اتصالات API به فرانت‌آند Vue.js
    path('api/projects/', project_api, name='project_api'),
    path('api/experiments/', experiment_log_api, name='experiment_log_api'),
]