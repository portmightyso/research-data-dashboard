from django.urls import path
from .views import (
    DashboardHome, 
    LoginView, 
    logout_view, 
    # ProjectAPI,  # <-- این را فعلاً کامنت کن تا ارور ندهد
    ExperimentLogAPI
)

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard_home'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    
    # اگر کدهای پروژه‌ات قبلاً کار می‌کرده، این مسیر را هم فعلاً کامنت کن:
    # path('api/projects/', ProjectAPI.as_view(), name='project_api'),
    
    path('api/experiments/', ExperimentLogAPI.as_view(), name='experiment_api'),
]