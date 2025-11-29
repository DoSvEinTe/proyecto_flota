from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """Decorador que verifica si el usuario es Admin"""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'No tienes permiso para acceder a esta sección. Se requiere acceso de Administrador.')
        return redirect('home')
    
    return wrapped_view


def usuario_or_admin_required(view_func):
    """Decorador que verifica si el usuario es Usuario o Admin"""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Usuario']).exists():
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('home')
    
    return wrapped_view


def get_user_role(user):
    """Retorna el rol del usuario: 'admin', 'usuario' o None"""
    if not user.is_authenticated:
        return None
    
    if user.is_superuser:
        return 'admin'
    
    if user.groups.filter(name='Admin').exists():
        return 'admin'
    
    if user.groups.filter(name='Usuario').exists():
        return 'usuario'
    
    return None


def can_view_section(user, section):
    """
    Verifica si un usuario puede ver una sección específica
    
    Secciones disponibles:
    - 'admin': Solo Admin
    - 'buses', 'conductores': Solo Admin
    - 'viajes', 'lugares', 'pasajeros': Admin y Usuario
    - 'home': Todos
    """
    if not user.is_authenticated:
        return False
    
    role = get_user_role(user)
    
    # Secciones solo para admin
    admin_only = ['buses', 'conductores', 'costos']
    
    # Secciones para admin y usuario
    shared = ['viajes', 'lugares', 'pasajeros', 'home']
    
    if section in admin_only:
        return role == 'admin'
    elif section in shared:
        return True
    
    return False
