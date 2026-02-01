from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NGO, Registration

def dashboard(request):
    # UC 2: Employees view a list of registered NGO activities 
    ngos = NGO.objects.all()
    
    # We need to know which ones the user already joined to disable the button
    user_registered_ids = []
    if request.user.is_authenticated:
        user_registered_ids = Registration.objects.filter(employee=request.user).values_list('ngo_id', flat=True)

    return render(request, 'service_dashboard/index.html', {
        'ngos': ngos,
        'user_registered_ids': user_registered_ids
    })

@login_required
def register_ngo(request, ngo_id):
    # UC 3: Employees select an activity and register [cite: 9]
    ngo = get_object_or_404(NGO, id=ngo_id)
    
    # Check 1: Is user already registered?
    if Registration.objects.filter(employee=request.user, ngo=ngo).exists():
        messages.warning(request, f"You are already registered for {ngo.name}.")
        
    # Check 2: Are there slots available? (Prevent overbooking) [cite: 9]
    elif ngo.seats_available() <= 0:
        messages.error(request, f"Sorry, {ngo.name} is full.")
        
    else:
        # Success: Create the registration
        Registration.objects.create(employee=request.user, ngo=ngo)
        messages.success(request, f"Successfully registered for {ngo.name}!")
        
    return redirect('dashboard')
