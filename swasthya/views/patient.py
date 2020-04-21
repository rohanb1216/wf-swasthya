from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView,View
from django.views.generic import CreateView,ListView
from ..models import User, Patient
from ..forms import PatientSignUpForm,PatientDetailsForm, BookingFormInit,MedicalRecordUploadForm, BookingFormFinal
from ..models import User, Patient,Doctor,Appointment,MedicalRecords
from ..forms import PatientSignUpForm,PatientDetailsForm,SearchForm,SearchForm2
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from django.http import JsonResponse
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
    slots = [True, True, True, True, True, True, True]
    print(type(request.user.username))
    if request.method == 'POST':
        bookingForm = BookingFormInit(request.POST)
        slotForm = BookingFormFinal(request.POST)
        if bookingForm.is_valid():
            booking = bookingForm.save(commit=False)
            slotForm.is_valid()
            slot = slotForm.cleaned_data
            slot = slot['slots']
            # print(type(slot))
            # print(slot)
            appointment = Appointment.objects.get(doctor = booking.doctor, date = booking.date)
            if(slot == 'slot1'):
                appointment.slot1 = request.user.username
            elif slot == 'slot2':
                appointment.slot2 = request.user.username
            elif slot == 'slot3':
                appointment.slot3 = request.user.username
            elif slot == 'slot4':
                appointment.slot4 = request.user.username
            elif slot == 'slot5':
                appointment.slot5 = request.user.username
            elif slot == 'slot6':
                appointment.slot6 = request.user.username
            elif slot == 'slot7':
                appointment.slot6 = request.user.username
            appointment.save()
            
            
            return redirect("p_home")
            
    else:
        bookingForm = BookingFormInit(request.POST, initial={'date': datetime.date.today})
        slotForm = BookingFormFinal(request.POST)
        return render(request, "swasthya/patient/book.html", {'form':bookingForm, 'slotForm':slotForm})

def ExistingSlots(request):
    slots = [True, True, True, True, True, True, True]
    doctor = request.GET.get('doctor', None)
    date = request.GET.get('date', None)
    doctor = Doctor.objects.get(pk=doctor)
    # print(type(date))
    if Appointment.objects.filter(date = date, doctor=doctor).exists():
        print('if')
        appointment = Appointment.objects.get(date = date, doctor = doctor)
        # slots = [True, True, True, True, True, True, True]
        if appointment.slot1 != '':
            slots[0] = False
        if appointment.slot2 != '':
            slots[1] = False
        if appointment.slot3 != '':
            slots[2] = False
        if appointment.slot4 != '':
            slots[3] = False
        if appointment.slot5 != '':
            slots[4] = False
        if appointment.slot6 != '':
            slots[5] = False
        if appointment.slot7 != '':
            slots[6] = False
        return JsonResponse(slots, safe = False)


    else:
        appointment = Appointment.objects.create(doctor = doctor, date = date, slot1 = '', slot2 = '', slot3 = '', slot4 = '', slot5 = '', slot6 = '', slot7 = '')
        print(Appointment.objects.all())
        print('else')
        return JsonResponse(slots, safe = False)


def ViewAppointment(request):
    appointments = Appointment.objects.raw('SELECT id, doctor_id, date, slot1, slot2, slot3, slot4, slot5, slot6, slot7 FROM swasthya_appointment WHERE %s IN(slot1, slot2, slot3, slot4, slot5, slot6, slot7);', [request.user.username])
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
    id = User.objects.get(username=name)
    doctor=  Doctor.objects.get(user_id=id)
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
