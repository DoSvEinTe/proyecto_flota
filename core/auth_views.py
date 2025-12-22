from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django import forms


class LoginForm(forms.Form):
    """Formulario personalizado de login"""
    LOGIN_CHOICES = [
        ('usuario', '👤 Iniciar como Usuario'),
        ('admin', '👨‍💼 Iniciar como Admin'),
    ]
    
    login_type = forms.ChoiceField(
        label='Tipo de Inicio de Sesión',
        choices=LOGIN_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        initial='usuario'
    )
    
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'username'
        }),
        required=True
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password'
        })
    )

    def clean(self):
        """Validar dinámicamente según el tipo de login"""
        cleaned_data = super().clean()
        login_type = cleaned_data.get('login_type')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        # Para ambas opciones, username y password son requeridos
        if not username:
            self.add_error('username', 'Este campo es obligatorio')
        if not password:
            self.add_error('password', 'Este campo es obligatorio')
        
        return cleaned_data


@ratelimit(key='ip', rate='5/15m', method='POST', block=False)
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista de login con protección contra brute-force.
    Soporta 2 tipos de login:
    1. Usuario normal - autenticación solo con su contraseña personal
    2. Admin - puede usar su contraseña personal O contraseña maestra
    
    🔒 OWASP #7: Identification and Authentication Failures
    - Máximo 5 intentos por 15 minutos por IP
    - Después, se bloquea la IP por 15 minutos
    """
    from django.conf import settings
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            login_type = form.cleaned_data['login_type']
            
            # Obtener usuario por username
            user = User.objects.filter(username=username).first()
            
            if login_type == 'usuario':
                # OPCIÓN 1: Usuario normal - solo con su contraseña
                if user and user.check_password(password):
                    # Verificar que NO sea admin
                    if user.is_staff or user.is_superuser:
                        form.add_error(None, '❌ Este usuario es administrador. Usa la opción "Iniciar como Admin"')
                    else:
                        # Login exitoso como usuario normal
                        login(request, user)
                        messages.success(request, f'✅ ¡Bienvenido!')
                        return redirect('home')
                else:
                    form.add_error(None, '❌ Usuario o contraseña incorrectos')
            
            elif login_type == 'admin':
                # OPCIÓN 2: Admin - solo con su contraseña personal
                if not user:
                    form.add_error(None, '❌ Usuario no encontrado')
                elif not (user.is_staff or user.is_superuser):
                    form.add_error(None, '❌ Este usuario no tiene permisos de administrador')
                elif user.check_password(password):
                    # Login exitoso como admin
                    login(request, user)
                    messages.success(request, f'✅ ¡Bienvenido Admin!')
                    return redirect('home')
                else:
                    form.add_error(None, '❌ Contraseña incorrecta')
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
