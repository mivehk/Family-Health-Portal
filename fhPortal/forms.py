from django import forms
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        error_messages = {
            'p_first_name': {'required': ''},
            'p_last_name': {'required': ''},
            'p_dob': {'required': ''},
            'p_email': {'required': ''},
            'sex_cat': {'required': ''},
            'blood_type': {'required': ''},
        }
