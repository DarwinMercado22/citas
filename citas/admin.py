from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'medico', 'fecha', 'hora', 'estado']
    list_filter = ['estado', 'fecha', 'medico']
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'medico__first_name', 'medico__last_name']
    date_hierarchy = 'fecha'