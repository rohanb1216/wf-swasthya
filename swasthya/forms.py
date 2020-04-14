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
        fields = ('name','contact','email','gender','qualification','specialisation','location')

class SearchForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=('specialisation','location')


choices_list = Doctor.objects.order_by().values_list('specialisation').distinct()
# choices=list(choices)
# choices_list=[]
# for i in choices:
#     choices_list.append((i,i))

class SearchForm2(forms.Form):
    specialisation = forms.ModelChoiceField(queryset=Doctor.objects.order_by('specialisation').values_list('specialisation',flat=True).distinct())
    location = forms.ModelChoiceField(queryset=Doctor.objects.order_by('location').values_list('location',flat=True).distinct())
