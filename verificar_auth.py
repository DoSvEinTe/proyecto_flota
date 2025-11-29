import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("\n" + "="*60)
print("✓ USUARIOS CREADOS EN EL SISTEMA")
print("="*60)
for user in User.objects.all():
    role = "SUPERUSER (ADMIN)" if user.is_superuser else user.groups.all()[0].name if user.groups.all() else "SIN GRUPO"
    print(f"  • {user.username:15} | {role:20} | Email: {user.email}")

print("\n" + "="*60)
print("✓ GRUPOS DE ACCESO")
print("="*60)
for group in Group.objects.all():
    print(f"  • {group.name}")

print("\n" + "="*60)
print("✓ CONFIGURACIÓN COMPLETADA")
print("="*60)
print("""
CREDENCIALES DE PRUEBA:

ADMINISTRADOR:
  Usuario: admin
  Contraseña: admin123
  Acceso: ✓ Completo (Buses, Conductores, Viajes, Lugares, Pasajeros)

USUARIO REGULAR:
  Usuario: usuario
  Contraseña: usuario123
  Acceso: ✓ Limitado (Solo Viajes, Lugares, Pasajeros - Lectura y Creación)

""")
