from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from datetime import date
from django.db.models import Q
import cx_Oracle

from django.contrib.auth import authenticate, login, logout


from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, ReservaForm
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
            User.objects.create_user(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'), first_name=form.cleaned_data.get('username'),last_name=form.cleaned_data.get('apellidos'))
            #form.save()
            Cliente.objects.create(rut=form.cleaned_data.get('rut'),nombre=form.cleaned_data.get('username'),apellidos=form.cleaned_data.get('apellidos'),telefono=form.cleaned_data.get('telefono'),correo=form.cleaned_data.get('email'),contraseña=form.cleaned_data.get('password1'))
            user= form.cleaned_data.get('email')
            name=form.cleaned_data.get('username')
            my_group = Group.objects.get(name='user') 
            my_group.user_set.add(User.objects.get(username=user).pk)
            messages.success(request,'Cuenta creada para ' + name)

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
            messages.info(request,'Correo o Contraseña Incorrecto(s)')
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
    form = ReservaForm()
    arrendar =request.session.get('arrendar')
    if request.method == 'POST':
        
        form = ReservaForm(request.POST)

        if form.is_valid():

            delta=(form.cleaned_data.get('fecha_salida')-form.cleaned_data.get('fecha_entrada'))
            sub=(Departamento.objects.get(id_depto=arrendar).precio)*(delta.days+1)
            idre=((Reservas.objects.all().count())+1)
            transp=((Transporte.objects.all().count())+1)
            pric=0
            rut=(Cliente.objects.get(correo=request.user).rut)
            if form.cleaned_data.get('tour'):
                tur='Si'
                pric=+(5000*((form.cleaned_data.get('num_acomp')+1)))
            else:
                tur='No'
            if form.cleaned_data.get('transport'):
                tran='Si'
                pric=+10000
            else:
                tran='No'
            pricto=pric+sub#pago_reserva| (dias*precioNoche)+tour+transporte
            
            
            Reservas.objects.create(id_reservas=idre,pago_reserva=pricto,
            num_acomp=form.cleaned_data.get('num_acomp'),fecha_entrada=form.cleaned_data.get('fecha_entrada'),
            fecha_salida=form.cleaned_data.get('fecha_salida'),multa=None,subtotal=sub,
            cliente_rut=Cliente.objects.get(rut=rut),departamento_id_depto=Departamento.objects.get(id_depto=arrendar),
            metodo_pago_id_met_pago=form.cleaned_data.get('metodo_pago_id_met_pago'),std_reservas_id_std_resev=StdReservas.objects.get(id_std_resev=3))
            
            Transporte.objects.create(id_transp=transp,direccion='Casa',
             destino=(Departamento.objects.get(id_depto=arrendar).direccion),zonas=(Departamento.objects.get(id_depto=arrendar).zonas_id_zonas),
             comunas='PROVINCIA DE CAUTÍN',fecha_trans=(form.cleaned_data.get('fecha_entrada')),
             std_transporte_id_std_transp=(StdTransporte.objects.get(id_std_transp=1)),trans_condc_id_conduc=TransCondc.objects.get(id_conduc=1))

            ServicioExtra.objects.create(id_servextra=((ServicioExtra.objects.all().count())+1),tour=tur,transporte=tran,precio=pric,
             tour_id_tour=Tour.objects.get(id_tour=1),transporte_id_transp=Transporte.objects.get(id_transp=transp),
             reservas_id_reservas=Reservas.objects.get(id_reservas=idre))

            obj=Departamento.objects.get(id_depto=arrendar)
            obj.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=3)
            obj.save()
            
            return redirect('home')
    
    deptos= Departamento.objects.all().filter(id_depto=arrendar)
    inv=Inventario.objects.all()
    
    return render(request,'core/pages/arriendo.html',{'deptos':deptos,'inv':inv,'form':form})

@login_required(login_url='login')
def home(request):
    context={}
    
    deptos= Departamento.objects.all().filter(std_depto_id_stdo_depto=1)
    
    reserv=0
    reserv2=[]
    reserv3=[]
    if Reservas.objects.all().filter(cliente_rut=(Cliente.objects.get(correo=request.user).rut)).count()>0:
        reserv2= (Reservas.objects.all().filter(cliente_rut=(Cliente.objects.get(correo=request.user).rut)))
        #queries = [Q(pk=value) for value in reserv2]
        #query = queries.pop()
        #for item in queries:
        #    query|=item.departamento_id_depto
        #for i in reserv2:
         #   reserv3 |=i.departamento_id_depto
        reserv=Departamento.objects.all()
    
    if request.method == 'POST' and 'arrendar'in request.POST:
        arrendar=request.POST.get('arrendar')
        request.session['arrendar'] = arrendar
        return redirect('arriendo')
    elif request.method == 'POST' and 'cancelar'in request.POST:
        cancelar=request.POST.get('cancelar')
        canceler=Reservas.objects.get(id_reservas=cancelar)
        print(cancelar)
        ServicioExtra.objects.filter(reservas_id_reservas=canceler.id_reservas).delete()
        Transporte.objects.filter(destino=canceler.departamento_id_depto.direccion).delete()
        obj=Departamento.objects.get(id_depto=canceler.departamento_id_depto.id_depto)
        obj.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=1)
        Reservas.objects.filter(id_reservas=canceler.id_reservas).delete()
        obj.save()
            
        return redirect('home')
    return render(request,'core/pages/home.html',{'deptos':deptos,'reserv':reserv,'reserv2':reserv2})