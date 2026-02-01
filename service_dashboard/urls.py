from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/<int:ngo_id>/', views.register_ngo, name='register_ngo'),
]