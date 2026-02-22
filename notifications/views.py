from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages, admin  # <-- ADDED 'admin' here
from service_dashboard.models import NGO 
from .models import Notification
from django.contrib.auth.models import User

# Helper: Check if user is admin
def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_notification_panel(request):
    """
    Prototype for Use Case 5: 
    1. Admin sets schedule reminders.
    2. Admin broadcasts messages.
    """
    events = NGO.objects.all()

    # --- NEW: Grab the custom AuraIT branding ---
    context = admin.site.each_context(request)
    context['events'] = events  # Keep your dropdown events working!
    # --------------------------------------------

    if request.method == 'POST':
        # --- Functionality: Broadcast Messages ---
        if 'broadcast' in request.POST:
            event_id = request.POST.get('event_id')

            # Retrieve Data
            title = request.POST.get('subject')
            body = request.POST.get('message')
            
            # Logic: Who gets the message?
            recipients = []
            if event_id == 'all':
                recipients = User.objects.all()
            else:
                # In a real app, filter by users registered for this event
                # For prototype, we'll just send to everyone for now
                recipients = User.objects.all() 

            # Create Database Records
            for user in recipients:
                Notification.objects.create(recipient=user, title=title, message=body)

            messages.success(request, f"Broadcast sent to {len(recipients)} users.")
        
        # --- Functionality: Schedule Reminders ---
        elif 'update_reminders' in request.POST:
            # Captures the toggle states (1 week, 3 days, etc.)
            messages.success(request, "Reminder schedules updated successfully.")
            
        return redirect('notifications:admin_panel')

    # --- CHANGED: Pass the combined context to the HTML ---
    return render(request, 'notifications/admin_panel.html', context)

@login_required
def user_notifications(request):
    """
    Employee View: See their own notifications list
    """
    user_notifs = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications/user_list.html', {'notifications': user_notifs})
