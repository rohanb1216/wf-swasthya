from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from swasthya.models import User,Patient,Doctor


class DoctorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_doctor = True
    #     if commit:
    #         user.save()
    #     return user

class PatientSignUpForm(UserCreationForm): 
    class Meta(UserCreationForm.Meta):
        model = User

    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_patient = True
    #     user.save()
    #     return user

class PatientDetailsForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name','age','contact','email','gender')

class DoctorDetailsForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('name','contact','email','gender','qualification','specialisation')