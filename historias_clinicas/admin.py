from django.contrib import admin
from .models import HistoriaClinica, Consulta, Examen

class ConsultaInline(admin.TabularInline):
    model = Consulta
    extra = 0
    readonly_fields = ['fecha_consulta']

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha_creacion', 'ultima_actualizacion']
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'paciente__numero_documento']
    inlines = [ConsultaInline]

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'medico', 'fecha_consulta', 'diagnostico']
    list_filter = ['fecha_consulta', 'medico']
    search_fields = ['historia_clinica__paciente__nombres', 'diagnostico']

@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'consulta', 'fecha_solicitud', 'fecha_realizacion']
    list_filter = ['tipo', 'fecha_solicitud']