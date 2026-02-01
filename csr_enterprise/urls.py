from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service_dashboard.urls')), # This makes the dashboard the homepage
]
