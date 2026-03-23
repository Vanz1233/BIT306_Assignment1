from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator

class NGO(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # NEW: 5.1 Timestamp requirement
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    # NEW: 5.1 Foreign Key mapping linking Activity to NGO
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name='activities')
    
    # Moved from your original NGO model
    service_type = models.CharField(max_length=100)
    event_date = models.DateField()
    start_time = models.TimeField()
    
    # UPDATED: 5.1 Field validation (MinValueValidator)
    max_employees = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Maximum number of volunteer slots"
    )
    cutoff_date = models.DateTimeField(help_text="Last date/time for employees to register")
    
    # NEW: 5.1 Timestamp requirement
    created_at = models.DateTimeField(auto_now_add=True)

    def seats_taken(self):
        return self.registration_set.count()

    def seats_available(self):
        return self.max_employees - self.seats_taken()

    def __str__(self):
        return f"{self.service_type} at {self.ngo.name}"
        
    class Meta:
        verbose_name = 'Activity'          
        verbose_name_plural = 'Activities'  

class Registration(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # UPDATED: Registration now links to the Activity, not the NGO directly
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    
    # UPDATED: Renamed from 'registered_at' to 'created_at' to strictly match 5.1 wording
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents an employee from registering for the same activity twice
        unique_together = ('employee', 'activity')

    def __str__(self):
        return f"{self.employee.username} - {self.activity.service_type}"
    

