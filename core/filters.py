import django_filters
from .models import *

class DepartamentoFilter(django_filters.FilterSet):
    class Meta:
        model = Departamento
        fields = ['zonas_id_zonas','std_depto_id_stdo_depto'] 