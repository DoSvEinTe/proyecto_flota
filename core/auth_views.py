from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django import forms


class LoginForm(forms.Form):
    """Formulario personalizado de login"""
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password'
        })
    )


@ratelimit(key='ip', rate='5/15m', method='POST', block=True)
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista de login con protección contra brute-force.
    
    🔒 OWASP #7: Identification and Authentication Failures
    - Máximo 5 intentos por 15 minutos por IP
    - Después, se bloquea la IP por 15 minutos
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {user.first_name or user.username}!')
                return redirect('home')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
                messages.warning(request, 'Intento de login fallido. Máximo 5 intentos en 15 minutos.')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


@login_required(login_url='login')
@require_http_methods(["POST"])
def logout_view(request):
    """Vista de logout"""
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    """Dashboard principal después del login"""
    return redirect('home')
