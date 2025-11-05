from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from pacientes.models import Paciente
from citas.models import Cita
from historias_clinicas.models import Consulta
from usuarios.models import Usuario

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    
    # Estadísticas generales
    total_pacientes = Paciente.objects.filter(activo=True).count()
    total_medicos = Usuario.objects.filter(rol='MEDICO', activo=True).count()
    
    # Citas de hoy
    citas_hoy = Cita.objects.filter(fecha=hoy)
    if request.user.rol == 'MEDICO':
        citas_hoy = citas_hoy.filter(medico=request.user)
    
    # Citas próximas (próximos 7 días)
    fecha_limite = hoy + timedelta(days=7)
    citas_proximas = Cita.objects.filter(
        fecha__gte=hoy,
        fecha__lte=fecha_limite,
        estado='PROGRAMADA'
    )
    if request.user.rol == 'MEDICO':
        citas_proximas = citas_proximas.filter(medico=request.user)
    
    # Consultas recientes
        consultas_recientes = Consulta.objects.select_related(
        'historia_clinica__paciente', 'medico'
    ).order_by('-fecha_consulta')

    if request.user.rol == 'MEDICO':
        consultas_recientes = consultas_recientes.filter(medico=request.user)

    consultas_recientes = consultas_recientes[:5]

    context = {
        'total_pacientes': total_pacientes,
        'total_medicos': total_medicos,
        'citas_hoy': citas_hoy,
        'citas_proximas': citas_proximas[:5],
        'consultas_recientes': consultas_recientes,
    }

    return render(request, 'dashboard.html', context)

@login_required
def reportes(request):
    """Vista principal de reportes"""
    return render(request, 'reportes/index.html')

@login_required
def reporte_pacientes(request):
    """Reporte de pacientes registrados"""
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    pacientes = Paciente.objects.filter(activo=True)
    
    if fecha_desde:
        pacientes = pacientes.filter(fecha_registro__gte=fecha_desde)
    
    if fecha_hasta:
        pacientes = pacientes.filter(fecha_registro__lte=fecha_hasta)
    
    context = {
        'pacientes': pacientes,
        'total': pacientes.count(),
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta
    }
    
    return render(request, 'reportes/pacientes.html', context)

@login_required
def reporte_consultas(request):
    """Reporte de consultas realizadas"""
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    medico_id = request.GET.get('medico')
    
    consultas = Consulta.objects.select_related(
        'historia_clinica__paciente', 'medico'
    ).all()
    
    if fecha_desde:
        consultas = consultas.filter(fecha_consulta__gte=fecha_desde)
    
    if fecha_hasta:
        consultas = consultas.filter(fecha_consulta__lte=fecha_hasta)
    
    if medico_id:
        consultas = consultas.filter(medico_id=medico_id)
    
    medicos = Usuario.objects.filter(rol='MEDICO', activo=True)
    
    context = {
        'consultas': consultas,
        'total': consultas.count(),
        'medicos': medicos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'medico_id': medico_id
    }
    
    return render(request, 'reportes/consultas.html', context)

@login_required
def reporte_citas(request):
    """Reporte de citas"""
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    estado = request.GET.get('estado')
    
    citas = Cita.objects.select_related('paciente', 'medico').all()
    
    if fecha_desde:
        citas = citas.filter(fecha__gte=fecha_desde)
    
    if fecha_hasta:
        citas = citas.filter(fecha__lte=fecha_hasta)
    
    if estado:
        citas = citas.filter(estado=estado)
    
    context = {
        'citas': citas,
        'total': citas.count(),
        'estados': Cita.ESTADO,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estado': estado
    }
    
    return render(request, 'reportes/citas.html', context)