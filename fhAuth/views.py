from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from fhPortal.models import Patient, TestResult
from .forms import CustomUserCreationForm

from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
import logging
logger = logging.getLogger('custom_logger')

@login_required
def index(request):
	patient_list = Patient.objects.filter(user=request.user)
	return render(request, 'fhPortal/index.html', {'patient_list': patient_list})
    #return render(request, 'djVsanCapacity/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            #form.save()
            user = form.save()
            messages.success(request, f"Account created successfully for {user.username}! You can now log in.")
            #user = form.save(commit=False)
            #user.set_password(form.cleaned_data['password'])
            #user.save()
            return redirect('fhAuth:login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")    
    else:
        #form = UserCreationForm()
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
