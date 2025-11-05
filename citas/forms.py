from django import forms
from .models import Cita
from usuarios.models import Usuario
from pacientes.models import Paciente

class CitaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha'
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        label='Hora'
    )
    
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha', 'hora', 'motivo', 'estado', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'paciente': 'Paciente',
            'medico': 'Médico',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'motivo': 'Motivo',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo médicos activos
        self.fields['medico'].queryset = Usuario.objects.filter(rol='MEDICO', activo=True)
        # Filtrar solo pacientes activos
        self.fields['paciente'].queryset = Paciente.objects.filter(activo=True)


class CitaCancelarForm(forms.Form):
    motivo_cancelacion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese el motivo de la cancelación...'
        }),
        label='Motivo de Cancelación',
        required=True
    )


class CitaBusquedaForm(forms.Form):
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Desde'
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Hasta'
    )
    medico = forms.ModelChoiceField(
        required=False,
        queryset=Usuario.objects.filter(rol='MEDICO', activo=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Médico',
        empty_label='Todos'
    )
    estado = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + list(Cita.ESTADO),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Estado'
    )