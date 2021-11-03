from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
import cx_Oracle

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import base64

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            Cliente.objects.create(rut=form.cleaned_data.get('rut'),nombre=form.cleaned_data.get('username'),apellidos=form.cleaned_data.get('apellidos'),telefono=form.cleaned_data.get('telefono'),correo=form.cleaned_data.get('email'),contraseña=form.cleaned_data.get('password1'))
            user= form.cleaned_data.get('username')
            my_group = Group.objects.get(name='user') 
            my_group.user_set.add(User.objects.get(username=user).pk)
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
def arriendo(request):
    arrendar =request.session.get('arrendar')
    deptos= Departamento.objects.all().filter(id_depto=arrendar)
    inv=Inventario.objects.all()
    
    return render(request,'core/pages/arriendo.html',{'deptos':deptos,'inv':inv})

@login_required(login_url='login')
def home(request):
    context={}
    
    deptos= Departamento.objects.all().filter(std_depto_id_stdo_depto=1)
    
    if request.method == 'POST':
        arrendar=request.POST.get('arrendar')
        request.session['arrendar'] = arrendar
        return redirect('arriendo')
    return render(request,'core/pages/home.html',{'deptos':deptos})