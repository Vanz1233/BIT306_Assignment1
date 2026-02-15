# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm

@login_required
def profile_view(request):
    """
    Handles Use Case 5: Manage Profile.
    Allows the logged-in user to update their personal details.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
