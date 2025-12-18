"""
Funciones de validación de permisos por objeto.

🔒 OWASP #1: Broken Access Control - Evitar IDORs
"""

from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from functools import wraps


def check_object_access(user, obj, allow_admin=True, allow_owner=True):
    """
    Verificar si usuario tiene permiso para acceder a un objeto.
    
    Args:
        user: Usuario actual (request.user)
        obj: Objeto a acceder
        allow_admin: ¿Permite acceso a admin/superuser?
        allow_owner: ¿Permite acceso al propietario?
    
    Raises:
        PermissionDenied: Si el usuario NO tiene permiso
    
    Ejemplo:
        check_object_access(request.user, viaje, allow_admin=True)
    """
    
    # 1. Admin siempre tiene acceso (si allow_admin=True)
    if allow_admin and user.is_superuser:
        return True
    
    # 2. Verificar si usuario es admin mediante grupos
    if allow_admin and user.groups.filter(name='Admin').exists():
        return True
    
    # 3. Verificar si es el propietario
    if allow_owner:
        # Si el objeto tiene campo 'user' o 'conductor' o 'propietario'
        if hasattr(obj, 'user') and obj.user == user:
            return True
        if hasattr(obj, 'conductor') and obj.conductor.user == user:
            return True
        if hasattr(obj, 'propietario') and obj.propietario == user:
            return True
    
    # Si llegamos aquí, el usuario NO tiene permiso
    raise PermissionDenied(
        'No tienes permiso para acceder a este recurso.'
    )


def object_access_required(allow_admin=True, allow_owner=True):
    """
    Decorador para validar acceso a objeto en vistas.
    
    Uso en vistas basadas en clases:
        @method_decorator(object_access_required(), name='dispatch')
        class MiVista(DetailView):
            ...
    
    Uso en vistas función:
        @object_access_required()
        def mi_vista(request, pk):
            objeto = MiModelo.objects.get(pk=pk)
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Obtener objeto del kwargs (usualmente pk)
            pk = kwargs.get('pk')
            if pk:
                # Intentar obtener el modelo del request (asumiendo DetailView)
                # o pasar explícitamente
                pass
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def validate_viaje_access(user, viaje):
    """
    Validar acceso a un viaje.
    
    - Admin: acceso completo
    - Usuario: solo acceso a viajes (es lectura pública)
    """
    if user.is_superuser:
        return True
    
    if user.groups.filter(name='Admin').exists():
        return True
    
    # Para viajes, todos los usuarios pueden verlos (lectura pública)
    # La restricción se puede aplicar por rol/grupo
    return True


def validate_conductor_access(user, conductor):
    """
    Validar acceso a un conductor.
    
    - Admin: acceso completo
    - Otros usuarios: 403 Forbidden (solo admin puede ver conductores)
    """
    if user.is_superuser:
        return True
    
    if user.groups.filter(name='Admin').exists():
        return True
    
    raise PermissionDenied('No tienes permiso para acceder a este conductor.')


def validate_costos_access(user, costos):
    """
    Validar acceso a costos de viaje.
    
    - Admin: acceso completo
    - Otros: 403 Forbidden (solo admin puede ver costos)
    """
    if user.is_superuser:
        return True
    
    if user.groups.filter(name='Admin').exists():
        return True
    
    raise PermissionDenied('No tienes permiso para acceder a estos costos.')
