from django.urls import path
from . import views

urlpatterns = [
    path('', views.paciente_listar, name='paciente_listar'),
    path('crear/', views.paciente_crear, name='paciente_crear'),
    path('<int:pk>/', views.paciente_detalle, name='paciente_detalle'),
    path('<int:pk>/editar/', views.paciente_editar, name='paciente_editar'),
    path('<int:pk>/eliminar/', views.paciente_eliminar, name='paciente_eliminar'),
]