from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha de Nacimiento'
    )
    
    class Meta:
        model = Paciente
        fields = [
            'tipo_documento', 'numero_documento', 'nombres', 'apellidos',
            'fecha_nacimiento', 'genero', 'telefono', 'celular', 'email',
            'direccion', 'ciudad', 'tipo_sangre', 'alergias',
            'contacto_emergencia_nombre', 'contacto_emergencia_telefono',
            'contacto_emergencia_parentesco', 'activo'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_sangre': forms.Select(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contacto_emergencia_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_emergencia_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_emergencia_parentesco': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'numero_documento': 'Número de Documento',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'genero': 'Género',
            'telefono': 'Teléfono',
            'celular': 'Celular',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'tipo_sangre': 'Tipo de Sangre',
            'alergias': 'Alergias',
            'contacto_emergencia_nombre': 'Nombre del Contacto de Emergencia',
            'contacto_emergencia_telefono': 'Teléfono del Contacto de Emergencia',
            'contacto_emergencia_parentesco': 'Parentesco',
            'activo': 'Activo',
        }


class PacienteBusquedaForm(forms.Form):
    busqueda = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, apellido o documento...'
        })
    )
    tipo_documento = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + list(Paciente.TIPO_DOCUMENTO),
        label='Tipo de Documento',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    activo = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos'), ('1', 'Activos'), ('0', 'Inactivos')],
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )