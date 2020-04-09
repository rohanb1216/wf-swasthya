from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('d_home')
        else:
            return redirect('p_home')
    return render(request, 'swasthya/home.html')
