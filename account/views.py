from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from django.contrib.auth.models import User
#from students.models import Student
#from teachers.models import Teacher
from .forms import UserRegistrationForm
# Create your views here.

@login_required
def dashboard(request):
    total_students = 10
    total_teachers = 10
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
    }
    return render(request, 'dashboard.html', context)
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            auth_user = authenticate(username=user_form.cleaned_data['username'],
                                     password=user_form.cleaned_data['password'])
            if auth_user is not None:
                login(request, auth_user)
            #return redirect('account:dashboard')
            return redirect('')
        else:
            return render(request, 'account/register.html', {'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})
