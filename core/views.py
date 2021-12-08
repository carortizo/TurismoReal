from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from datetime import date
from datetime import datetime
from django.db.models import Q
from .filters import DepartamentoFilter
from .filters import CheckOutFilter
from django.db.models import Max
import cx_Oracle

from django.contrib.auth import authenticate, login, logout


from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.views import View
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from .models import *
from .forms import CreateUserForm, EstadoForm, ReservaForm, ZonaForm
from .decorators import func_only, unauthenticated_user, allowed_users, admin_only, user_only
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import base64

##Mover ciertas cosas a models.py si sobra tiempo


#check-out reserva seleccionada
@login_required(login_url='login')
@allowed_users(allowed_roles=['func'])
def checker(request):
        ##check es id_reservas
    check =request.session.get('check')
    reserva=Reservas.objects.get(id_reservas=check)
    idcre=CheckOut.objects.all()
    if idcre.count()>0:
        idcre.aggregate(Max('id_check_out'))
        idcre=idcre.order_by('-id_check_out')[0]
        idc=(int(idcre.id_check_out)+1)
    else:
        idc=1
    idrer=RegistroArri.objects.all()
    if idrer.count()>0:
        idrer.aggregate(Max('id_registro_arri'))
        idrer=idrer.order_by('-id_registro_arri')[0]
        idr=(int(idrer.id_registro_arri)+1)
    else:
        idr=1
    idp=Personal.objects.get(correo=request.user.username)
    if request.method == 'POST':
        estado=request.POST.get('deptostd')
        multa=request.POST.get('multa')
        total=(int(multa)+int((reserva.subtotal)))

        
        checkers=CheckIn.objects.get(registro_pago_id_reg_pago=(RegistroPago.objects.get(reservas_id_reservas=reserva)))
        RegistroArri.objects.create(id_registro_arri=idr,descripcion=estado,pago_total=total,check_in_id_check_in=checkers)
        rp=RegistroArri.objects.get(id_registro_arri=idr)
        CheckOut.objects.create(id_check_out=idc,descripcion=estado,multa=multa,registro_arri_id_registro_arri=rp,personal_id_personal=idp)
        dep=Departamento.objects.get(id_depto=reserva.departamento_id_depto.id_depto)
        dep.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=1)
        dep.save()
        reserva.multa=multa
        reserva.save()
        return redirect('checkout')
    
    context={"reserva":reserva}
    return render(request,'core/pages/checker.html',context)

#Check-out
@login_required(login_url='login')
@allowed_users(allowed_roles=['func'])
def checkout(request):
    regi=RegistroArri.objects.all()
    arregloregi=[]
    for i in regi:
       arregloregi.append(i.check_in_id_check_in.registro_pago_id_reg_pago.reservas_id_reservas.id_reservas)

    #regi2=RegistroPago.objects.all()
    #arregloregi2=[]
    #for i in regi2:
       #arregloregi2.append(i.reservas_id_reservas.id_reservas)

    deptos= Reservas.objects.filter().exclude(id_reservas__in=arregloregi)
    cliente=Cliente.objects.all()
    
    arreglo=[]

    for i in deptos:
        
        data={
            'data':i,
            'img':base64.b64encode(i.departamento_id_depto.img).decode()
        }

        arreglo.append(data)
    if request.method == 'POST':
        check=request.POST.get('check')
        request.session['check']= check
        return redirect('checker')
    
    context={"resev2":arreglo,"cli":cliente}
    return render(request,'core/pages/checkout.html',context)


