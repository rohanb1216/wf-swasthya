from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from swasthya.models import User,Patient,Doctor, Appointment,MedicalRecords

slots = (
    ('slot1', '10:00 AM - 10:30 AM'),
    ('slot2', '10:30 AM - 11:00 AM'),
    ('slot3', '11:00 AM - 11:30 AM'),
    ('slot4', '11:30 PM - 12:00 PM'),
    ('slot5', '13:00 PM - 13:30 PM'),
    ('slot6', '13:30 PM - 14:00 PM'),
    ('slot7', '14:00 PM - 14:30 PM')
)

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


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class BookingFormInit(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor','date')
        widgets = {
            'date': DateInput(),
        }
        #fields = ('name','contact','email','gender','qualification','specialisation','location')

class BookingFormFinal(forms.Form):
    slots = forms.ChoiceField(choices=slots, widget=forms.RadioSelect)
        
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

class DateForm(forms.Form):
            start=  forms.DateField(widget=DateInput)
            end =  forms.DateField(widget=DateInput) 

class MedicalRecordUploadForm(forms.ModelForm):
    class Meta:
        model=MedicalRecords
        fields=('record','title')