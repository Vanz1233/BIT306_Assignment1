from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse

# IMPORTANT: Adjust these imports based on where you put your models!
from service_dashboard.models import NGO, Registration 
from service_dashboard.services import EventService 

@require_POST 
@login_required
def register_ngo(request, ngo_id):
    """
    Handles the logic for registering a user to an event.
    Moves to 'events' app to separate business logic from the dashboard.
    """
    # Delegate logic to the Service Layer (Topic 2.3 - Loose Coupling)
    success, message = EventService.register_employee(request.user, ngo_id)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
        
    return redirect('dashboard')

# ==========================================
# FIX: RESTful DELETE Endpoint (Topic 3.1d)
# ==========================================
@require_http_methods(["DELETE"]) 
@login_required
def cancel_ngo(request, ngo_id):
    """
    Handles the logic for withdrawing a user from an event.
    Now properly uses the HTTP DELETE method!
    """
    # Delegate logic to the Service Layer
    success, message = EventService.withdraw_employee(request.user, ngo_id)
    
    if success:
        # Add the message to the session so it appears when the JS reloads the page
        messages.success(request, message) 
        return JsonResponse({"status": "success", "message": message})
    else:
        return JsonResponse({"status": "error", "message": message}, status=400)

@login_required
def ticket_view(request, ngo_id):
    """
    Prototype for Use Case 6: QR Code Check-in
    Now fully utilizing the Service Layer for data retrieval.
    """
    # Delegate the database check to the Service Layer
    ngo, is_registered = EventService.get_ticket_verification(request.user, ngo_id)
    
    if not ngo:
        return redirect('dashboard')
        
    if not is_registered:
        messages.error(request, "You do not have a ticket for this event.")
        return redirect('dashboard')
        
    return render(request, 'service_dashboard/ticket.html', {
        'ngo': ngo,
        'user': request.user
    })
