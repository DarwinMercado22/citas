from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    
    # Apps
    path('usuarios/', include('usuarios.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('historias/', include('historias_clinicas.urls')),
    path('citas/', include('citas.urls')),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/pacientes/', views.reporte_pacientes, name='reporte_pacientes'),
    path('reportes/consultas/', views.reporte_consultas, name='reporte_consultas'),
    path('reportes/citas/', views.reporte_citas, name='reporte_citas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)