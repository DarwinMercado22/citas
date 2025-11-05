from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import HistoriaClinica, Consulta, Examen
from pacientes.models import Paciente
from .forms import HistoriaClinicaForm, ConsultaForm, ExamenForm

def es_medico_o_admin(user):
    return user.rol in ['MEDICO', 'ADMIN']

@login_required
def historia_clinica_detalle(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    
    # Obtener o crear historia clínica
    historia_clinica, created = HistoriaClinica.objects.get_or_create(paciente=paciente)
    
    # Obtener todas las consultas
    consultas = historia_clinica.consultas.all()
    
    context = {
        'paciente': paciente,
        'historia_clinica': historia_clinica,
        'consultas': consultas,
        'created': created
    }
    
    return render(request, 'historias_clinicas/historia_detalle.html', context)

@login_required
def historia_clinica_editar(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    historia_clinica, created = HistoriaClinica.objects.get_or_create(paciente=paciente)
    
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST, instance=historia_clinica)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historia clínica actualizada exitosamente.')
            return redirect('historia_clinica_detalle', paciente_id=paciente_id)
    else:
        form = HistoriaClinicaForm(instance=historia_clinica)
    
    return render(request, 'historias_clinicas/historia_form.html', {
        'form': form,
        'paciente': paciente,
        'historia_clinica': historia_clinica
    })

@login_required
def consulta_crear(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    historia_clinica, created = HistoriaClinica.objects.get_or_create(paciente=paciente)
    
    # Solo médicos pueden crear consultas
    if request.user.rol != 'MEDICO':
        messages.error(request, 'Solo los médicos pueden registrar consultas.')
        return redirect('historia_clinica_detalle', paciente_id=paciente_id)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.historia_clinica = historia_clinica
            consulta.medico = request.user
            consulta.save()
            messages.success(request, 'Consulta registrada exitosamente.')
            return redirect('consulta_detalle', pk=consulta.pk)
    else:
        form = ConsultaForm()
    
    return render(request, 'historias_clinicas/consulta_form.html', {
        'form': form,
        'paciente': paciente,
        'titulo': 'Registrar Consulta'
    })

@login_required
def consulta_detalle(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    examenes = consulta.examenes.all()
    
    context = {
        'consulta': consulta,
        'paciente': consulta.historia_clinica.paciente,
        'examenes': examenes
    }
    
    return render(request, 'historias_clinicas/consulta_detalle.html', context)

@login_required
def consulta_editar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    
    # Solo el médico que creó la consulta o un admin puede editarla
    if request.user.rol != 'ADMIN' and consulta.medico != request.user:
        messages.error(request, 'No tienes permisos para editar esta consulta.')
        return redirect('consulta_detalle', pk=pk)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada exitosamente.')
            return redirect('consulta_detalle', pk=pk)
    else:
        form = ConsultaForm(instance=consulta)
    
    return render(request, 'historias_clinicas/consulta_form.html', {
        'form': form,
        'paciente': consulta.historia_clinica.paciente,
        'consulta': consulta,
        'titulo': 'Editar Consulta'
    })

@login_required
def examen_crear(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    
    # Solo médicos pueden ordenar exámenes
    if request.user.rol != 'MEDICO':
        messages.error(request, 'Solo los médicos pueden ordenar exámenes.')
        return redirect('consulta_detalle', pk=consulta_id)
    
    if request.method == 'POST':
        form = ExamenForm(request.POST, request.FILES)
        if form.is_valid():
            examen = form.save(commit=False)
            examen.consulta = consulta
            examen.save()
            messages.success(request, 'Examen registrado exitosamente.')
            return redirect('consulta_detalle', pk=consulta_id)
    else:
        form = ExamenForm()
    
    return render(request, 'historias_clinicas/examen_form.html', {
        'form': form,
        'consulta': consulta,
        'paciente': consulta.historia_clinica.paciente,
        'titulo': 'Registrar Examen'
    })

@login_required
def examen_editar(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    
    if request.method == 'POST':
        form = ExamenForm(request.POST, request.FILES, instance=examen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examen actualizado exitosamente.')
            return redirect('consulta_detalle', pk=examen.consulta.pk)
    else:
        form = ExamenForm(instance=examen)
    
    return render(request, 'historias_clinicas/examen_form.html', {
        'form': form,
        'examen': examen,
        'consulta': examen.consulta,
        'paciente': examen.consulta.historia_clinica.paciente,
        'titulo': 'Editar Examen'
    })

@login_required
def examen_eliminar(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    consulta_id = examen.consulta.pk
    
    # Solo médicos o admin pueden eliminar
    if request.user.rol not in ['MEDICO', 'ADMIN']:
        messages.error(request, 'No tienes permisos para eliminar exámenes.')
        return redirect('consulta_detalle', pk=consulta_id)
    
    if request.method == 'POST':
        examen.delete()
        messages.success(request, 'Examen eliminado exitosamente.')
        return redirect('consulta_detalle', pk=consulta_id)
    
    return render(request, 'historias_clinicas/examen_confirm_delete.html', {
        'examen': examen
    })