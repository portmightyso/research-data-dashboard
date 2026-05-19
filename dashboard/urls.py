from django.urls import path
from .views import (
    DashboardHome, 
    LoginView, 
    logout_view, 
    ProjectAPI, 
    ExperimentLogAPI
)

urlpatterns = [
    # صفحه اصلی داشبورد
    path('', DashboardHome.as_view(), name='dashboard_home'),
    
    # احراز هویت و مدیریت جلسات کاربری
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    
    # APIهای فرانت‌آند (Vue.js) برای ارتباط با دیتابیس
    path('api/projects/', ProjectAPI.as_view(), name='project_api'),
    path('api/experiments/', ExperimentLogAPI.as_view(), name='experiment_api'),
]