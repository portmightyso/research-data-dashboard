from django.urls import path
from .views import ProjectListAPI, DashboardHome, LoginView, logout_view

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard_home'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('api/projects/', ProjectListAPI.as_view(), name='project_api'),
]