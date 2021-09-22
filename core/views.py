from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

#from models import *
from .forms import CreateUserForm
from .decorators import unauthenticated_user

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user= form.cleaned_data.get('username')
            messages.success(request,'Cuenta creada para ' + user)

            return redirect('login')

    context={'form':form}
    return render(request,'core/pages/register.html',context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Usuario o Contraseña Incorrecto(s)')
    context={}
    return render(request,'core/pages/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def user(request):
    return HttpResponse('user')

@login_required(login_url='login')
def departamento(request):
    return HttpResponse('departamento')

@unauthenticated_user
def pswd(request):

    return HttpResponse('pswd')


@login_required(login_url='login')
def home(request):
    return render(request,'core/pages/home.html')