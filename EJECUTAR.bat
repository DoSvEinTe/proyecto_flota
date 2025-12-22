@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         🚌 SISTEMA DE GESTIÓN DE FLOTA 🚌                ║
echo ║                                                            ║
echo ║    Iniciando el sistema, por favor espera...              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Ir al directorio del proyecto
cd /d "%~dp0"

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no se encuentra en PATH
    echo.
    echo Por favor:
    echo 1. Instala Python desde https://www.python.org
    echo 2. Durante la instalación, marca "Add Python to PATH"
    echo 3. Reinicia este script
    pause
    exit /b 1
)

REM Ejecutar el launcher
echo ⏳ Cargando interfaz...
python launcher.py

pause
exit /b 0
