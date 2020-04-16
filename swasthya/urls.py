from django.contrib import admin
from django.urls import path, include
from swasthya.views import swasthya,doctor,patient

urlpatterns = [
    path('', swasthya.home, name='home'),
    path('patient/', patient.p_home, name='p_home'),
    path('doctor/', doctor.d_home, name='d_home'),
    path('patient/book', patient.bookAppointment, name='book'),
    path('patient/view', patient.ViewAppointment, name='view'),
    #path('doctor_list', patient.doctor_list, name='doctor_list')
    path('doctor_list', patient.doctor_list_form, name='doctor_list'),
    #path('doctor_list',patient.DoctorListView.as_view(), name='doctor_list'),
    path('patient/change_password', patient.change_password, name='change_password'),
    path('patient/profile_edit', patient.profile_edit, name='profile_edit'),
    path('patient/profile_view', patient.profile_view, name='profile_view'),
    path('doctor/change_password', doctor.change_password, name='change_password'),
    path('doctor/profile_edit', doctor.profile_edit, name='profile_edit'),
    path('doctor/profile_view', doctor.profile_view, name='profile_view')

]