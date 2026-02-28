from .models import Notification

def unread_notifications(request):
    """
    Globally injects the unread notification count into all templates.
    """
    if request.user.is_authenticated:
        # Count only notifications for this user that haven't been read
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_notif_count': count}
    
    # If the user isn't logged in, return 0
    return {'unread_notif_count': 0}