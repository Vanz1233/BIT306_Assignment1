# events/services.py
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import NGO, Registration

class EventRegistrationService:
    
    @staticmethod
    @transaction.atomic  # Enterprise Feature: Ensures if one database save fails, the whole thing cancels safely!
    def register_employee(employee, ngo_id):
        """
        BUSINESS LOGIC LAYER: Handles the rules for registering a user to an NGO event.
        """
        # 1. Get the NGO event
        try:
            ngo = NGO.objects.get(id=ngo_id)
        except NGO.DoesNotExist:
            raise ValidationError("This NGO event does not exist.")

        # 2. Rule Check: Is the employee already registered?
        if Registration.objects.filter(employee=employee, ngo=ngo).exists():
            raise ValidationError("You are already registered for this event.")

        # 3. Rule Check: Is the event full?
        if ngo.seats_taken >= ngo.max_employees:
            raise ValidationError("This event is fully booked.")

        # 4. Action: Create the registration
        registration = Registration.objects.create(
            employee=employee,
            ngo=ngo
        )

        # 5. Action: Update the available seats
        ngo.seats_taken += 1
        ngo.save()

        return registration