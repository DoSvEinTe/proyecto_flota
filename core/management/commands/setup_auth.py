from django.core.management.base import BaseCommand
from django.db import transaction

from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Crea los usuarios y grupos de autenticación de prueba (admin/usuario).'

    @transaction.atomic
    def handle(self, *args, **options):
        # Crear grupos
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        usuario_group, _ = Group.objects.get_or_create(name='Usuario')

        self.stdout.write('✓ Grupos creados/actualizados')

        # Crear usuario administrador
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@flota.local',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema'
            )
            admin_user.groups.add(admin_group)
            self.stdout.write('✓ Usuario ADMIN creado: usuario=admin, contraseña=admin123')
        else:
            self.stdout.write('- Usuario ADMIN ya existe')

        # Crear usuario regular
        if not User.objects.filter(username='usuario').exists():
            regular_user = User.objects.create_user(
                username='usuario',
                email='usuario@flota.local',
                password='usuario123',
                first_name='Usuario',
                last_name='Regular'
            )
            regular_user.groups.add(usuario_group)
            self.stdout.write('✓ Usuario USUARIO creado: usuario=usuario, contraseña=usuario123')
        else:
            self.stdout.write('- Usuario USUARIO ya existe')

        self.stdout.write(self.style.SUCCESS('\n✓ Inicialización completada exitosamente'))
