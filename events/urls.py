from django.urls import path
from . import views  # Imports views from the current 'events' folder

app_name = 'events'  # Namespacing helps with reverse lookups

urlpatterns = [
    # Pattern: events/<id>/register/
    # Purpose: POST request to register (Topic 3.1 & 3.3)
    path('<int:ngo_id>/register/', views.register_ngo, name='register'),

    # Pattern: events/<id>/cancel/
    # Purpose: POST request to cancel
    path('<int:ngo_id>/cancel/', views.cancel_ngo, name='cancel'),

    # Pattern: events/<id>/ticket/
    # Purpose: GET request to view ticket (Use Case 6)
    path('<int:ngo_id>/ticket/', views.ticket_view, name='ticket'),
]