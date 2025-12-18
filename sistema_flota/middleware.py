"""
Middleware de logging y monitoreo para seguridad.

🔒 OWASP #9: Security Logging and Monitoring Failures
"""

import logging
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.contrib.auth import signals

logger = logging.getLogger('auth')
security_logger = logging.getLogger('django.security')


class SecurityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware que registra eventos de seguridad importantes.
    
    Qué registra:
    - Intentos fallidos de login
    - Accesos sin autorización (403)
    - Errores del servidor (500)
    - Rutas sensibles accedidas
    """
    
    RUTAS_SENSIBLES = [
        '/admin/',
        '/api/',
        '/costos/',
        '/flota/',
        '/core/',
    ]
    
    def process_response(self, request, response):
        """Registrar eventos después de procesar la respuesta"""
        
        # 1. Registrar errores 403 (Acceso denegado)
        if response.status_code == 403:
            security_logger.warning(
                f'Acceso denegado (403): {request.method} {request.path} | '
                f'IP: {self.get_client_ip(request)} | Usuario: {request.user.username or "Anónimo"}'
            )
        
        # 2. Registrar errores 500 (Error del servidor)
        if response.status_code == 500:
            security_logger.error(
                f'Error 500: {request.method} {request.path} | '
                f'IP: {self.get_client_ip(request)} | Usuario: {request.user.username or "Anónimo"}'
            )
        
        # 3. Registrar accesos a rutas sensibles
        if any(ruta in request.path for ruta in self.RUTAS_SENSIBLES):
            if response.status_code == 200:
                logger.info(
                    f'Acceso exitoso a ruta sensible: {request.method} {request.path} | '
                    f'Usuario: {request.user.username or "Anónimo"} | '
                    f'IP: {self.get_client_ip(request)}'
                )
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        """Obtener IP del cliente (considerando proxies)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    """
    Registrar intentos fallidos de login.
    Señal Django: user_login_failed
    """
    ip = get_client_ip_from_request(request)
    username = credentials.get('username', 'desconocido')
    
    logger.warning(
        f'Intento de login fallido | '
        f'Usuario: {username} | '
        f'IP: {ip}'
    )


@receiver(signals.user_logged_in)
def log_login_success(sender, request, user, **kwargs):
    """Registrar login exitoso"""
    ip = get_client_ip_from_request(request)
    
    logger.info(
        f'Login exitoso | '
        f'Usuario: {user.username} | '
        f'IP: {ip} | '
        f'Rol: {"Admin" if user.is_superuser else "Usuario"}'
    )


@receiver(signals.user_logged_out)
def log_logout(sender, request, user, **kwargs):
    """Registrar logout"""
    ip = get_client_ip_from_request(request)
    
    logger.info(
        f'Logout | '
        f'Usuario: {user.username if user else "Anónimo"} | '
        f'IP: {ip}'
    )


def get_client_ip_from_request(request):
    """Obtener IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
