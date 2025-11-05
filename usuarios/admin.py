from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'email', 'rol', 'activo']
    list_filter = ['rol', 'activo', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('cedula', 'telefono', 'especialidad', 'rol', 'activo')}),
    )