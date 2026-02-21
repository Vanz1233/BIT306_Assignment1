from django.contrib import admin
from .models import NGO, Registration
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse

# --- CUSTOM USER ADMIN (Cleans up the cluttered default User page) ---
# Unregister the default User and Group
admin.site.unregister(User)
admin.site.unregister(Group)

class CustomUserAdmin(BaseUserAdmin):
    # This completely hides the massive 'Groups' and 'User permissions' boxes
    fieldsets = (
        ('Account Credentials', {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email')}),
        ('System Roles (Check both for Admin, none for Employee)', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)


# Use Case 1: Administrator manages and monitors availability [cite: 7]
@admin.register(NGO)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'max_employees', 'seats_taken', 'seats_available')

# Use Case 4: Administrator monitors participation [cite: 10]
admin.site.register(Registration)

original_get_app_list = admin.site.get_app_list

def custom_get_app_list(request, app_label=None):
    # Get the standard sidebar list from Django
    app_list = original_get_app_list(request, app_label)
    
    # Only append if Django is building the full sidebar (app_label is None)
    if app_label is None:
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
                },
                {
                    'name': '📢 Broadcasts',
                    'object_name': 'broadcasts',
                    'admin_url': reverse('notifications:admin_panel'),
                    'view_only': True,
                }
            ]
        }
        app_list.append(custom_operations)
        
    return app_list

# Overwrite Django's default behavior with our custom function
admin.site.get_app_list = custom_get_app_list