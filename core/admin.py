from django.contrib import admin
from django.db.models.aggregates import StdDev
from .models import Cliente, Departamento, Zonas, Inventario, StdDepto, Acompañantes,CheckIn,CheckOut,MetodoPago,Personal,RegistroArri,RegistroPago,Reservas,ServicioExtra,StdReservas,StdTour,StdTransporte,TipoPersonal,Tour,TransCondc,TransVehi,Transporte
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Zonas)
admin.site.register(Inventario)
admin.site.register(StdDepto)
admin.site.register(Departamento)
admin.site.register(Acompañantes)
admin.site.register(CheckIn)
admin.site.register(CheckOut)
admin.site.register(MetodoPago)
admin.site.register(Personal)
admin.site.register(RegistroArri)
admin.site.register(RegistroPago)
admin.site.register(Reservas)
admin.site.register(ServicioExtra)
admin.site.register(StdReservas)
admin.site.register(StdTour)
admin.site.register(StdTransporte)
admin.site.register(TipoPersonal)
admin.site.register(Tour)
admin.site.register(TransCondc)
admin.site.register(TransVehi)
admin.site.register(Transporte)
