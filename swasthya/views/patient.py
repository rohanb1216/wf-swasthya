from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView
from ..models import User, Patient
from ..forms import PatientSignUpForm,PatientDetailsForm

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'registration/signup_form_patient.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('p_home')

def p_home(request):
    return render(request, 'swasthya/patient/patient_home.html')

def patient_signup(request):
    if request.method == 'POST':
        user_form = PatientSignUpForm(request.POST, prefix='UF')
        profile_form = PatientDetailsForm(request.POST, prefix='PF')
        if user_form.is_valid():
            user=user_form.save(commit=False)
            user.is_patient = True
            user.save()
            if profile_form.is_valid():
                patient_profile= profile_form.save(commit=False)
                patient_profile.user=user
                patient_profile.save()
                #return(redirect('p_home'))
                return render(request, 'swasthya/patient/patient_home.html',{
                'user_form': user_form,
                'patient_profile_form': profile_form})
    else:
        user_form = PatientSignUpForm(prefix='UF')
        profile_form = PatientDetailsForm(prefix='PF')
        return render(request, 'swasthya/patient/signup_patient.html',{
            'user_form': user_form,
            'patient_profile_form': profile_form,
        })
