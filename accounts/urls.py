# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # 1. Login Page
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # 2. Logout Action
    # Note: As of Django 5.0+, logout usually requires POST. 
    # We will use the built-in view which handles the logic.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 3. Profile Management (Use Case 5)
    path('profile/', views.profile_view, name='profile'),
]