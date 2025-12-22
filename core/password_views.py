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
    ✅ NO requiere contraseña maestra - solo verifica contraseña actual
    Solo requiere contraseña maestra si es admin cambiando su propia contraseña
    """
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            
            # Validar contraseña actual del usuario
            user = request.user
            if not user.check_password(current_password):
                messages.error(request, '❌ Contraseña actual incorrecta')
                return render(request, 'core/change_password.html', {'form': form})
            
            # Cambiar contraseña del usuario actual
            user.set_password(new_password)
            user.save()
            
            # Actualizar en el archivo .env
            update_user_password_in_env(user.username, new_password)
            
            # Log de auditoria
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
        form = ChangePasswordForm(user=request.user)
    
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
            
            # Actualizar en el archivo .env
            update_user_password_in_env(user.username, new_password)
            
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
@require_http_methods(["GET", "POST"])
def list_users_admin_view(request):
    """
    Vista para listar usuarios (solo para admin)
    ⚠️ REQUIERE VERIFICACIÓN DE CONTRASEÑA MAESTRA
    Permite acceso rápido a cambiar contraseñas
    """
    
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, '❌ No tienes permisos para acceder a esta página')
        return redirect('home')
    
    # Verificar si ya pasó la verificación de contraseña maestra
    master_password_verified = request.session.get('master_password_verified_users', False)
    
    if not master_password_verified:
        # Mostrar formulario de verificación
        from .password_forms import MasterPasswordVerificationForm
        
        if request.method == 'POST':
            form = MasterPasswordVerificationForm(request.POST)
            if form.is_valid():
                master_password = form.cleaned_data.get('master_password')
                MASTER_PASSWORD = get_master_password()
                
                if master_password == MASTER_PASSWORD:
                    # Marcar como verificado en sesión (válido por 1 hora)
                    request.session['master_password_verified_users'] = True
                    request.session.set_expiry(3600)  # 1 hora
                    messages.success(request, '✅ Acceso verificado. Gestión de usuarios desbloqueada.')
                    return redirect('user_list_admin')
                else:
                    messages.error(request, '❌ Contraseña maestra incorrecta')
        else:
            form = MasterPasswordVerificationForm()
        
        return render(request, 'core/master_password_verification.html', {
            'form': form,
            'title': 'Verificación de Seguridad - Gestión de Usuarios',
            'page_icon': '🔐'
        })
    
    # Si pasó la verificación, mostrar usuarios
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
import os
import re


def get_master_password():
    """Lee contraseña maestra del .env sin reiniciar servidor"""
    env_file = os.path.join(settings.BASE_DIR, '.env')
    
    if not os.path.exists(env_file):
        return 'admin123'
    
    try:
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip().startswith('MASTER_PASSWORD='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    
    return 'admin123'


def update_user_password_in_env(username, new_password):
    """Actualiza la contraseña de usuario/admin en el archivo .env"""
    env_file = os.path.join(settings.BASE_DIR, '.env')
    
    if not os.path.exists(env_file):
        return False
    
    # Mapeo de usuarios a variables de entorno
    user_mapping = {
        'usuario': 'DEFAULT_USER_PASSWORD',
        'admin': 'DEFAULT_ADMIN_PASSWORD'
    }
    
    if username not in user_mapping:
        return False
    
    env_var_name = user_mapping[username]
    
    try:
        # Leer el contenido actual del archivo
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Buscar y actualizar la línea correspondiente
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith(f'{env_var_name}='):
                lines[i] = f'{env_var_name}={new_password}\n'
                updated = True
                break
        
        # Si no encontró la línea, agregarla al final
        if not updated:
            lines.append(f'{env_var_name}={new_password}\n')
        
        # Escribir el archivo actualizado
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo actualizar .env: {e}")
        return False


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def system_configuration_view(request):
    """
    Vista para configuraciones del sistema
    SOLO PARA SUPERUSERS
    """
    
    if not request.user.is_superuser:
        messages.error(request, '❌ No tienes permisos para acceder a esta página')
        return redirect('home')
    
    # Verificar contraseña maestra
    master_password_verified = request.session.get('master_password_verified_config', False)
    
    if not master_password_verified:
        # Mostrar verificación
        from .password_forms import MasterPasswordVerificationForm
        
        if request.method == 'POST':
            form = MasterPasswordVerificationForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('master_password')
                MASTER_PASSWORD = get_master_password()
                
                if password == MASTER_PASSWORD:
                    request.session['master_password_verified_config'] = True
                    request.session.set_expiry(7200)  # 2 horas
                    messages.success(request, '✅ Verificación exitosa')
                    return redirect('system_configuration')
                else:
                    messages.error(request, '❌ Contraseña maestra incorrecta')
        else:
            form = MasterPasswordVerificationForm()
        
        return render(request, 'core/master_password_verification.html', {
            'form': form,
            'title': 'Verificación de Seguridad',
            'page_icon': '🔐'
        })
    
    # Manejo de formularios POST
    context = {'title': 'Configuración del Sistema'}
    
    if request.method == 'POST':
        action = request.POST.get('action')
        env_file = os.path.join(settings.BASE_DIR, '.env')
        
        # Leer archivo .env
        env_content = ''
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                env_content = f.read()
        
        # Cambiar contraseña maestra
        if action == 'change_master_password':
            current = request.POST.get('current_master_password', '')
            new_pass = request.POST.get('new_master_password', '')
            confirm = request.POST.get('confirm_master_password', '')
            
            if not current or not new_pass or not confirm:
                messages.error(request, '❌ Todos los campos son requeridos')
            elif len(new_pass) < 8:
                messages.error(request, '❌ La contraseña debe tener al menos 8 caracteres')
            elif new_pass != confirm:
                messages.error(request, '❌ Las contraseñas no coinciden')
            elif current != get_master_password():
                messages.error(request, '❌ Contraseña actual incorrecta')
            else:
                # Actualizar .env
                if 'MASTER_PASSWORD=' in env_content:
                    env_content = re.sub(r'MASTER_PASSWORD=.*', f'MASTER_PASSWORD={new_pass}', env_content)
                else:
                    env_content += f'\nMASTER_PASSWORD={new_pass}'
                
                with open(env_file, 'w') as f:
                    f.write(env_content)
                
                messages.success(request, '✅ Contraseña maestra actualizada exitosamente')
                print(f"[AUDITORIA] {request.user.username} cambió contraseña maestra - {timezone.now()}")
                return redirect('system_configuration')
        
        # Cambiar email
        elif action == 'change_email_config':
            email = request.POST.get('email_host_user', '').strip()
            password = request.POST.get('email_host_password', '').strip()
            
            if not email or not password:
                messages.error(request, '❌ Todos los campos son requeridos')
            elif '@gmail.com' not in email:
                messages.error(request, '❌ Solo se soporta Gmail (@gmail.com)')
            elif len(password) < 16:
                messages.error(request, '❌ La contraseña debe tener 16 caracteres')
            else:
                # Actualizar .env
                if 'EMAIL_HOST_USER=' in env_content:
                    env_content = re.sub(r'EMAIL_HOST_USER=.*', f'EMAIL_HOST_USER={email}', env_content)
                else:
                    env_content += f'\nEMAIL_HOST_USER={email}'
                
                if 'EMAIL_HOST_PASSWORD=' in env_content:
                    env_content = re.sub(r'EMAIL_HOST_PASSWORD=.*', f'EMAIL_HOST_PASSWORD={password}', env_content)
                else:
                    env_content += f'\nEMAIL_HOST_PASSWORD={password}'
                
                with open(env_file, 'w') as f:
                    f.write(env_content)
                
                messages.success(request, '✅ Email configurado exitosamente')
                print(f"[AUDITORIA] {request.user.username} cambió email config - {timezone.now()}")
                return redirect('system_configuration')
    
    # Obtener valores actuales
    current_email = os.getenv('EMAIL_HOST_USER', '')
    context['master_password_form'] = None
    context['email_form'] = None
    
    return render(request, 'core/system_configuration.html', context)
