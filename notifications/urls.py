from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Admin Panel (For sending)
    path('admin-panel/', views.admin_notification_panel, name='admin_panel'),
    
    # User View (For viewing)
    path('my-alerts/', views.user_notifications, name='user_list'),

    path('api/<int:notification_id>/update/', views.mark_notification_read, name='mark_read'),
]