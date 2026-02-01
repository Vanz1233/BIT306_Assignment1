from django.db import models
from django.contrib.auth.models import User  # We use Django's built-in User for Employees/Admins

class NGO(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    service_type = models.CharField(max_length=100)
    event_date = models.DateField()
    start_time = models.TimeField()
    max_employees = models.PositiveIntegerField(help_text="Maximum number of volunteer slots")
    cutoff_date = models.DateTimeField(help_text="Last date/time for employees to register")
    
    # This helps calculate available slots later for Use Case 2 & 4 [cite: 8, 10]
    def seats_taken(self):
        return self.registration_set.count()

    def seats_available(self):
        return self.max_employees - self.seats_taken()

    def __str__(self):
        return self.name

class Registration(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents an employee from registering for the same NGO twice
        unique_together = ('employee', 'ngo')

    def __str__(self):
        return f"{self.employee.username} - {self.ngo.name}"
