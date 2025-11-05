from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Usuario
from .forms import UsuarioRegistroForm, UsuarioLoginForm, UsuarioEditForm

def es_admin(user):
    return user.is_authenticated and user.rol == 'ADMIN'

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UsuarioLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.activo:
                    login(request, user)
                    messages.success(request, f'¡Bienvenido {user.get_full_name()}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Tu cuenta está desactivada.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = UsuarioLoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

@login_required
@user_passes_test(es_admin)
def usuario_crear(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario {usuario.username} creado exitosamente.')
            return redirect('usuario_listar')
    else:
        form = UsuarioRegistroForm()
    
    return render(request, 'usuarios/usuario_form.html', {
        'form': form,
        'titulo': 'Crear Usuario'
    })

@login_required
@user_passes_test(es_admin)
def usuario_listar(request):
    busqueda = request.GET.get('busqueda', '')
    rol = request.GET.get('rol', '')
    
    usuarios = Usuario.objects.all()
    
    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) |
            Q(cedula__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    
    if rol:
        usuarios = usuarios.filter(rol=rol)
    
    context = {
        'usuarios': usuarios,
        'busqueda': busqueda,
        'rol': rol,
        'roles': Usuario.ROLES
    }
    
    return render(request, 'usuarios/usuario_list.html', context)

@login_required
@user_passes_test(es_admin)
def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente.')
            return redirect('usuario_listar')
    else:
        form = UsuarioEditForm(instance=usuario)
    
    return render(request, 'usuarios/usuario_form.html', {
        'form': form,
        'titulo': 'Editar Usuario',
        'usuario': usuario
    })

@login_required
@user_passes_test(es_admin)
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        usuario.activo = False
        usuario.save()
        messages.success(request, f'Usuario {usuario.username} desactivado exitosamente.')
        return redirect('usuario_listar')
    
    return render(request, 'usuarios/usuario_confirm_delete.html', {'usuario': usuario})

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})