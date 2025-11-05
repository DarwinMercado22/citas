from django import forms
from .models import HistoriaClinica, Consulta, Examen

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['antecedentes_personales', 'antecedentes_familiares', 'medicamentos_actuales']
        widgets = {
            'antecedentes_personales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enfermedades previas, cirugías, hospitalizaciones...'
            }),
            'antecedentes_familiares': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enfermedades hereditarias en la familia...'
            }),
            'medicamentos_actuales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Medicamentos que toma actualmente...'
            }),
        }
        labels = {
            'antecedentes_personales': 'Antecedentes Personales',
            'antecedentes_familiares': 'Antecedentes Familiares',
            'medicamentos_actuales': 'Medicamentos Actuales',
        }


class ConsultaForm(forms.ModelForm):
    proxima_cita = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Próxima Cita'
    )
    
    class Meta:
        model = Consulta
        fields = [
            'presion_arterial', 'frecuencia_cardiaca', 'temperatura',
            'peso', 'altura', 'motivo_consulta', 'sintomas',
            'diagnostico', 'tratamiento', 'observaciones', 'proxima_cita'
        ]
        widgets = {
            'presion_arterial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 120/80'
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ppm'
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': '°C'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'kg'
            }),
            'altura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'cm'
            }),
            'motivo_consulta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'sintomas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'tratamiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'presion_arterial': 'Presión Arterial',
            'frecuencia_cardiaca': 'Frecuencia Cardíaca',
            'temperatura': 'Temperatura',
            'peso': 'Peso',
            'altura': 'Altura',
            'motivo_consulta': 'Motivo de Consulta',
            'sintomas': 'Síntomas',
            'diagnostico': 'Diagnóstico',
            'tratamiento': 'Tratamiento',
            'observaciones': 'Observaciones',
        }


class ExamenForm(forms.ModelForm):
    fecha_realizacion = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha de Realización'
    )
    
    class Meta:
        model = Examen
        fields = ['tipo', 'nombre', 'descripcion', 'fecha_realizacion', 'resultados', 'archivo_resultado']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resultados': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'archivo_resultado': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tipo': 'Tipo de Examen',
            'nombre': 'Nombre del Examen',
            'descripcion': 'Descripción',
            'fecha_realizacion': 'Fecha de Realización',
            'resultados': 'Resultados',
            'archivo_resultado': 'Archivo de Resultado',
        }