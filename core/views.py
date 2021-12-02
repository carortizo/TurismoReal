from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from datetime import date
from datetime import datetime
from django.db.models import Q
from .filters import DepartamentoFilter
import cx_Oracle

from django.contrib.auth import authenticate, login, logout


from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, EstadoForm, ReservaForm, ZonaForm
from .decorators import func_only, unauthenticated_user, allowed_users, admin_only, user_only
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import base64

@login_required(login_url='login')
@allowed_users(allowed_roles=['func'])
def funcHome(request):
    return render(request,'core/pages/func.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def newdepto(request):
    form2= ZonaForm()
    form= EstadoForm()
    registrar =request.session.get('Registrar')
    if request.method == 'POST':
        form2= ZonaForm(request.POST)
        form= EstadoForm(request.POST)
        if form.is_valid() and form2.is_valid():
            me=request.POST.get('metros_cua')
            dir=request.POST.get('direccion')
            pre=request.POST.get('precio')
            zon=form2.cleaned_data.get("zonas")
            std=form.cleaned_data.get("estado")
            idnv=((Inventario.objects.all().count())+1)
            hab=request.POST.get('habitacion')
            cam=request.POST.get('cama')
            ban=request.POST.get('bano')
            inc=request.POST.get('incluido')
            imagen=request.FILES["imagen"].read()
            Inventario.objects.create(id_inventario=idnv,habitacion=hab,camas=cam,incluido=inc,baños=ban)
            inv=Inventario.objects.get(id_inventario=idnv)
            idep=((Departamento.objects.all().count())+1)
            Departamento.objects.create(id_depto=idep,metros_cua=me,direccion=dir,precio=pre,img=imagen,zonas_id_zonas=zon,inventario_id_inventario=inv,std_depto_id_stdo_depto=std)
            return redirect('admins')
    context={"form":form,"form2":form2}
    return render(request,'core/pages/newdepto.html',context)


#Página home de admins
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminHome(request):
    deptos= Departamento.objects.all()
    myFilter = DepartamentoFilter(request.GET, queryset=deptos)
    deptos=myFilter.qs
    context={"deptos":deptos,"myFilter":myFilter}
    return render(request,'core/pages/admins.html',context)



#Página para registrar funcionarios. Solo deberia poder acceder un admin(?)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registerFunc(request):
    form = CreateUserForm()
    form2= ZonaForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form2= ZonaForm(request.POST)
        if form.is_valid() and form2.is_valid():
            if User.objects.filter(username=form.cleaned_data.get('email')).exists():
               messages.info(request,'Correo ya se encuentra en uso')
            elif Cliente.objects.filter(rut=form.cleaned_data.get('rut')).exists():
                messages.info(request,'Rut ya se encuentra en uso')
            else:
                User.objects.create_user(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'), first_name=form.cleaned_data.get('username'),last_name=form.cleaned_data.get('apellidos'))
                #form.save()
                id_per=((Personal.objects.all().count())+1)
                idz=form2.cleaned_data.get("zonas")
                Personal.objects.create(id_personal=id_per, nombre=form.cleaned_data.get('username'),apellidos=form.cleaned_data.get('apellidos'),rut=form.cleaned_data.get('rut'),telefono=form.cleaned_data.get('telefono'),correo=form.cleaned_data.get('email'),contraseña=form.cleaned_data.get('password1'),tipo_personal_id_tipo_prs=(TipoPersonal.objects.get(id_tipo_prs=1)),zonas_id_zonas=idz)
                user= form.cleaned_data.get('email')
                name=form.cleaned_data.get('username')
                my_group = Group.objects.get(name='func') 
                my_group.user_set.add(User.objects.get(username=user).pk)
                messages.success(request,'Cuenta creada para ' + name)

                return redirect('admins')

    context={'form':form,'form2':form2}
    return render(request,'core/pages/registerfunc.html',context)

##Codigo para página de registro de cliente
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data.get('email')).exists():
               messages.info(request,'Correo ya se encuentra en uso')
            elif Cliente.objects.filter(rut=form.cleaned_data.get('rut')).exists():
                messages.info(request,'Rut ya se encuentra en uso')
            else:
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

##Codigo para página de inicio de sesión
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

##Codigo para cerrar sesión
def logoutUser(request):
    logout(request)
    return redirect('login')


##Codigo para página de arriendo/reserva
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def arriendo(request):
    form = ReservaForm()
    arrendar =request.session.get('arrendar')
    if request.method == 'POST':
        acomp=int(request.POST.get('acomp'))
        tour=request.POST.get('tour')
        transport=request.POST.get('transport')
        entrada=datetime.strptime(request.POST.get('entrada'), "%Y-%m-%d").date()
        salida=datetime.strptime(request.POST.get('salida'), "%Y-%m-%d").date()
        
        form = ReservaForm(request.POST)
        
        if form.is_valid():
            delta=(salida-entrada)
            sub=((((Departamento.objects.get(id_depto=arrendar).precio)*((acomp)+1)))*(delta.days))
            idre=((Reservas.objects.all().count())+1)
            transp=((Transporte.objects.all().count())+1)
            pric=0
            rut=(Cliente.objects.get(correo=request.user).rut)
            if tour:
                tur='Si'
                pric+=(5000*((acomp)+1))
                
            else:
                tur='No'
            if transport:
                tran='Si'
                pric+=10000
                
            else:
                tran='No'
            pricto=pric+sub#pago_reserva| (dias*precioNoche)+tour+transporte
            
            
            Reservas.objects.create(id_reservas=idre,pago_reserva=pricto,
            num_acomp=acomp,fecha_entrada=entrada,
            fecha_salida=salida,multa=None,subtotal=sub,
            cliente_rut=Cliente.objects.get(rut=rut),departamento_id_depto=Departamento.objects.get(id_depto=arrendar),
            metodo_pago_id_met_pago=form.cleaned_data.get('metodo_pago_id_met_pago'),std_reservas_id_std_resev=StdReservas.objects.get(id_std_resev=3))
            
            Transporte.objects.create(id_transp=transp,direccion='Casa',
             destino=(Departamento.objects.get(id_depto=arrendar).direccion),zonas=(Departamento.objects.get(id_depto=arrendar).zonas_id_zonas),
             comunas='PROVINCIA DE CAUTÍN',fecha_trans=entrada,
             std_transporte_id_std_transp=(StdTransporte.objects.get(id_std_transp=1)),trans_condc_id_conduc=TransCondc.objects.get(id_conduc=1))

            ServicioExtra.objects.create(id_servextra=((ServicioExtra.objects.all().count())+1),tour=tur,transporte=tran,precio=pric,
             tour_id_tour=Tour.objects.get(id_tour=1),transporte_id_transp=Transporte.objects.get(id_transp=transp),
             reservas_id_reservas=Reservas.objects.get(id_reservas=idre))

            obj=Departamento.objects.get(id_depto=arrendar)
            obj.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=3)
            obj.save()
            
            return redirect('home')
    
    deptos= Departamento.objects.all().filter(id_depto=arrendar)
    arreglo=[]
    for i in deptos:
        
        data={
            'data':i,
            'img':base64.b64encode(i.img).decode()
        }
        arreglo.append(data)
    inv=Inventario.objects.all()
    
    return render(request,'core/pages/arriendo.html',{'deptos':arreglo,'inv':inv,'form':form})

