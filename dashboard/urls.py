from django.urls import path
from .views import (
    DashboardHome, 
    LoginView, 
    logout_view, 
    ProjectAPI,       # <-- مطمئن شو کامنت نیست
    ExperimentLogAPI
)

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard_home'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    
    path('api/projects/', ProjectAPI.as_view(), name='project_api'), # <-- مطمئن شو کامنت نیست
    path('api/experiments/', ExperimentLogAPI.as_view(), name='experiment_api'),
]