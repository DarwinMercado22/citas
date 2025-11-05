from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class UsuarioRegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombres',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    cedula = forms.CharField(
        max_length=20,
        required=True,
        label='Cédula',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=15,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    rol = forms.ChoiceField(
        choices=Usuario.ROLES,
        required=True,
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    especialidad = forms.CharField(
        max_length=100,
        required=False,
        label='Especialidad (solo médicos)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'cedula', 
                  'telefono', 'rol', 'especialidad', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
    def clean_especialidad(self):
        rol = self.cleaned_data.get('rol')
        especialidad = self.cleaned_data.get('especialidad')
        
        if rol == 'MEDICO' and not especialidad:
            raise forms.ValidationError('La especialidad es obligatoria para médicos')
        
        return especialidad


class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )


class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'especialidad', 'activo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'especialidad': 'Especialidad',
            'activo': 'Activo',
        }