##Codigo para página "casa" 
@login_required(login_url='login')
@user_only
@allowed_users(allowed_roles=['user'])
def home(request):
    context={}
    
    deptos= Departamento.objects.all().filter(std_depto_id_stdo_depto=1)
    
    arreglo=[]

    for i in deptos:
        
        data={
            'data':i,
            'img':base64.b64encode(i.img).decode()
        }
        arreglo.append(data)
    
    reserv=0
    reserv2=[]
    reserv3=[]
    arreglo2=[]
    if Reservas.objects.all().filter(cliente_rut=(Cliente.objects.get(correo=request.user).rut)).count()>0:
        reserv2= (Reservas.objects.all().filter(cliente_rut=(Cliente.objects.get(correo=request.user).rut)))
        
        for i in reserv2:
        
            data={
            'data':i,
            'img':base64.b64encode(i.departamento_id_depto.img).decode()
        }
        arreglo2.append(data)
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
        ServicioExtra.objects.filter(reservas_id_reservas=canceler.id_reservas).delete()
        Transporte.objects.filter(destino=canceler.departamento_id_depto.direccion).delete()
        obj=Departamento.objects.get(id_depto=canceler.departamento_id_depto.id_depto)
        obj.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=1)
        Reservas.objects.filter(id_reservas=canceler.id_reservas).delete()
        obj.save()
            
        return redirect('home')
    elif request.method == 'POST' and 'editar'in request.POST:
        editar=request.POST.get('editar')
        request.session['editar']= editar
        return redirect('editar')

    return render(request,'core/pages/home.html',{'deptos':arreglo,'reserv':reserv,'reserv2':arreglo2})

