#!/usr/bin/env python
"""
Script para inicializar el sistema con usuarios y datos por defecto
Ejecutar después de las migraciones:
    python initialize_system.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from django.contrib.auth.models import User
from decouple import config

def initialize_users():
    """Inicializa usuarios por defecto"""
    print("=" * 60)
    print("Inicializando usuarios por defecto...")
    print("=" * 60)
    
    # Configuraciones del .env
    default_user_username = config('DEFAULT_USER_USERNAME', default='usuario')
    default_user_password = config('DEFAULT_USER_PASSWORD', default='usuario123')
    default_user_email = config('DEFAULT_USER_EMAIL', default='usuario@example.com')
    
    default_admin_username = config('DEFAULT_ADMIN_USERNAME', default='admin')
    default_admin_password = config('DEFAULT_ADMIN_PASSWORD', default='admin123')
    default_admin_email = config('DEFAULT_ADMIN_EMAIL', default='admin@example.com')
    
    # Crear usuario regular
    if not User.objects.filter(username=default_user_username).exists():
        User.objects.create_user(
            username=default_user_username,
            email=default_user_email,
            password=default_user_password
        )
        print(f"✅ Usuario regular creado: {default_user_username}")
    else:
        print(f"⚠️  Usuario regular ya existe: {default_user_username}")
    
    # Crear administrador
    if not User.objects.filter(username=default_admin_username).exists():
        User.objects.create_superuser(
            username=default_admin_username,
            email=default_admin_email,
            password=default_admin_password
        )
        print(f"✅ Administrador creado: {default_admin_username}")
    else:
        print(f"⚠️  Administrador ya existe: {default_admin_username}")
    
    print("\n" + "=" * 60)
    print("🎉 Inicialización completada")
    print("=" * 60)
    print(f"""
Credenciales para iniciar sesión:

👤 Usuario Regular:
   - Usuario: {default_user_username}
   - Contraseña: {default_user_password}

👨‍💼 Administrador:
   - Usuario: {default_admin_username}
   - Contraseña: {default_admin_password}

🔐 Contraseña Maestra (para configuración):
   - {config('MASTER_PASSWORD', default='admin123')}
    """)

if __name__ == '__main__':
    try:
        initialize_users()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