#check-in reserva seleccionada
@login_required(login_url='login')
@allowed_users(allowed_roles=['func'])
def check(request):
    ##check es id_reservas
    check =request.session.get('check')
    reserva=Reservas.objects.get(id_reservas=check)
    idcre=CheckIn.objects.all()
    if idcre.count()>0:
        idcre.aggregate(Max('id_check_in'))
        idcre=idcre.order_by('-id_check_in')[0]
        idc=(int(idcre.id_check_in)+1)
    else:
        idc=1    
    idre=RegistroPago.objects.all()
    if idre.count()>0:
        idre.aggregate(Max('id_reg_pago'))
        idre=idre.order_by('-id_reg_pago')[0]
        idr=(int(idre.id_reg_pago)+1)
    else:
        idr=1
    idp=Personal.objects.get(correo=request.user.username)
    if request.method == 'POST':
        estado=request.POST.get('deptostd')
        RegistroPago.objects.create(id_reg_pago=idr,descripcion=estado,pago_total=reserva.subtotal,reservas_id_reservas=reserva,metodo_pago_id_met_pago=reserva.metodo_pago_id_met_pago)
        rp=RegistroPago.objects.get(id_reg_pago=idr)
        CheckIn.objects.create(id_check_in=idc,descripcion=estado,registro_pago_id_reg_pago=rp,personal_id_personal=idp)
        return redirect('checkin')
    
    context={"reserva":reserva}
    return render(request,'core/pages/check.html',context)


#Check-in
@login_required(login_url='login')
@allowed_users(allowed_roles=['func'])
def checkin(request):
    regi=RegistroPago.objects.all()
    arregloregi=[]
    for i in regi:
       arregloregi.append(i.reservas_id_reservas.id_reservas)




    deptos= Reservas.objects.filter().exclude(id_reservas__in=arregloregi)
    cliente=Cliente.objects.all()
    
    arreglo=[]

    for i in deptos:
        
        data={
            'data':i,
            'img':base64.b64encode(i.departamento_id_depto.img).decode()
        }

        arreglo.append(data)
    if request.method == 'POST':
        check=request.POST.get('check')
        request.session['check']= check
        return redirect('check')
    
    context={"resev2":arreglo,"cli":cliente}
    return render(request,'core/pages/checkin.html',context)

