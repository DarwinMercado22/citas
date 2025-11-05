from django.urls import path
from . import views

urlpatterns = [
    path('', views.cita_listar, name='cita_listar'),
    path('crear/', views.cita_crear, name='cita_crear'),
    path('<int:pk>/', views.cita_detalle, name='cita_detalle'),
    path('<int:pk>/editar/', views.cita_editar, name='cita_editar'),
    path('<int:pk>/cancelar/', views.cita_cancelar, name='cita_cancelar'),
    path('<int:pk>/cambiar-estado/', views.cita_cambiar_estado, name='cita_cambiar_estado'),
    path('del-dia/', views.citas_del_dia, name='citas_del_dia'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
]