from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard & Notifications (Landing page goes here)
    path('', include('service_dashboard.urls')),
    
    # Event & Booking Logic (Prefixed with 'events/' for clarity)
    path('events/', include('events.urls')),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # admin create notifications
    path('notifications/', include('notifications.urls')),
]

admin.site.site_header = "CSR Connect Enterprise"
admin.site.site_title = "CSR Admin Portal"
admin.site.index_title = "Welcome to CSR Management"