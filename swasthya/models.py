from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

gender_list=(('M','M'),('F','F'),('Other','Other'))

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    contact= models.CharField(max_length=12)
    email= models.EmailField()
    gender = models.CharField(max_length=10,choices = gender_list, default = 'M')

    

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=12)
    email= models.EmailField()
    gender = models.CharField(max_length=10,choices = gender_list, default = 'M')
    qualification = models.CharField(max_length=250)
    specialisation = models.CharField(max_length=250)
    

    def __str__(self):
        return self.user.username