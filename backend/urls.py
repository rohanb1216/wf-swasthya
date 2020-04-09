from django.contrib import admin
from django.urls import path, include
from swasthya.views import swasthya,doctor,patient

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('swasthya.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', swasthya.SignUpView.as_view(), name='signup'),
    path('accounts/signup/doctor/', doctor.DoctorSignUpView.as_view(), name='doctor_signup'),
    path('accounts/signup/patient/', patient.PatientSignUpView.as_view(), name='patient_signup'),

]