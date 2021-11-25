from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MaxValueValidator

from .models import *

class CreateUserForm(UserCreationForm):
    rut = forms.IntegerField(validators=[MaxValueValidator(999999999)])
    telefono = forms.IntegerField(validators=[MaxValueValidator(999999999)])
    apellidos = forms.CharField(max_length=75)
    email = forms.EmailField(max_length=60, required=True)
    class Meta:
        model = User
        fields= ['rut','username','apellidos','telefono','email','password1','password2']


class DateInput(forms.DateInput):
    input_type ='date'



class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reservas
        fields = ("metodo_pago_id_met_pago",)
        





