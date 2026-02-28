from django.shortcuts import render, get_object_or_404, redirect  
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import NGO, Registration
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.contrib import messages, admin  
from .services import EventService   
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# --- Helper Check ---
def is_admin(user):
    return user.is_superuser or user.is_staff

# --- Main Views ---
def dashboard(request):
    """
    The main landing page. 
    It aggregates data but doesn't handle the 'heavy lifting' of registration logic.
    """
    ngos = NGO.objects.all()
    user_registered_ids = []
    
    if request.user.is_authenticated:
        # Get list of IDs so template knows which buttons to show (Register vs Withdraw)
        user_registered_ids = Registration.objects.filter(employee=request.user).values_list('ngo_id', flat=True)

    return render(request, 'service_dashboard/index.html', {
        'ngos': ngos,
        'user_registered_ids': user_registered_ids,
        'now': timezone.now()
    })

# --- Admin Views ---
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # 1. Grab native Django context 
    # (Because of our global fix in admin.py, this will now AUTOMATICALLY include CSR Operations!)
    context = admin.site.each_context(request)
    app_list = admin.site.get_app_list(request)
            
    context['available_apps'] = app_list
    
    # 2. Add our custom stats
    total_users = User.objects.count()
    total_events = NGO.objects.count()
    
    active_events_count = NGO.objects.annotate(
        booked_count=Count('registration')
    ).filter(
        booked_count__lt=F('max_employees'), 
        cutoff_date__gt=timezone.now()
    ).count()

    upcoming_events = NGO.objects.filter(
        event_date__gte=timezone.now()
    ).order_by('event_date')[:5]

    # 3. Merge them together
    context.update({
        'total_users': total_users,
        'total_events': total_events,
        'active_events': active_events_count,
        'upcoming_events': upcoming_events,
    })
    
    return render(request, 'service_dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def scanner_prototype(request):
    """Admin view to simulate scanning a QR code (Use Case 6)"""
    
    # 1. Grab the custom AuraIT branding we set in urls.py
    context = admin.site.each_context(request)

    if request.method == 'POST':
        # Grab the fake name typed in for the prototype test
        attendee = request.POST.get('attendee_name')
        messages.success(request, f"SCAN SUCCESS: {attendee} has been successfully checked in!")
        return redirect('scanner_prototype') # Or whatever your URL name is
        
    # 2. Pass the context to the template so the header updates!
    return render(request, 'service_dashboard/scanner.html', context)

# --- Employee Ticket View ---
@login_required
def view_ticket(request, event_id):
    """Employee view to see their own QR code ticket (Use Case 6)"""
    event = get_object_or_404(NGO, id=event_id)
    
    context = {
        'event': event,
        'user': request.user
    }
    return render(request, 'service_dashboard/ticket.html', context)

@login_required
def register_event(request, ngo_id):
    if request.method == 'POST':
        # Delegate to Service Layer
        success, message = EventService.register_employee(request.user, ngo_id)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
            
    return redirect('dashboard')

@require_http_methods(["DELETE"]) # <-- This is what fixes the 405 error!
@login_required
def cancel_registration(request, ngo_id):
    """
    Topic 3.1d: Uses proper DELETE HTTP method for cancellations.
    """
    # Delegate to Service Layer
    success, message = EventService.withdraw_employee(request.user, ngo_id)
    
    if success:
        return JsonResponse({"status": "success", "message": message})
    else:
        return JsonResponse({"status": "error", "message": message}, status=400)

@login_required
def smart_login_redirect(request):
    """
    Acts as a traffic cop after login.
    Admins go to the custom dashboard, regular employees go to the homepage.
    """
    if request.user.is_superuser or request.user.is_staff:
        # Send admins to our custom hijacked /admin/ URL
        return redirect('/admin/')
    else:
        # Send normal employees to the event browsing page
        return redirect('/')




