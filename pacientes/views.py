from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Paciente
from .forms import PacienteForm, PacienteBusquedaForm

@login_required
def paciente_crear(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f'Paciente {paciente.get_nombre_completo()} registrado exitosamente.')
            return redirect('paciente_detalle', pk=paciente.pk)
    else:
        form = PacienteForm()
    
    return render(request, 'pacientes/paciente_form.html', {
        'form': form,
        'titulo': 'Registrar Paciente'
    })

@login_required
def paciente_listar(request):
    form = PacienteBusquedaForm(request.GET)
    pacientes = Paciente.objects.all()
    
    if form.is_valid():
        busqueda = form.cleaned_data.get('busqueda')
        tipo_documento = form.cleaned_data.get('tipo_documento')
        activo = form.cleaned_data.get('activo')
        
        if busqueda:
            pacientes = pacientes.filter(
                Q(numero_documento__icontains=busqueda) |
                Q(nombres__icontains=busqueda) |
                Q(apellidos__icontains=busqueda) |
                Q(email__icontains=busqueda)
            )
        
        if tipo_documento:
            pacientes = pacientes.filter(tipo_documento=tipo_documento)
        
        if activo:
            pacientes = pacientes.filter(activo=(activo == '1'))
    
    # Paginación
    paginator = Paginator(pacientes, 10)  # 10 pacientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'pacientes': page_obj
    }
    
    return render(request, 'pacientes/paciente_list.html', context)

@login_required
def paciente_detalle(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    context = {
        'paciente': paciente,
        'edad': paciente.get_edad()
    }
    
    return render(request, 'pacientes/paciente_detail.html', context)

@login_required
def paciente_editar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Paciente {paciente.get_nombre_completo()} actualizado exitosamente.')
            return redirect('paciente_detalle', pk=paciente.pk)
    else:
        form = PacienteForm(instance=paciente)
    
    return render(request, 'pacientes/paciente_form.html', {
        'form': form,
        'titulo': 'Editar Paciente',
        'paciente': paciente
    })

@login_required
def paciente_eliminar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    # Solo administradores pueden eliminar
    if request.user.rol != 'ADMIN':
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('paciente_detalle', pk=pk)
    
    if request.method == 'POST':
        paciente.activo = False
        paciente.save()
        messages.success(request, f'Paciente {paciente.get_nombre_completo()} desactivado exitosamente.')
        return redirect('paciente_listar')
    
    return render(request, 'pacientes/paciente_confirm_delete.html', {'paciente': paciente})