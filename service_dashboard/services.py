from django.utils import timezone
from .models import NGO, Registration

class EventService:
    """
    Handles business logic for Event Registration.
    Separates logic from the View layer (Topic 2.2).
    """

    @staticmethod
    def register_employee(user, ngo_id):
        # 1. Fetch Data
        try:
            ngo = NGO.objects.get(id=ngo_id)
        except NGO.DoesNotExist:
            return False, "Event not found."

        # 2. Rule: Check Cut-off Date (Topic 2.2 - Validation)
        if timezone.now() > ngo.cutoff_date:
            return False, "Registration for this event has closed."

        # 3. Rule: Check Duplicate Registration
        if Registration.objects.filter(employee=user, ngo=ngo).exists():
            return False, f"You are already registered for {ngo.name}."

        # 4. Rule: Check Slot Availability (Topic 2.2 - Availability Checks)
        if ngo.seats_available() <= 0:
            return False, f"Sorry, {ngo.name} is full."

        # 5. Execute Transaction
        Registration.objects.create(employee=user, ngo=ngo)
        return True, f"Successfully registered for {ngo.name}!"

    @staticmethod
    def withdraw_employee(user, ngo_id):
        try:
            ngo = NGO.objects.get(id=ngo_id)
        except NGO.DoesNotExist:
            return False, "Event not found."

        # Rule: Cannot withdraw after cut-off
        if timezone.now() > ngo.cutoff_date:
            return False, "It is too late to cancel your registration."

        registration = Registration.objects.filter(employee=user, ngo=ngo).first()
        if registration:
            registration.delete()
            return True, f"You have withdrawn from {ngo.name}."
        else:
            return False, "You are not registered for this event."