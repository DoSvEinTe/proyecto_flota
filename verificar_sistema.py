#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICADOR DE INSTALACIÓN - Sistema FlotaGest
Verifica que todo está correctamente instalado
"""

import subprocess
import sys
import os
from pathlib import Path

def verificar_python():
    """Verificar Python"""
    print("\n✓ Verificando Python...", end=" ")
    try:
        version = sys.version.split()[0]
        print(f"OK (v{version})")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def verificar_pip():
    """Verificar pip"""
    print("✓ Verificando pip...", end=" ")
    try:
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True
        )
        if resultado.returncode == 0:
            print("OK")
            return True
        else:
            print("ERROR")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def verificar_django():
    """Verificar Django"""
    print("✓ Verificando Django...", end=" ")
    try:
        import django
        print(f"OK (v{django.VERSION[0]}.{django.VERSION[1]})")
        return True
    except ImportError:
        print("NO INSTALADO")
        return False


def verificar_mysqlclient():
    """Verificar mysqlclient"""
    print("✓ Verificando mysqlclient...", end=" ")
    try:
        import MySQLdb
        print("OK")
        return True
    except ImportError:
        print("NO INSTALADO")
        return False


def verificar_pillow():
    """Verificar Pillow"""
    print("✓ Verificando Pillow...", end=" ")
    try:
        import PIL
        print("OK")
        return True
    except ImportError:
        print("NO INSTALADO")
        return False


def verificar_dotenv():
    """Verificar python-dotenv"""
    print("✓ Verificando python-dotenv...", end=" ")
    try:
        import dotenv
        print("OK")
        return True
    except ImportError:
        print("NO INSTALADO")
        return False


def verificar_mysql_conexion():
    """Verificar conexión a MySQL"""
    print("✓ Verificando conexión MySQL...", end=" ")
    try:
        import MySQLdb
        
        conexion = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="Contra.12"
        )
        conexion.close()
        print("OK")
        return True
    except Exception as e:
        print(f"ERROR ({str(e)[:30]}...)")
        print("  → Verifica que MySQL esté ejecutándose")
        print("  → Usuario: root, Contraseña: Contra.12")
        return False


def verificar_archivo_env():
    """Verificar archivo .env"""
    print("✓ Verificando archivo .env...", end=" ")
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print("OK")
        return True
    else:
        print("NO ENCONTRADO")
        print("  → Crea un archivo .env en la raíz del proyecto")
        return False


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🔍 VERIFICADOR DE INSTALACIÓN - Sistema FlotaGest")
    print("="*60)
    
    resultados = {
        "Python": verificar_python(),
        "pip": verificar_pip(),
        ".env": verificar_archivo_env(),
    }
    
    print("\n--- Librerías Requeridas ---")
    resultados["Django"] = verificar_django()
    resultados["mysqlclient"] = verificar_mysqlclient()
    resultados["Pillow"] = verificar_pillow()
    resultados["python-dotenv"] = verificar_dotenv()
    
    print("\n--- Conexiones Externas ---")
    resultados["MySQL"] = verificar_mysql_conexion()
    
    # Resumen
    print("\n" + "="*60)
    total = len(resultados)
    correctas = sum(1 for v in resultados.values() if v)
    
    print(f"\n📊 RESULTADO: {correctas}/{total} componentes OK\n")
    
    if correctas == total:
        print("✅ TODO ESTÁ LISTO - ¡Puedes ejecutar el sistema!")
        print("\nEjecuta: python launcher.py")
    else:
        print("⚠️  FALTAN COMPONENTES")
        print("\nComponentes faltantes:")
        for nombre, ok in resultados.items():
            if not ok:
                print(f"   - {nombre}")
        print("\nEjecuta: INSTALAR.bat")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        input("\nPresiona Enter para salir...")
