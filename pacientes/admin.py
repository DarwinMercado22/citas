from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'get_nombre_completo', 'tipo_sangre', 'telefono', 'activo']
    list_filter = ['tipo_documento', 'genero', 'tipo_sangre', 'activo']
    search_fields = ['numero_documento', 'nombres', 'apellidos', 'email']
    date_hierarchy = 'fecha_registro'