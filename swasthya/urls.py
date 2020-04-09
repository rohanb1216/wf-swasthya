from django.contrib import admin
from django.urls import path, include
from swasthya.views import swasthya,doctor,patient

urlpatterns = [
    path('', swasthya.home, name='home'),
    path('patient/', patient.p_home, name='p_home'),
    path('doctor/', doctor.d_home, name='d_home'),
    

]