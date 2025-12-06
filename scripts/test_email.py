"""
Script para probar la configuración de email.
Ejecuta: python scripts/test_email.py
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("=" * 60)
    print("PRUEBA DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    print(f"\n📧 Configuración actual:")
    print(f"   HOST: {settings.EMAIL_HOST}")
    print(f"   PORT: {settings.EMAIL_PORT}")
    print(f"   USER: {settings.EMAIL_HOST_USER}")
    print(f"   USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   FROM: {settings.DEFAULT_FROM_EMAIL}")
    
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ ERROR: Variables de entorno EMAIL_HOST_USER o EMAIL_HOST_PASSWORD no configuradas")
        print("\n💡 Configúralas con:")
        print('   $env:EMAIL_HOST_USER = "tu_correo@gmail.com"')
        print('   $env:EMAIL_HOST_PASSWORD = "tu_contraseña_de_aplicacion"')
        return
    
    print("\n📤 Enviando email de prueba...")
    
    try:
        send_mail(
            subject='Prueba - Sistema FlotaGest',
            message='Este es un email de prueba del sistema FlotaGest.\n\nSi recibes este mensaje, la configuración de email funciona correctamente. ✅',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("\n✅ ¡Email enviado exitosamente!")
        print(f"   Revisa la bandeja de entrada de: {settings.EMAIL_HOST_USER}")
        
    except Exception as e:
        print(f"\n❌ Error al enviar email: {str(e)}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que la contraseña de aplicación sea correcta (sin espacios)")
        print("   2. Asegúrate de tener activada la verificación en 2 pasos en Gmail")
        print("   3. Verifica tu conexión a internet")

if __name__ == '__main__':
    test_email()
