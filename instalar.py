#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSTALADOR AUTOMÁTICO - Sistema FlotaGest
Instala todas las dependencias automáticamente
"""

import subprocess
import sys
import os
from pathlib import Path

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y mostrar progreso"""
    print(f"\n{'='*60}")
    print(f"📦 {descripcion}")
    print(f"{'='*60}")
    
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=False,
            text=True
        )
        
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - COMPLETADO")
            return True
        else:
            print(f"❌ {descripcion} - ERROR")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def verificar_python():
    """Verificar que Python está instalado"""
    print("\n" + "="*60)
    print("🔍 Verificando Python...")
    print("="*60)
    
    try:
        version = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            text=True
        )
        print(f"✅ Python detectado: {version.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python no está instalado: {str(e)}")
        return False


def instalar_dependencias():
    """Instalar dependencias de pip"""
    proyecto_dir = Path(__file__).resolve().parent
    requirements_file = proyecto_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ No se encontró requirements.txt en {proyecto_dir}")
        return False
    
    comando = f"{sys.executable} -m pip install -r \"{requirements_file}\""
    return ejecutar_comando(comando, "Instalando dependencias Python")


def hacer_migraciones():
    """Hacer migraciones de Django"""
    proyecto_dir = Path(__file__).resolve().parent
    os.chdir(proyecto_dir)
    
    comando = f"{sys.executable} manage.py migrate"
    return ejecutar_comando(comando, "Aplicando migraciones de Django")


def recolectar_estaticos():
    """Recolectar archivos estáticos"""
    proyecto_dir = Path(__file__).resolve().parent
    os.chdir(proyecto_dir)
    
    comando = f"{sys.executable} manage.py collectstatic --noinput"
    return ejecutar_comando(comando, "Recolectando archivos estáticos")


def crear_archivo_env():
    """Crear archivo .env desde .env.example si no existe"""
    print("\n" + "="*60)
    print("🔧 Configurando archivo .env...")
    print("="*60)
    
    proyecto_dir = Path(__file__).resolve().parent
    env_file = proyecto_dir / '.env'
    env_example = proyecto_dir / '.env.example'
    
    # Si .env ya existe, no hacer nada
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    
    # Si .env.example existe, copiar
    if env_example.exists():
        try:
            with open(env_example, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print("✅ Archivo .env creado desde .env.example")
            return True
        except Exception as e:
            print(f"⚠️  Error al crear .env: {e}")
            return False
    else:
        print("⚠️  Archivo .env.example no encontrado")
        return False


def main():
    """Función principal del instalador"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "🚌 INSTALADOR - SISTEMA FLOTAGEST" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    # Paso 0: Crear archivo .env
    crear_archivo_env()
    
    # Paso 1: Verificar Python
    if not verificar_python():
        print("\n❌ Python no está instalado. Por favor instala Python 3.8+")
        input("Presiona Enter para salir...")
        return False
    
    # Paso 2: Instalar dependencias
    print("\n📥 Descargando e instalando dependencias...")
    print("   Esto puede tomar varios minutos...")
    
    if not instalar_dependencias():
        print("\n❌ Error al instalar dependencias")
        input("Presiona Enter para salir...")
        return False
    
    # Paso 3: Hacer migraciones
    print("\n🔄 Configurando base de datos...")
    if not hacer_migraciones():
        print("\n⚠️  Error en migraciones (puede ser normal si MySQL no está disponible)")
        print("   Configura MySQL e intenta nuevamente")
    
    # Paso 4: Recolectar estáticos
    print("\n📁 Configurando archivos...")
    recolectar_estaticos()
    
    # Paso 5: Crear usuarios por defecto
    print("\n👥 Creando usuarios por defecto...")
    proyecto_dir = Path(__file__).resolve().parent
    os.chdir(proyecto_dir)
    comando = f"{sys.executable} initialize_system.py"
    ejecutar_comando(comando, "Inicializando usuarios")
    
    # Resumen
    print("\n" + "="*60)
    print("✅ INSTALACIÓN COMPLETADA")
    print("="*60)
    print("\n📌 PRÓXIMOS PASOS:")
    print("\n1. Verifica que MySQL esté ejecutándose")
    print("   Abre: http://localhost/phpmyadmin (o similar)")
    print("\n2. Ejecuta el launcher.py:")
    print("   - Doble click en 'launcher.py'")
    print("   - O desde terminal: python launcher.py")
    print("\n3. Haz click en 'INICIAR SISTEMA'")
    print("\n4. Abre tu navegador en: http://127.0.0.1:8000/")
    print("\n" + "="*60)
    print("\n🔐 CREDENCIALES POR DEFECTO:")
    print("   Usuario: usuario / Contraseña: usuario123")
    print("   Admin: admin / Contraseña: admin123")
    print("="*60 + "\n")
    
    input("Presiona Enter para salir...")
    return True
    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        input("Presiona Enter para salir...")
