from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('MEDICO', 'Médico'),
        ('ENFERMERO', 'Enfermero'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='ENFERMERO')
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_rol_display()}"