from django.urls import path
from . import views

urlpatterns = [
    # Historia Clínica
    path('paciente/<int:paciente_id>/', views.historia_clinica_detalle, name='historia_clinica_detalle'),
    path('paciente/<int:paciente_id>/editar/', views.historia_clinica_editar, name='historia_clinica_editar'),
    
    # Consultas
    path('paciente/<int:paciente_id>/consulta/crear/', views.consulta_crear, name='consulta_crear'),
    path('consulta/<int:pk>/', views.consulta_detalle, name='consulta_detalle'),
    path('consulta/<int:pk>/editar/', views.consulta_editar, name='consulta_editar'),
    
    # Exámenes
    path('consulta/<int:consulta_id>/examen/crear/', views.examen_crear, name='examen_crear'),
    path('examen/<int:pk>/editar/', views.examen_editar, name='examen_editar'),
    path('examen/<int:pk>/eliminar/', views.examen_eliminar, name='examen_eliminar'),
]