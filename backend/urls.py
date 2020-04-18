from django.contrib import admin
from django.urls import path, include
from swasthya.views import swasthya,doctor,patient
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('swasthya.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', swasthya.SignUpView.as_view(), name='signup'),
    path('accounts/signup/doctor/', doctor.doctor_signup, name='doctor_signup'),
    path('accounts/signup/patient/', patient.patient_signup, name='patient_signup'),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)