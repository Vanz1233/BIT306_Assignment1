from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import NGO, Registration
from .services import EventService  # <--- IMPORT THE NEW SERVICE
from django.views.decorators.http import require_POST

def dashboard(request):
    ngos = NGO.objects.all()
    user_registered_ids = []
    if request.user.is_authenticated:
        user_registered_ids = Registration.objects.filter(employee=request.user).values_list('ngo_id', flat=True)

    return render(request, 'service_dashboard/index.html', {
        'ngos': ngos,
        'user_registered_ids': user_registered_ids,
        'now': timezone.now()
    })

@login_required
def register_ngo(request, ngo_id):
    # Delegate logic to the Service Layer (Topic 2.3 - Loose Coupling)
    success, message = EventService.register_employee(request.user, ngo_id)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
        
    return redirect('dashboard')

@login_required
def cancel_ngo(request, ngo_id):
    # Delegate logic to the Service Layer
    success, message = EventService.withdraw_employee(request.user, ngo_id)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
        
    return redirect('dashboard')

@require_POST  # <--- Add this decorator
@login_required
def cancel_ngo(request, ngo_id):
    # Delegate logic to the Service Layer
    success, message = EventService.withdraw_employee(request.user, ngo_id)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
        
    return redirect('dashboard')
