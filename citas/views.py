from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Cita
from .forms import CitaForm, CitaCancelarForm, CitaBusquedaForm

@login_required
def cita_crear(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.creado_por = request.user
            try:
                cita.full_clean()  # Validar el modelo
                cita.save()
                messages.success(request, 'Cita registrada exitosamente.')
                return redirect('cita_detalle', pk=cita.pk)
            except Exception as e:
                messages.error(request, f'Error al crear la cita: {str(e)}')
    else:
        form = CitaForm()
    
    return render(request, 'citas/cita_form.html', {
        'form': form,
        'titulo': 'Registrar Cita'
    })

@login_required
def cita_listar(request):
    form = CitaBusquedaForm(request.GET)
    citas = Cita.objects.select_related('paciente', 'medico').all()
    
    if form.is_valid():
        fecha_desde = form.cleaned_data.get('fecha_desde')
        fecha_hasta = form.cleaned_data.get('fecha_hasta')
        medico = form.cleaned_data.get('medico')
        estado = form.cleaned_data.get('estado')
        
        if fecha_desde:
            citas = citas.filter(fecha__gte=fecha_desde)
        
        if fecha_hasta:
            citas = citas.filter(fecha__lte=fecha_hasta)
        
        if medico:
            citas = citas.filter(medico=medico)
        
        if estado:
            citas = citas.filter(estado=estado)
    
    # Si el usuario es médico, mostrar solo sus citas
    if request.user.rol == 'MEDICO':
        citas = citas.filter(medico=request.user)
    
    context = {
        'form': form,
        'citas': citas
    }
    
    return render(request, 'citas/cita_list.html', context)

@login_required
def cita_detalle(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    
    # Verificar si el usuario puede ver esta cita
    if request.user.rol == 'MEDICO' and cita.medico != request.user:
        messages.error(request, 'No tienes permisos para ver esta cita.')
        return redirect('cita_listar')
    
    context = {
        'cita': cita
    }
    
    return render(request, 'citas/cita_detalle.html', context)

@login_required
def cita_editar(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    
    # Solo se pueden editar citas que no estén completadas o canceladas
    if cita.estado in ['COMPLETADA', 'CANCELADA']:
        messages.error(request, 'No se pueden editar citas completadas o canceladas.')
        return redirect('cita_detalle', pk=pk)
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                cita = form.save()
                cita.full_clean()
                messages.success(request, 'Cita actualizada exitosamente.')
                return redirect('cita_detalle', pk=pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar la cita: {str(e)}')
    else:
        form = CitaForm(instance=cita)
    
    return render(request, 'citas/cita_form.html', {
        'form': form,
        'cita': cita,
        'titulo': 'Editar Cita'
    })

@login_required
def cita_cancelar(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    
    if cita.estado in ['COMPLETADA', 'CANCELADA']:
        messages.error(request, 'Esta cita ya está completada o cancelada.')
        return redirect('cita_detalle', pk=pk)
    
    if request.method == 'POST':
        form = CitaCancelarForm(request.POST)
        if form.is_valid():
            cita.estado = 'CANCELADA'
            cita.fecha_cancelacion = timezone.now()
            cita.motivo_cancelacion = form.cleaned_data['motivo_cancelacion']
            cita.save()
            messages.success(request, 'Cita cancelada exitosamente.')
            return redirect('cita_detalle', pk=pk)
    else:
        form = CitaCancelarForm()
    
    return render(request, 'citas/cita_cancelar.html', {
        'form': form,
        'cita': cita
    })

@login_required
def cita_cambiar_estado(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Cita.ESTADO).keys():
            cita.estado = nuevo_estado
            cita.save()
            messages.success(request, f'Estado de la cita actualizado a {cita.get_estado_display()}.')
        else:
            messages.error(request, 'Estado inválido.')
        
        return redirect('cita_detalle', pk=pk)
    
    return redirect('cita_detalle', pk=pk)

@login_required
def citas_del_dia(request):
    hoy = timezone.now().date()
    citas = Cita.objects.filter(fecha=hoy).select_related('paciente', 'medico')
    
    # Si es médico, mostrar solo sus citas
    if request.user.rol == 'MEDICO':
        citas = citas.filter(medico=request.user)
    
    context = {
        'citas': citas,
        'fecha': hoy
    }
    
    return render(request, 'citas/citas_del_dia.html', context)

@login_required
def mis_citas(request):
    """Vista para que los médicos vean solo sus citas"""
    if request.user.rol != 'MEDICO':
        messages.error(request, 'Esta vista es solo para médicos.')
        return redirect('dashboard')
    
    citas = Cita.objects.filter(medico=request.user).order_by('fecha', 'hora')
    
    context = {
        'citas': citas
    }
    
    return render(request, 'citas/mis_citas.html', context)