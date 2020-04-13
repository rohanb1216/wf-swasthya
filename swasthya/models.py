from django.contrib.auth.models import AbstractUser
from django.db import models
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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
