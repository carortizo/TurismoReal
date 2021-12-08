from django.db.models.query import QuerySet
import django_filters
from .models import *

CHOICE_ZONE=[(i.id_zonas,i.descripcion) for i in Zonas.objects.all()]
CHOICE_STATE=[(i.id_stdo_depto,i.descripcion) for i in StdDepto.objects.all()]
CHOICE_DEPTO=[(i.id_depto,i.direccion) for i in Departamento.objects.all()]

class DepartamentoFilter(django_filters.FilterSet):
    zone=django_filters.ChoiceFilter(field_name='zonas_id_zonas',label="Zona",choices=CHOICE_ZONE)
    estado=django_filters.ChoiceFilter(field_name='std_depto_id_stdo_depto',label="Estado",choices=CHOICE_STATE)


class CheckOutFilter(django_filters.FilterSet):
    
    start=django_filters.DateRangeFilter(field_name="registro_arri_id_registro_arri__check_in_id_check_in__registro_pago_id_reg_pago__reservas_id_reservas__fecha_salida",label="Rango")
    zone=django_filters.ChoiceFilter(field_name='registro_arri_id_registro_arri__check_in_id_check_in__registro_pago_id_reg_pago__reservas_id_reservas__departamento_id_depto__zonas_id_zonas',label="Zona",choices=CHOICE_ZONE)
    depto=django_filters.ChoiceFilter(field_name='registro_arri_id_registro_arri__check_in_id_check_in__registro_pago_id_reg_pago__reservas_id_reservas__departamento_id_depto',label="Departamento",choices=CHOICE_DEPTO)