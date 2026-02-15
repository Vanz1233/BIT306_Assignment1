from django.urls import path
from . import views

urlpatterns = [
    # Landing Page
    path('', views.dashboard, name='dashboard'),
    
    path('notifications/', views.notifications_view, name='notifications'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin-dashboard/scanner/', views.scanner_prototype, name='scanner_prototype'),
    
    path('ticket/<int:event_id>/', views.view_ticket, name='view_ticket'),

    path('register/<int:ngo_id>/', views.register_event, name='register'),

    path('cancel/<int:ngo_id>/', views.cancel_registration, name='cancel'),
]

