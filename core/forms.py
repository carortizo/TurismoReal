from django.forms import ModelForm
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