#Página "Home" de funcionarios
@login_required(login_url='login')
@allowed_users(allowed_roles=['func'])
def funcHome(request):
    return render(request,'core/pages/func.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def inform(request):
    out= CheckOut.objects.all()
    myFilter = CheckOutFilter(request.GET, queryset=out)
    out=myFilter.qs
    usuario=request.user.username.upper()
    date=str(datetime.date(datetime.today())).upper()
    context={"out":out,"myFilter":myFilter,'usuario':usuario,'date':date}
    if request.method == 'POST':
        template= get_template('core/pages/pdf.html')
        

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        html = template.render(context)
            
            # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
            # if error then show some funy view
        return response
    return render(request,'core/pages/inform.html',context)

#Edición de departamentos
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edepto(request):
    #edepto es el id del departamento que decidiste editar
    edepto =request.session.get('edepto')
    form2= ZonaForm()
    form= EstadoForm()
    idepto = (Departamento.objects.all().filter(id_depto=edepto))
    arreglo=[]
    for i in idepto:
        
        data={
            'data':i,
            'img':base64.b64encode(i.img).decode()
        }
        arreglo.append(data)

    if request.method == 'POST':
        form2= ZonaForm(request.POST)
        form= EstadoForm(request.POST)
        if form.is_valid() and form2.is_valid():
            change=request.POST.get('change')
            if change=="True":
                imagen=request.FILES["imagen"].read()
                dep=Departamento.objects.get(id_depto=edepto)
                dep.img=imagen
                dep.save()
            dep2=Departamento.objects.get(id_depto=edepto)
            inv=Inventario.objects.get(id_inventario=dep2.inventario_id_inventario.id_inventario)
            dep2.zonas_id_zonas=form2.cleaned_data.get("zonas")
            dep2.direccion=request.POST.get('direccion')
            dep2.std_depto_id_stdo_depto=form.cleaned_data.get("estado")
            dep2.descripcion=request.POST.get('descripcion')
            dep2.metros_cua=request.POST.get('metros_cua')
            dep2.precio=request.POST.get('precio')
            dep2.save()
            
            inv.habitacion=request.POST.get('habitacion')
            inv.camas=request.POST.get('cama')
            inv.incluido=request.POST.get('incluido')
            inv.baños=request.POST.get('bano')
            inv.save()
            

            return redirect('admins')
    
    context={"idepto":arreglo,"form":form,"form2":form2}
    return render(request,'core/pages/edepto.html',context)

#Creacion de nuevos departamentos
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def newdepto(request):
    form2= ZonaForm()
    form= EstadoForm()
    registrar =request.session.get('Registrar')
    if request.method == 'POST':
        form2= ZonaForm(request.POST)
        form= EstadoForm(request.POST)
        imagen=request.FILES["imagen"].read()
        if form.is_valid() and form2.is_valid():
            me=request.POST.get('metros_cua')
            dir=request.POST.get('direccion')
            pre=request.POST.get('precio')
            zon=form2.cleaned_data.get("zonas")
            std=form.cleaned_data.get("estado")
            idnvre=Inventario.objects.all()
            if idnvre.count()>0:
                idnvre.aggregate(Max('id_inventario'))
                idnvre=idnvre.order_by('-id_inventario')[0]
                idnv=(int(idnvre.id_inventario)+1)
            else:
                idnv=1
            hab=request.POST.get('habitacion')
            cam=request.POST.get('cama')
            ban=request.POST.get('bano')
            inc=request.POST.get('incluido')
            desc=request.POST.get('descripcion')
            
            Inventario.objects.create(id_inventario=idnv,habitacion=hab,camas=cam,incluido=inc,baños=ban)
            inv=Inventario.objects.get(id_inventario=idnv)
            idepre=Departamento.objects.all()
            if idepre.count()>0:
                idepre.aggregate(Max('id_depto'))
                idepre=idepre.order_by('-id_depto')[0]
                idep=(int(idepre.id_depto)+1)
            else:
                idep=1
            Departamento.objects.create(id_depto=idep,metros_cua=me,direccion=dir,descripcion=desc,precio=pre,img=None,zonas_id_zonas=zon,inventario_id_inventario=inv,std_depto_id_stdo_depto=std)
            dep=Departamento.objects.get(id_depto=idep)
            dep.img=imagen
            dep.save()
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
    if request.method == 'POST':
        edepto=request.POST.get('edepto')
        request.session['edepto']= edepto
        return redirect('edepto')
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
                id_perer=Personal.objects.all()
                if id_perer.count()>0:
                    id_perer.aggregate(Max('id_personal'))
                    id_perer=id_perer.order_by('-id_personal')[0]
                    id_per=(int(id_perer.id_personal)+1)
                else:
                    id_per=1
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
            idrere=Reservas.objects.all()
            if idrere.count()>0:
                idrere.aggregate(Max('id_reservas'))
                idrere=idrere.order_by('-id_reservas')[0]
                idre=(int(idrere.id_reservas)+1)
            else:
                idre=1

            transpid=Transporte.objects.all()
            if transpid.count()>0:
                transpid.aggregate(Max('id_transp'))
                transpid=transpid.order_by('-id_transp')[0]
                transp=(int(transpid.id_transp)+1)
            else:
                transp=1
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
            
            ##La creación de un transportista esta fuera del objetivo de este trabajo/ "Provincia de cautín" esta intencionalmente Hard Coded
            
            Transporte.objects.create(id_transp=transp,direccion='Casa',
             destino=(Departamento.objects.get(id_depto=arrendar).direccion),zonas=(Departamento.objects.get(id_depto=arrendar).zonas_id_zonas),
             comunas='PROVINCIA DE CAUTÍN',fecha_trans=entrada,
             std_transporte_id_std_transp=(StdTransporte.objects.get(id_std_transp=1)),trans_condc_id_conduc=TransCondc.objects.get(id_conduc=1))
            
            idevalserv=ServicioExtra.objects.all()
            if idevalserv.count()>0:
                idevalserv.aggregate(Max('id_servextra'))
                idevalserv=idevalserv.order_by('-id_servextra')[0]
                ideva=(int(idevalserv.id_servextra)+1)
            else:
                ideva=1
            


            ServicioExtra.objects.create(id_servextra=ideva,tour=tur,transporte=tran,precio=pric,
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
    regi=RegistroArri.objects.all()
    arregloregi=[]
    for i in regi:
       arregloregi.append(i.check_in_id_check_in.registro_pago_id_reg_pago.reservas_id_reservas.id_reservas)

    deptos= Reservas.objects.filter(id_reservas__in=arregloregi)

    if Reservas.objects.all().filter(cliente_rut=(Cliente.objects.get(correo=request.user).rut)).exclude(id_reservas__in=arregloregi).count()>0:
        
        reserv2= (Reservas.objects.all().filter(cliente_rut=(Cliente.objects.get(correo=request.user).rut)).exclude(id_reservas__in=arregloregi))
        
        for i in reserv2:
        
            data={
            'data':i,
            'img':base64.b64encode(i.departamento_id_depto.img).decode()
        }
        arreglo2.append(data)

        regis=RegistroPago.objects.all()
        arregloregis=[]
        for i in regis:
            arregloregis.append(i.reservas_id_reservas.id_reservas)
        reserv3= (Reservas.objects.all().filter(cliente_rut=(Cliente.objects.get(correo=request.user).rut)).exclude(id_reservas__in=arregloregis))
        

        reserv=Departamento.objects.all()
    
    if request.method == 'POST' and 'arrendar'in request.POST:
        arrendar=request.POST.get('arrendar')
        request.session['arrendar'] = arrendar
        return redirect('arriendo')
    elif request.method == 'POST' and 'cancelar'in request.POST:
        cancelar=request.POST.get('cancelar')
        regis2=RegistroPago.objects.all()
        arregloregis2=[]
        for i in regis2:
            arregloregis2.append(i.reservas_id_reservas.id_reservas)

        if Reservas.objects.all().filter(id_reservas=cancelar).exclude(id_reservas__in=arregloregis2).count()>0:
            canceler=Reservas.objects.get(id_reservas=cancelar)
            ServicioExtra.objects.filter(reservas_id_reservas=canceler).delete()
            obj=Departamento.objects.get(id_depto=canceler.departamento_id_depto.id_depto)
            obj.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=1)
            Reservas.objects.filter(id_reservas=cancelar).delete()
            obj.save()
            
        return redirect('home')
    elif request.method == 'POST' and 'editar'in request.POST:
        editar=request.POST.get('editar')
        regis2=RegistroPago.objects.all()
        arregloregis2=[]
        for i in regis2:
            arregloregis2.append(i.reservas_id_reservas.id_reservas)

        if Reservas.objects.all().filter(id_reservas=editar).exclude(id_reservas__in=arregloregis2).count()>0:
            request.session['editar']= editar
            return redirect('editar')
        else:
            return redirect('home')

    return render(request,'core/pages/home.html',{'deptos':arreglo,'reserv':reserv,'reserv2':arreglo2,'reserv3':reserv3})

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
            trans=Transporte.objects.filter(destino=serv.transporte_id_transp)[0]
            trans.fecha_trans=entrada
            trans.save()

            
            obj=Departamento.objects.get(id_depto=(resv))
            obj.std_depto_id_stdo_depto=StdDepto.objects.get(id_stdo_depto=3)
            obj.save()
            
            return redirect('home')
    
    deptos2= Departamento.objects.all().filter(id_depto= (resv))
    reserv2=Reservas.objects.all().filter(id_reservas=idres)
    servi=ServicioExtra.objects.all().filter(reservas_id_reservas=editar)
    inv=Inventario.objects.all()
    arreglo=[]
    for i in deptos2:
        
        data={
            'data':i,
            'img':base64.b64encode(i.img).decode()
        }
        arreglo.append(data)
    
    return render(request,'core/pages/editar.html',{'deptos2':arreglo,'inv':inv,'form':form,'reserv2':reserv2,"servi":servi})




#def pdf(request):
#    try:
#        template= get_template('core/pages/pdf.html')
#        context = {'title': 'pdf'}
#        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

#        html = template.render(context)
            
            # create a pdf
#        pisa_status = pisa.CreatePDF(
#        html, dest=response)
#            # if error then show some funy view
#        return response
#    except:
#        pass
#    return redirect('admins')





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

   