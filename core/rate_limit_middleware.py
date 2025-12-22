"""
Middleware para manejar errores 403 de rate-limiting de forma elegante
"""
from django.shortcuts import render
from django.contrib import messages
from django_ratelimit.exceptions import Ratelimited


class RateLimitMiddleware:
    """Middleware para capturar errores de rate-limiting y mostrar mensaje amigable"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Ratelimited:
            # Capturar el error de rate-limiting
            if request.path == '/core/login/' or 'login' in request.path:
                from core.auth_views import LoginForm
                form = LoginForm()
                form.add_error(None, '❌ Demasiados intentos. Intenta en 15 minutos.')
                return render(request, 'auth/login.html', {
                    'form': form,
                    'ratelimited': True
                })
            return response
        
        # Si la respuesta es 403 y es un POST a login
        if response.status_code == 403 and request.method == 'POST' and 'login' in request.path:
            from core.auth_views import LoginForm
            form = LoginForm()
            form.add_error(None, '❌ Demasiados intentos. Intenta en 15 minutos.')
            return render(request, 'auth/login.html', {
                'form': form,
                'ratelimited': True
            }, status=200)
        
        return response
