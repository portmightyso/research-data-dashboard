from django.urls import path
from .views import (
    DashboardHome, 
    ProjectAPI,
    ExperimentLogAPI
)
from django.contrib.auth.views import LoginView, LogoutView # یا هر ویوی لاگینی که خودت داری

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard_home'),
    path('api/projects/', ProjectAPI.as_view(), name='project_api'),
    path('api/experiments/', ExperimentLogAPI.as_view(), name='experiment_api'),
]