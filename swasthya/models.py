from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
# from django.core.validators import MinValueValidator

# from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)


gender_list = (('M', 'M'), ('F', 'F'), ('Other', 'Other'))


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='patient_profile')
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    contact = models.CharField(max_length=12)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=gender_list, default='M')

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor_profile')
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=12)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=gender_list, default='M')
    qualification = models.CharField(max_length=250)
    specialisation = models.CharField(max_length=250)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    slot1 = models.CharField(max_length=100, default='', blank=True)
    slot2 = models.CharField(max_length=100, default='', blank=True)
    slot3 = models.CharField(max_length=100, default='', blank=True)
    slot4 = models.CharField(max_length=100, default='', blank=True)
    slot5 = models.CharField(max_length=100, default='', blank=True)
    slot6 = models.CharField(max_length=100, default='', blank=True)
    slot7 = models.CharField(max_length=100, default='', blank=True)
    

class MedicalRecords(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    title= models.CharField(max_length=200, default='Record')
    date = models.DateField(default=datetime.date.today)
    record = models.ImageField(upload_to = 'images/', default = 'images/no-img.png')