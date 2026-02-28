from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout  # <-- ADDED THIS
from django.shortcuts import redirect   # <-- ADDED THIS
from service_dashboard.views import admin_dashboard, smart_login_redirect

# ==========================================
# CUSTOM LOGOUT REDIRECT
# ==========================================
def custom_admin_logout(request):
    logout(request)
    return redirect('/')  # <-- Sends you straight to your homepage!

urlpatterns = [
    # 1. The Traffic Cop URL
    path('smart-redirect/', smart_login_redirect, name='smart_redirect'),
    
    # 2. THE NEW ESCAPE HATCH (Must be above the other admin URLs)
    path('admin/logout/', custom_admin_logout, name='custom_admin_logout'),
    
    # This catches the base /admin/ URL and shows your dashboard
    path('admin/', admin_dashboard, name='custom_admin_index'),
    
    # This handles all the other admin magic (login, database tables, etc.)
    path('admin/', admin.site.urls),

    path('', include('events.urls')),
    
    # Dashboard & Notifications (Landing page goes here)
    path('', include('service_dashboard.urls')),
    
    # Event & Booking Logic (Prefixed with 'events/' for clarity)
    path('events/', include('events.urls')),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # admin create notifications
    path('notifications/', include('notifications.urls')),
]

# Admin Panel UI Customizations
admin.site.site_header = "AuraIT Enterprise | CSR Connect"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to AuraIT's CSR Management"