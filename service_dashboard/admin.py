from django.contrib import admin
from .models import NGO, Registration

# Use Case 1: Administrator manages and monitors availability 
@admin.register(NGO)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'max_employees', 'seats_taken', 'seats_available')

# Use Case 4: Administrator monitors participation [cite: 10]
admin.site.register(Registration)
