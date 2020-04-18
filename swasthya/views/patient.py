from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView,View
from django.views.generic import CreateView,ListView
from ..models import User, Patient
from ..forms import PatientSignUpForm,PatientDetailsForm, BookingForm,MedicalRecordUploadForm
from ..models import User, Patient,Doctor,Appointment,MedicalRecords
from ..forms import PatientSignUpForm,PatientDetailsForm,SearchForm,SearchForm2
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import datetime
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
    patient_profile = Patient.objects.get(user=request.user)
    return render(request, 'swasthya/patient/patient_home.html', {'patient_profile': patient_profile})

def patient_signup(request):
    if request.method == 'POST':
        user_form = PatientSignUpForm(request.POST, prefix='UF')
        profile_form = PatientDetailsForm(request.POST, prefix='PF')
        print(user_form.errors.as_data())
        print(profile_form.errors.as_data())
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save(commit=False)
            user.is_patient = True
            user.save()
            patient_profile= profile_form.save(commit=False)
            patient_profile.user=user
            patient_profile.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return(redirect('p_home'))
            #return render(request, 'swasthya/patient/patient_home.html',{'patient_profile': patient_profile})
        else:
            user_form = PatientSignUpForm(request.POST, prefix='UF')
            profile_form = PatientDetailsForm(request.POST, prefix='PF')
            #context['form'] = self.form_class(self.request.POST)
            return render(request, 'swasthya/patient/signup_patient.html',{
                'user_form': user_form,
                'profile_form': profile_form,
            })

    else:
        user_form = PatientSignUpForm(request.POST, prefix='UF')
        profile_form = PatientDetailsForm(request.POST, prefix='PF')
        return render(request, 'swasthya/patient/signup_patient.html',{
            'user_form': user_form,
            'profile_form': profile_form,
        })

def bookAppointment(request):
    user = Patient.objects.get(user=request.user)
    if request.method == 'POST':
        bookingForm = BookingForm(request.POST)
        if bookingForm.is_valid():
            booking = bookingForm.save(commit=False)
            booking.patient = user
            booking.save()
            return redirect("p_home")
        else:
            return render(request, "swasthya/patient/book.html", {'form':bookingForm, 'user':user})
    else:
        bookingForm = BookingForm(request.POST)
        return render(request, "swasthya/patient/book.html", {'form':bookingForm, 'user':user})

def ViewAppointment(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient = patient)
    return render(request, "swasthya/patient/viewAppointments.html", {'appointments':appointments})


#works, but not a select menu
def doctor_list(request):
    doctors=Doctor.objects.all()    
    if(request.method=="POST"):
        form1=SearchForm(request.POST)
        if(form1.is_valid()):
            doctors=Doctor.objects.all().filter(Q(specialisation=request.POST.get('specialisation','')) & Q(location=request.POST.get('location','')))
            return render(request,"swasthya/patient/doctor_list.html",{'form1':form1,'doctors':doctors})
    else:
        form1=SearchForm()
        return render (request,"swasthya/patient/doctor_list.html",{'form1':form1,'doctors':doctors})  

def doctor_detail(request,name):
    doctor=  Doctor.objects.get(user=name)
    return render(request,"swasthya/patient/doctor_detail.html",{"doctor":doctor})

#gives select form but doesn't select
def doctor_list_form(request):
    doctors=Doctor.objects.all()    
    if(request.method=="POST"):
        form1=SearchForm2(request.POST)
        if(form1.is_valid()):
            doctors=Doctor.objects.all().filter(Q(specialisation=request.POST.get('specialisation','')) & Q(location=request.POST.get('location','')))
            return render(request,"swasthya/patient/doctor_list.html",{'form1':form1,'doctors':doctors})
        else:
            form1=SearchForm2()
            return render (request,"swasthya/patient/doctor_list.html",{'form1':form1})
    else:
            form1=SearchForm2()
            return render (request,"swasthya/patient/doctor_list.html",{'form1':form1,'doctors':doctors})   

#tried another method but that didn't work either
class DoctorListView(View):
    model = Doctor
    form_class = SearchForm2
    template_name = 'swasthya/patient/doctor_list.html'

    def get(self, request, *args, **kwargs):
        form1 = SearchForm2()
        context ={'form1': form1}
        return render(request,'swasthya/patient/doctor_list.html',context)
    
    def post(self, request, *args, **kwargs):
        form1 = SearchForm2(data=request.POST)
        specialisation = request.POST.get('specialisation')
        form1.fields['specialisation'].choices = [(specialisation, specialisation)]
        if form1.is_valid():
            doctors=Doctor.objects.all().filter(Q(specialisation=request.POST.get('specialisation','')) & Q(location=request.POST.get('location','')))
            form1 = SearchForm2()
            return render(request, 'swasthya/patient/doctor_list.html', {'form1': form1,'doctors':doctors})
        return render(request, 'swasthya/patient/doctor_list.html', {'form1': form1})

def change_password_patient(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('p_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'swasthya/patient/change_password.html', {
        'form': form
    })

def profile_edit_patient(request):
        user = Patient.objects.get(user=request.user)
        #quotes=quote.objects.get(pk=pk)
        if(request.method=="POST"):
            form=PatientDetailsForm(request.POST,instance=user)
            if(form.is_valid()):
                form.save()
                update_session_auth_hash(request, user)
                return(redirect("profile_view_patient"))
        else:
            form=PatientDetailsForm(instance=user)
            return render (request,'swasthya/patient/profile_edit.html',{'form':form})  
def profile_view_patient(request):
        patient = Patient.objects.get(user=request.user)
        return render (request,'swasthya/patient/profile_view.html',{'patient':patient})

def add_medical_record(request):
    user = Patient.objects.get(user=request.user)
    if request.method == 'POST':
        form = MedicalRecordUploadForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = user
            record.save()
            return redirect("view_medical_records")
        else:
            return render(request, "swasthya/patient/add_medical_record.html", {'form':form, 'user':user})
    else:
        form = MedicalRecordUploadForm(request.POST)
        return render(request, "swasthya/patient/add_medical_record.html", {'form':form, 'user':user})

def view_medical_records(request):
    patient = Patient.objects.get(user=request.user)
    records=MedicalRecords.objects.filter(patient=patient)
    return render (request,'swasthya/patient/view_medical_records.html',{'records':records})
