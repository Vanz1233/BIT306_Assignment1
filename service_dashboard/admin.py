from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html  # <-- NEW: Needed for the custom delete button

from .models import NGO, Registration

# ==========================================
# CUSTOM USER ADMIN
# ==========================================
# Unregister the default User and Group
admin.site.unregister(User)
admin.site.unregister(Group)

class CustomUserAdmin(BaseUserAdmin):
    # The profile fields
    fieldsets = (
        ('Admin Profile', {'fields': ('username', 'first_name', 'last_name', 'email')}),
    )
    
    # The table columns
    list_display = ('username', 'first_name', 'last_name', 'email')

    # 1. NEW: This completely removes the 4 dropdown filters!
    list_filter = ()
    
    # 2. NEW: This ensures your search bar stays active
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # 3. Keep this to hide the red delete button
    def has_delete_permission(self, request, obj=None):
        return False

    # 4. Keeps the profile edit page clean without breaking the "Add User" button!
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

admin.site.register(User, CustomUserAdmin)


# ==========================================
# NGO EVENT ADMIN (Use Case 1)
# ==========================================
@admin.register(NGO)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'max_employees', 'seats_taken', 'seats_available')


# ==========================================
# REGISTRATION ADMIN (Use Case 4)
# ==========================================
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    # Dictates what columns show up in the monitoring table, including our new button
    list_display = ('employee', 'ngo', 'delete_action')
    
    # Adds the clean Search bar (Searching by Employee username and NGO name)
    search_fields = ('employee__username', 'ngo__name') 
    
    # Removes that clunky dropdown filter
    list_filter = () 
    
    # 1. Removes the "ADD REGISTRATION" button
    def has_add_permission(self, request):
        return False
        
    # 2. Removes the ability to click into a registration and change it
    def has_change_permission(self, request, obj=None):
        return False

    # ==========================================
    # CUSTOM INLINE DELETE BUTTON
    # ==========================================
    def delete_action(self, obj):
        # Dynamically grabs the correct delete URL for this specific registration
        delete_url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete", args=[obj.pk])
        
        # Renders a neat Bootstrap button right inside the table
        return format_html(
            '<a class="btn btn-danger btn-sm text-white fw-bold" href="{}">Delete</a>', 
            delete_url
        )
    
    # Renames the column header in the table from "Delete action" to "Actions"
    delete_action.short_description = 'Actions'


# ==========================================
# CUSTOM SIDEBAR INJECTION
# ==========================================
original_get_app_list = admin.site.get_app_list

def custom_get_app_list(request, app_label=None):
    # Get the standard sidebar list from Django
    app_list = original_get_app_list(request, app_label)
    
    # Only modify the sidebar if Django is building the full list
    if app_label is None:
        
        # 1. Loop through the existing apps and rename them
        for app in app_list:
            if app['app_label'] == 'auth':
                app['name'] = 'User Management'
                
            elif app['app_label'] == 'service_dashboard':  # Assuming this is your event app name
                app['name'] = 'NGO Management'
                
            elif app['app_label'] == 'notifications':
                app['name'] = 'Broadcasts Management'
                # Move the custom Broadcasts link inside this app's group!
                app['models'].append({
                    'name': '📢 Broadcast Center',
                    'object_name': 'broadcasts',
                    'admin_url': reverse('notifications:admin_panel'),
                    'view_only': True,
                })

        # 2. Add the custom CSR Operations section (Now only containing Scan Ticket)
        custom_operations = {
            'name': 'CSR Operations',
            'app_label': 'csr_operations',
            'app_url': '',
            'has_module_perms': True,
            'models': [
                {
                    'name': '📸 Scan Ticket',
                    'object_name': 'scanner',
                    'admin_url': reverse('scanner_prototype'),
                    'view_only': True,
                }
            ]
        }
        app_list.append(custom_operations)
        
    return app_list

# Overwrite Django's default behavior with our custom function
admin.site.get_app_list = custom_get_app_list