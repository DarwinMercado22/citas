from django.db import models
from django.core.validators import RegexValidator

class Paciente(models.Model):
    TIPO_DOCUMENTO = (
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
    )
    
    TIPO_SANGRE = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )
    
    GENERO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )
    
    # Datos personales
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=GENERO)
    
    # Contacto
    telefono = models.CharField(max_length=15)
    celular = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    
    # Datos médicos
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE)
    alergias = models.TextField(blank=True, help_text="Alergias conocidas del paciente")
    
    # Contacto de emergencia
    contacto_emergencia_nombre = models.CharField(max_length=200)
    contacto_emergencia_telefono = models.CharField(max_length=15)
    contacto_emergencia_parentesco = models.CharField(max_length=50)
    
    # Metadata
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-fecha_registro']
        
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.numero_documento}"
    
    def get_edad(self):
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def get_nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"