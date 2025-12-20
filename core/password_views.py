"""
Vistas para cambio de contraseña
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .password_forms import (
    ChangePasswordForm, 
    ChangeOtherUserPasswordForm,
    AdminChangePasswordForm
)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def change_password_view(request):
    """
    Vista para que el usuario cambie su propia contraseña
    Requiere la contraseña maestra configurada
    """
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            master_password = form.cleaned_data.get('master_password')
            new_password = form.cleaned_data.get('new_password')
            
            # Validar contraseña maestra
            MASTER_PASSWORD = getattr(settings, 'MASTER_PASSWORD', 'admin123')
            
            if master_password != MASTER_PASSWORD:
                messages.error(request, '❌ Contraseña maestra incorrecta')
                return render(request, 'core/change_password.html', {'form': form})
            
            # Cambiar contraseña del usuario actual
            user = request.user
            user.set_password(new_password)
            user.save()
            
            # Log de auditoria (opcional, para seguridad)
            messages.success(
                request, 
                '✅ Contraseña cambiada exitosamente. '
                'Por favor, inicia sesión nuevamente.'
            )
            
            # Registrar en auditoría
            from django.utils import timezone
            print(f"[AUDITORIA] Usuario {user.username} cambió su contraseña - {timezone.now()}")
            
            # Desloguear al usuario y redirigir a login
            from django.contrib.auth import logout
            logout(request)
            return redirect('login')
    
    else:
        form = ChangePasswordForm()
    
    context = {
        'form': form,
        'title': 'Cambiar mi Contraseña',
        'page_icon': '🔐'
    }
    
    return render(request, 'core/change_password.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def change_user_password_admin_view(request, username):
    """
    Vista para que admin cambie contraseña de otro usuario
    Solo accesible por administradores
    """
    
    # Verificar que sea admin
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, '❌ No tienes permisos para acceder a esta página')
        return redirect('home')
    
    # Obtener el usuario
    user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        form = AdminChangePasswordForm(request.POST)
        
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            
            # Cambiar contraseña del usuario
            user.set_password(new_password)
            user.save()
            
            messages.success(
                request, 
                f'✅ Contraseña de {user.username} cambiada exitosamente'
            )
            
            # Log de auditoría
            print(f"[AUDITORIA] Admin {request.user.username} cambió contraseña de {user.username} - {timezone.now()}")
            
            return redirect('user_list_admin')
    
    else:
        form = AdminChangePasswordForm(initial={'username': username})
    
    context = {
        'form': form,
        'target_user': user,
        'title': f'Cambiar Contraseña - {user.get_full_name() or user.username}',
        'page_icon': '🔐'
    }
    
    return render(request, 'core/admin_change_password.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def list_users_admin_view(request):
    """
    Vista para listar usuarios (solo para admin)
    Permite acceso rápido a cambiar contraseñas
    """
    
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, '❌ No tienes permisos para acceder a esta página')
        return redirect('home')
    
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
        'title': 'Gestión de Usuarios',
        'page_icon': '👥'
    }
    
    return render(request, 'core/users_list_admin.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def settings_view(request):
    """
    Vista de configuración para usuario
    Acceso a cambio de contraseña y otras opciones
    """
    
    context = {
        'title': 'Configuración',
        'page_icon': '⚙️',
        'user': request.user
    }
    
    return render(request, 'core/settings.html', context)


from django.utils import timezone
