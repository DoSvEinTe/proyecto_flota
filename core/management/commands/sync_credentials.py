"""
Comando para sincronizar credenciales del .env con la base de datos
Ejecutar: python manage.py sync_credentials
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Sincroniza credenciales de .env con la base de datos'

    def handle(self, *args, **options):
        print("\n" + "=" * 60)
        print("🔄 Sincronizando credenciales de .env con BD...")
        print("=" * 60)
        
        # Obtener credenciales del .env
        admin_username = config('DEFAULT_ADMIN_USERNAME', default='admin')
        admin_password = config('DEFAULT_ADMIN_PASSWORD', default='admin123')
        admin_email = config('DEFAULT_ADMIN_EMAIL', default='admin@example.com')
        
        user_username = config('DEFAULT_USER_USERNAME', default='usuario')
        user_password = config('DEFAULT_USER_PASSWORD', default='usuario123')
        user_email = config('DEFAULT_USER_EMAIL', default='usuario@example.com')
        
        # Sincronizar usuario regular
        try:
            user = User.objects.get(username=user_username)
            user.set_password(user_password)
            user.email = user_email
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Usuario '{user_username}' sincronizado"
                )
            )
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=user_username,
                email=user_email,
                password=user_password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Usuario '{user_username}' creado"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Error con usuario '{user_username}': {e}"
                )
            )
        
        # Sincronizar administrador
        try:
            admin = User.objects.get(username=admin_username)
            admin.set_password(admin_password)
            admin.email = admin_email
            admin.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Admin '{admin_username}' sincronizado"
                )
            )
        except User.DoesNotExist:
            admin = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Admin '{admin_username}' creado"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Error con admin '{admin_username}': {e}"
                )
            )
        
        print("\n" + "=" * 60)
        print("✅ Sincronización completada")
        print("=" * 60)
        print(f"\n🔐 Credenciales actuales en .env:\n")
        print(f"   Usuario regular:")
        print(f"      - Usuario: {user_username}")
        print(f"      - Contraseña: {user_password}")
        print(f"\n   Administrador:")
        print(f"      - Usuario: {admin_username}")
        print(f"      - Contraseña: {admin_password}\n")
