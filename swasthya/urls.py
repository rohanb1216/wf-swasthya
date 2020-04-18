from django.contrib import admin
from django.urls import path, include
from swasthya.views import swasthya,doctor,patient

urlpatterns = [
    path('', swasthya.home, name='home'),
    path('patient/', patient.p_home, name='p_home'),
    path('doctor/', doctor.d_home, name='d_home'),
    path('patient/book', patient.bookAppointment, name='book'),
    path('patient/view', patient.ViewAppointment, name='view'),
    path('doctor_list', patient.doctor_list, name='doctor_list'),
    path('patient/doctor_detail/<name>', patient.doctor_detail,name="doctor_detail"),
    #path('doctor_list', patient.doctor_list_form, name='doctor_list'),
    #path('doctor_list',patient.DoctorListView.as_view(), name='doctor_list'),
    path('patient/change_password', patient.change_password_patient, name='change_password_patient'),
    path('patient/profile_edit', patient.profile_edit_patient, name='profile_edit_patient'),
    path('patient/profile_view', patient.profile_view_patient, name='profile_view_patient'),
    path('patient/add_medical_record', patient.add_medical_record, name='add_medical_record'),
    path('patient/view_medical_records', patient.view_medical_records, name='view_medical_records'),
    path('doctor/change_password', doctor.change_password, name='change_password'),
    path('doctor/profile_edit', doctor.profile_edit, name='profile_edit'),
    path('doctor/profile_view', doctor.profile_view, name='profile_view'),
    path('doctor/view_appointments', doctor.view_appointments, name='view_appointments'),
    path('doctor/view_patients', doctor.view_patients, name='view_patients'),
    path('doctor/patient_detail/<name>', doctor.patient_detail,name="patient_detail"),

]