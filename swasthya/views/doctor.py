from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from ..forms import DoctorSignUpForm,DoctorDetailsForm,DateForm
from ..models import User, Doctor, Patient, Appointment, MedicalRecords
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('d_home')

def d_home(request):
    return render(request, 'swasthya/doctor/doctor_home.html')

def doctor_signup(request):
    if request.method == 'POST':
        user_form = DoctorSignUpForm(request.POST, prefix='UF')
        profile_form = DoctorDetailsForm(request.POST, prefix='PF')
        print(user_form.errors.as_data())
        print(profile_form.errors.as_data())
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save(commit=False)
            user.is_doctor = True
            user.save()
            doctor_profile= profile_form.save(commit=False)
            doctor_profile.user=user
            doctor_profile.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return(redirect('d_home'))
            #return render(request,'swasthya/doctor/doctor_home.html',{'doctor_profile': doctor_profile})
        else:
            user_form = DoctorSignUpForm(prefix='UF')
            doctor_profile = DoctorDetailsForm(prefix='PF')
            #context['form'] = self.form_class(self.request.POST)
            return render(request, 'swasthya/doctor/signup_doctor.html',{
                'user_form': user_form,
                'doctor_profile': doctor_profile,
            })
    else:
        user_form = DoctorSignUpForm(prefix='UF')
        doctor_profile = DoctorDetailsForm(prefix='PF')
        return render(request, 'swasthya/doctor/signup_doctor.html',{
			'user_form': user_form,
			'doctor_profile': doctor_profile,
		})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('d_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'swasthya/doctor/change_password.html', {
        'form': form
    })

def profile_edit(request):
        user = Doctor.objects.get(user=request.user)
        if(request.method=="POST"):
            form=DoctorDetailsForm(request.POST,instance=user)
            if(form.is_valid()):
                form.save()
                update_session_auth_hash(request, user)
                return(redirect("profile_view"))
        else:
            form=DoctorDetailsForm(instance=user)
            return render (request,'swasthya/doctor/profile_edit.html',{'form':form})  
def profile_view(request):
        doctor = Doctor.objects.get(user=request.user)
        return render (request,'swasthya/doctor/profile_view.html',{'doctor':doctor})

def view_patients(request):
    doctor = Doctor.objects.get(user=request.user)
    patients = Appointment.objects.filter(doctor = doctor)
    return render(request, "swasthya/doctor/view_patients.html", {'patients':patients})

def patient_detail(request,name):
    patient=  Patient.objects.get(user_id=name)
    records= MedicalRecords.objects.filter(patient=patient)
    return render(request,"swasthya/doctor/patient_detail.html",{"patient":patient,"records":records})

def view_appointments(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor = doctor)
    if(request.method=="POST"):
            form=DateForm(request.POST)
            if(form.is_valid()):
                start_date = form.cleaned_data['start']
                end_date = form.cleaned_data['end']
                try:
                    appointments = Appointment.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date) & Q(doctor = doctor))
                except Appointment.DoesNotExist:
                    appointments = None
                return render(request, "swasthya/doctor/view_appointments.html", {'appointments':appointments,'form':form})
    else:
        form=DateForm()
        return render (request,'swasthya/doctor/view_appointments.html',{'form':form})