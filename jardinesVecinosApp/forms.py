from django import forms 
from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Categoria, Producto

class RegistroUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre del usuario',
            'last_name': 'Apellido del usuario',
            'email': 'Correo',
            'password1': 'Contraseña',
            'password2': 'Repetir Contraseña',
        }
        error_messages = { #Solo se dan mensajes de error a estos ya que DJango no los valida por defecto
            'first_name': {
                'required': "El nombre es obligatorio.",
                'invalid': "El nombre solo puede contener letras.",
            },
            'last_name': {
                'required': "El apellido es obligatorio.",
                'invalid': "El apellido solo puede contener letras.",
            },
        }

class ActualizarPerfilForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(
        label="Contraseña nueva",
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label="Confirmar contraseña nueva",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Nombre del usuario',
            'last_name': 'Apellido del usuario',
            'email': 'Correo',
            'password1': 'Contraseña',
            'password2': 'Repetir Contraseña',
        }
        error_messages = { # Mensajes de error personalizados
            'first_name': {
                'required': "El nombre es obligatorio.",
                'invalid': "El nombre solo puede contener letras.",
            },
            'last_name': {
                'required': "El apellido es obligatorio.",
                'invalid': "El apellido solo puede contener letras.",
            },
        }

def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError('El nombre solo puede contener letras.')
        return first_name

def clean_last_name(self):
    last_name = self.cleaned_data.get('last_name')
    if not last_name.isalpha():
        raise forms.ValidationError('El apellido solo puede contener letras.')
    return last_name

class ProductoForm(forms.ModelForm):
    class Meta: 
        model = Producto
        fields = ['idProducto', 'stock','nombre', 'descripcion', 'precio', 'imagen', 'categoria']
        labels = {
            'idProducto': 'Id Producto',
            'stock': 'Stock',
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'precio': 'Precio',
            'imagen': 'Imagen',
            'categoria': 'Categoria'
        }
        widgets ={
            'idProducto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Id Producto',
                    'id': 'idProducto'
                }
            ),
            'stock': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese cantidad de stock',
                    'id': 'stock'
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese nombre Producto',
                    'id': 'nombre'
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese descripcion Producto',
                    'id': 'descripcion'
                }
            ),
            'precio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese precio',
                    'id': 'precio'
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'categoria'
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'imagen'
                }
            )
        }#fin_form
