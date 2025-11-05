from django.db import models
from django.core.exceptions import ValidationError
from pacientes.models import Paciente
from usuarios.models import Usuario
from datetime import datetime, time

class Cita(models.Model):
    ESTADO = (
        ('PROGRAMADA', 'Programada'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_CURSO', 'En Curso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
        ('NO_ASISTIO', 'No Asistió'),
    )
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='citas'
    )
    medico = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='citas_medico',
        limit_choices_to={'rol': 'MEDICO'}
    )
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO, default='PROGRAMADA')
    observaciones = models.TextField(blank=True)
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='citas_creadas'
    )
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    motivo_cancelacion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha', 'hora']
        unique_together = ['medico', 'fecha', 'hora']
        
    def __str__(self):
        return f"Cita - {self.paciente.get_nombre_completo()} con Dr. {self.medico.get_full_name()} - {self.fecha} {self.hora}"
    
    def clean(self):
        # Validar que la cita sea en horario laboral (8am - 6pm)
        if self.hora:
            if self.hora < time(8, 0) or self.hora >= time(18, 0):
                raise ValidationError('Las citas deben ser entre 8:00 AM y 6:00 PM')
        
        # Validar que la fecha no sea en el pasado
        if self.fecha:
            from django.utils import timezone
            if self.fecha < timezone.now().date():
                raise ValidationError('No se pueden crear citas en fechas pasadas')