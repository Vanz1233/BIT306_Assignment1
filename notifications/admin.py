from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # 1. Expand the table into proper, readable columns! 
    list_display = ('title', 'recipient', 'is_read', 'created_at', 'delete_action')
    
    # 2. Add a clean search bar (searching by the notification title or the recipient's username)
    search_fields = ('title', 'recipient__username')
    
    # 3. Keep the interface completely clean by removing the side filter panel
    list_filter = ()

    # ==========================================
    # CUSTOM INLINE DELETE BUTTON
    # ==========================================
    def delete_action(self, obj):
        # Dynamically grabs the correct delete URL
        delete_url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete", args=[obj.pk])
        
        # Renders the nice Bootstrap danger button
        return format_html(
            '<a class="btn btn-danger btn-sm text-white fw-bold" href="{}">✖ Delete</a>', 
            delete_url
        )
    
    # Renames the column header from "Delete action" to "Actions"
    delete_action.short_description = 'Actions'
