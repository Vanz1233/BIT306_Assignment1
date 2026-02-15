from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
# IMPORTANT: Adjust these imports based on where you put your models!
# If models are still in service_dashboard, import from there.
# If you moved models to this app, use .models
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

@require_POST 
@login_required
def cancel_ngo(request, ngo_id):
    """
    Handles the logic for withdrawing a user from an event.
    """
    # Delegate logic to the Service Layer
    success, message = EventService.withdraw_employee(request.user, ngo_id)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
        
    return redirect('dashboard')

@login_required
def ticket_view(request, ngo_id):
    """
    Prototype for Use Case 6: QR Code Check-in
    Located here because it relates to a specific Event (NGO).
    """
    try:
        ngo = NGO.objects.get(id=ngo_id)
        # Check if user is actually registered
        if not Registration.objects.filter(employee=request.user, ngo=ngo).exists():
            messages.error(request, "You do not have a ticket for this event.")
            return redirect('dashboard')
            
        return render(request, 'service_dashboard/ticket.html', {
            'ngo': ngo,
            'user': request.user
        })
    except NGO.DoesNotExist:
        return redirect('dashboard')
