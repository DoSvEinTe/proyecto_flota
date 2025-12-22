"""
Comando para inicializar usuarios por defecto desde .env
Uso: python manage.py initialize_default_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Inicializa usuarios por defecto desde las variables de entorno'

    def handle(self, *args, **options):
        # Obtener configuraciones del .env
        default_user_username = config('DEFAULT_USER_USERNAME', default='usuario')
        default_user_password = config('DEFAULT_USER_PASSWORD', default='usuario123')
        default_user_email = config('DEFAULT_USER_EMAIL', default='usuario@example.com')
        
        default_admin_username = config('DEFAULT_ADMIN_USERNAME', default='admin')
        default_admin_password = config('DEFAULT_ADMIN_PASSWORD', default='admin123')
        default_admin_email = config('DEFAULT_ADMIN_EMAIL', default='admin@example.com')
        
        # Crear usuario regular si no existe
        if not User.objects.filter(username=default_user_username).exists():
            user = User.objects.create_user(
                username=default_user_username,
                email=default_user_email,
                password=default_user_password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Usuario regular creado: {default_user_username}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️ Usuario regular ya existe: {default_user_username}'
                )
            )
        
        # Crear usuario administrador si no existe
        if not User.objects.filter(username=default_admin_username).exists():
            admin = User.objects.create_superuser(
                username=default_admin_username,
                email=default_admin_email,
                password=default_admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Administrador creado: {default_admin_username}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️ Administrador ya existe: {default_admin_username}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Inicialización de usuarios completada'
            )
        )