##Codigo para página de edición de reserva
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def editar(request):
    form = ReservaForm()
    editar =request.session.get('editar')
    idres=((ServicioExtra.objects.get(reservas_id_reservas=editar).reservas_id_reservas).id_reservas)
    resv = ((Reservas.objects.get(id_reservas=idres).departamento_id_depto).id_depto)
    serv=ServicioExtra.objects.get(reservas_id_reservas=editar)


    if request.method == 'POST':
        acomp=int(request.POST.get('acomp'))
        tour=request.POST.get('tour')
        transport=request.POST.get('transport')
        entrada=datetime.strptime(request.POST.get('entrada'), "%Y-%m-%d").date()
        salida=datetime.strptime(request.POST.get('salida'), "%Y-%m-%d").date()
        
        form = ReservaForm(request.POST)
        
        if form.is_valid():
            delta=(salida-entrada)
            sub=((((Departamento.objects.get(id_depto=resv).precio)*((acomp)+1)))*(delta.days))
            
            pric=0
            if tour:
                tur='Si'
                pric+=(5000*((acomp)+1))
                
            else:
                tur='No'
            if transport:
                tran='Si'
                pric+=10000
                
            else:
                tran='No'
            pricto=pric+sub#pago_reserva| (dias*precioNoche)+tour+transporte
            
            res=(Reservas.objects.get(id_reservas=idres))
            res.num_acomp=acomp
            res.fecha_entrada=entrada
            res.fecha_salida=salida
            res.pago_reserva=pricto
            res.subtotal=sub
            res.metodo_pago_id_met_pago=form.cleaned_data.get('metodo_pago_id_met_pago')
            res.save()
            serv=ServicioExtra.objects.get(reservas_id_reservas=editar)
            serv.tour=tur
            serv.transporte=tran
            serv.precio=pric
            serv.save()
            trans=Transporte.objects.get(destino=serv.transporte_id_transp)
            trans.fecha_trans=entrada
            trans.save()

            
            obj=Departamento.objects.get(id_depto=(resv))
            obj.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=3)
            obj.save()
            
            return redirect('home')
    
    deptos2= Departamento.objects.all().filter(id_depto= (resv))
    reserv2=Reservas.objects.all().filter(id_reservas=idres)
    servi=ServicioExtra.objects.all().filter(id_servextra=editar)
    inv=Inventario.objects.all()
    arreglo=[]
    for i in deptos2:
        
        data={
            'data':i,
            'img':base64.b64encode(i.img).decode()
        }
        arreglo.append(data)
    
    return render(request,'core/pages/editar.html',{'deptos2':arreglo,'inv':inv,'form':form,'reserv2':reserv2,"servi":servi})




#-----------Creo que los que siguen no fueron usados XD-------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def user(request):
    return HttpResponse('user')

@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def departamento(request):
    return HttpResponse('departamento')

@unauthenticated_user
def pswd(request):

    return HttpResponse('pswd')

   