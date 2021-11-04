from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
    rut = forms.IntegerField()
    telefono = forms.IntegerField()
    apellidos = forms.CharField(max_length=75)
    
    class Meta:
        model = User
        fields= ['rut','username','apellidos','telefono','email','password1','password2']


class DateInput(forms.DateInput):
    input_type ='date'



class ReservaForm(forms.ModelForm):
    tour = forms.BooleanField(required=False)
    transport= forms.BooleanField(required=False)
    class Meta:
        model = Reservas
        fields = ("num_acomp","fecha_entrada","fecha_salida","metodo_pago_id_met_pago",'tour','transport')
        widgets={'fecha_entrada':DateInput(),'fecha_salida':DateInput()}





