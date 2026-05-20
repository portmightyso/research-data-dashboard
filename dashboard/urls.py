from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    DashboardHome, 
    ProjectAPI,
    ExperimentLogAPI
)

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard_home'),
    
    # مسیرهای احراز هویت با نام‌گذاری دقیق برای حل ارور تملپیت
    path('login/', LoginView.as_view(template_name='login.html'), name='login_view'),
    path('logout/', LogoutView.as_view(next_page='login_view'), name='logout_view'), # این خط دقیقاً ارور را برطرف می‌کند
    
    # مسیرهای API
    path('api/projects/', ProjectAPI.as_view(), name='project_api'),
    path('api/experiments/', ExperimentLogAPI.as_view(), name='experiment_api'),
]