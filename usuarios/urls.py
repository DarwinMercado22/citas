from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('crear/', views.usuario_crear, name='usuario_crear'),
    path('listar/', views.usuario_listar, name='usuario_listar'),
    path('editar/<int:pk>/', views.usuario_editar, name='usuario_editar'),
    path('eliminar/<int:pk>/', views.usuario_eliminar, name='usuario_eliminar'),
]