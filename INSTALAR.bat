@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         🚌 INSTALADOR SISTEMA FLOTAGEST 🚌                ║
echo ║                                                            ║
echo ║    Este script instalará todas las dependencias de:       ║
echo ║    - Python                                               ║
echo ║    - Django y librerías necesarias                        ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no se encuentra en PATH
    echo.
    echo Por favor instala Python desde: https://www.python.org/
    echo Recuerda marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Ir al directorio del proyecto
cd /d "%~dp0"

REM Ejecutar el instalador Python
echo Iniciando instalación de dependencias...
echo.
python instalar.py

pause
exit /b 0
