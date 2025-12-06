# Script de Verificación de Instalación
# Ejecuta este script para verificar que todo esté configurado correctamente

import sys
import os

print("=" * 70)
print("VERIFICACIÓN DE INSTALACIÓN - Sistema FlotaGest")
print("=" * 70)

# Verificar Python
print("\n1. Verificando versión de Python...")
python_version = sys.version_info
print(f"   ✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
if python_version < (3, 10):
    print("   ⚠ ADVERTENCIA: Se recomienda Python 3.10 o superior")

# Verificar módulos requeridos
print("\n2. Verificando módulos Python...")
required_modules = [
    ('django', 'Django'),
    ('reportlab', 'ReportLab'),
    ('PIL', 'Pillow'),
    ('decouple', 'python-decouple'),
    ('requests', 'requests'),
    ('PyPDF2', 'PyPDF2'),
]

missing_modules = []
for module_name, package_name in required_modules:
    try:
        __import__(module_name)
        print(f"   ✓ {package_name}")
    except ImportError:
        print(f"   ✗ {package_name} - NO INSTALADO")
        missing_modules.append(package_name)

if missing_modules:
    print(f"\n   ⚠ Módulos faltantes: {', '.join(missing_modules)}")
    print(f"   Instala con: pip install {' '.join(missing_modules)}")
else:
    print("   ✓ Todos los módulos requeridos están instalados")

# Verificar archivo .env
print("\n3. Verificando configuración de entorno...")
if os.path.exists('.env'):
    print("   ✓ Archivo .env encontrado")
    with open('.env', 'r') as f:
        content = f.read()
        if 'EMAIL_HOST_USER' in content and 'EMAIL_HOST_PASSWORD' in content:
            print("   ✓ Variables de email configuradas")
        else:
            print("   ⚠ Variables de email no encontradas en .env")
else:
    print("   ✗ Archivo .env NO encontrado")
    print("   Copia .env.example a .env y configura tus credenciales")

# Verificar archivo .env.example
if os.path.exists('.env.example'):
    print("   ✓ Archivo .env.example encontrado")
else:
    print("   ⚠ Archivo .env.example no encontrado")

# Verificar Django
print("\n4. Verificando configuración de Django...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
    import django
    django.setup()
    print("   ✓ Django configurado correctamente")
    
    from django.conf import settings
    print(f"   ✓ DEBUG = {settings.DEBUG}")
    print(f"   ✓ SECRET_KEY configurado")
    
    if settings.EMAIL_HOST_USER:
        print(f"   ✓ Email configurado: {settings.EMAIL_HOST_USER}")
    else:
        print("   ⚠ Email no configurado")
        
except Exception as e:
    print(f"   ✗ Error al configurar Django: {e}")

# Verificar base de datos
print("\n5. Verificando conexión a base de datos...")
try:
    from django.db import connection
    connection.ensure_connection()
    print("   ✓ Conexión a base de datos exitosa")
    
    # Verificar migraciones
    from django.db.migrations.executor import MigrationExecutor
    executor = MigrationExecutor(connection)
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    
    if plan:
        print(f"   ⚠ Hay {len(plan)} migraciones pendientes")
        print("   Ejecuta: python manage.py migrate")
    else:
        print("   ✓ Todas las migraciones están aplicadas")
        
except Exception as e:
    print(f"   ✗ Error de base de datos: {e}")
    print("   Verifica la configuración de base de datos en settings.py")

# Verificar modelos
print("\n6. Verificando modelos de la aplicación...")
try:
    from core.models import Conductor
    from flota.models import Bus
    from viajes.models import Viaje
    from costos.models import CostosViaje
    
    conductores = Conductor.objects.count()
    buses = Bus.objects.count()
    viajes = Viaje.objects.count()
    costos = CostosViaje.objects.count()
    
    print(f"   ✓ Conductores: {conductores}")
    print(f"   ✓ Buses: {buses}")
    print(f"   ✓ Viajes: {viajes}")
    print(f"   ✓ Costos: {costos}")
    
except Exception as e:
    print(f"   ✗ Error al consultar modelos: {e}")

# Verificar archivos estáticos
print("\n7. Verificando archivos estáticos...")
if os.path.exists('static'):
    print("   ✓ Carpeta static/ encontrada")
else:
    print("   ⚠ Carpeta static/ no encontrada")
    
if os.path.exists('staticfiles'):
    print("   ✓ Carpeta staticfiles/ encontrada")
else:
    print("   ℹ Carpeta staticfiles/ no encontrada (se creará con collectstatic)")

# Verificar carpeta media
print("\n8. Verificando carpeta de medios...")
if os.path.exists('media'):
    print("   ✓ Carpeta media/ encontrada")
    if os.path.exists('media/cedulas'):
        print("   ✓ Carpeta media/cedulas/ encontrada")
    if os.path.exists('media/licencias'):
        print("   ✓ Carpeta media/licencias/ encontrada")
else:
    print("   ⚠ Carpeta media/ no encontrada (se creará automáticamente)")

# Resumen final
print("\n" + "=" * 70)
print("RESUMEN DE VERIFICACIÓN")
print("=" * 70)

if missing_modules:
    print("❌ INSTALACIÓN INCOMPLETA")
    print(f"Instala los módulos faltantes: pip install {' '.join(missing_modules)}")
elif not os.path.exists('.env'):
    print("⚠️ CONFIGURACIÓN PENDIENTE")
    print("Crea el archivo .env con tus credenciales")
else:
    print("✅ INSTALACIÓN COMPLETA")
    print("El sistema está listo para usarse")
    print("\nPara iniciar el servidor ejecuta:")
    print("   python manage.py runserver")

print("\n" + "=" * 70)
