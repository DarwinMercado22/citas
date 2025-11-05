from django.db import models
from pacientes.models import Paciente
from usuarios.models import Usuario

class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(
        Paciente, 
        on_delete=models.CASCADE, 
        related_name='historia_clinica'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    # Antecedentes
    antecedentes_personales = models.TextField(
        blank=True, 
        help_text="Enfermedades previas, cirugías, hospitalizaciones"
    )
    antecedentes_familiares = models.TextField(
        blank=True,
        help_text="Enfermedades hereditarias en la familia"
    )
    medicamentos_actuales = models.TextField(
        blank=True,
        help_text="Medicamentos que toma actualmente"
    )
    
    class Meta:
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'
        
    def __str__(self):
        return f"Historia Clínica - {self.paciente.get_nombre_completo()}"


class Consulta(models.Model):
    historia_clinica = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    medico = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        limit_choices_to={'rol': 'MEDICO'}
    )
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    
    # Signos vitales
    presion_arterial = models.CharField(max_length=10, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Consulta
    motivo_consulta = models.TextField()
    sintomas = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True)
    
    # Seguimiento
    proxima_cita = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-fecha_consulta']
        
    def __str__(self):
        return f"Consulta - {self.historia_clinica.paciente.get_nombre_completo()} - {self.fecha_consulta.date()}"


class Examen(models.Model):
    TIPO_EXAMEN = (
        ('LAB', 'Laboratorio'),
        ('IMG', 'Imagenología'),
        ('ESP', 'Especializado'),
    )
    
    consulta = models.ForeignKey(
        Consulta,
        on_delete=models.CASCADE,
        related_name='examenes'
    )
    tipo = models.CharField(max_length=3, choices=TIPO_EXAMEN)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_realizacion = models.DateField(null=True, blank=True)
    resultados = models.TextField(blank=True)
    archivo_resultado = models.FileField(
        upload_to='examenes/%Y/%m/',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Examen'
        verbose_name_plural = 'Exámenes'
        ordering = ['-fecha_solicitud']
        
    def __str__(self):
        return f"{self.nombre} - {self.consulta.historia_clinica.paciente.get_nombre_completo()}"