from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone  # Needed for checking dates
from .models import NGO, Registration

def dashboard(request):
    ngos = NGO.objects.all()
    user_registered_ids = []
    if request.user.is_authenticated:
        user_registered_ids = Registration.objects.filter(employee=request.user).values_list('ngo_id', flat=True)

    return render(request, 'service_dashboard/index.html', {
        'ngos': ngos,
        'user_registered_ids': user_registered_ids,
        'now': timezone.now() # Pass current time to template
    })

@login_required
def register_ngo(request, ngo_id):
    ngo = get_object_or_404(NGO, id=ngo_id)
    
    # Requirement: Check Cut-off Date
    if timezone.now() > ngo.cutoff_date:
        messages.error(request, "Registration for this event has closed.")
        return redirect('dashboard')

    if Registration.objects.filter(employee=request.user, ngo=ngo).exists():
        messages.warning(request, f"You are already registered for {ngo.name}.")
    elif ngo.seats_available() <= 0:
        messages.error(request, f"Sorry, {ngo.name} is full.")
    else:
        Registration.objects.create(employee=request.user, ngo=ngo)
        messages.success(request, f"Successfully registered for {ngo.name}!")
        
    return redirect('dashboard')

@login_required
def cancel_ngo(request, ngo_id):
    ngo = get_object_or_404(NGO, id=ngo_id)
    registration = Registration.objects.filter(employee=request.user, ngo=ngo).first()

    # Requirement: Check Cut-off Date for cancellation too
    if timezone.now() > ngo.cutoff_date:
        messages.error(request, "It is too late to cancel your registration.")
    elif registration:
        registration.delete()
        messages.success(request, f"You have withdrawn from {ngo.name}.")
    else:
        messages.error(request, "You are not registered for this event.")
        
    return redirect('dashboard')
