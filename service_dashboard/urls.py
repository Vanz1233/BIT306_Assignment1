from django.urls import path, include  # <--- Make sure 'include' is imported!
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # THIS LINE FIXES THE ERROR:
    path('accounts/', include('django.contrib.auth.urls')), 

    # Action Routes
    path('register/<int:ngo_id>/', views.register_ngo, name='register_ngo'),
    path('cancel/<int:ngo_id>/', views.cancel_ngo, name='cancel_ngo'),
]