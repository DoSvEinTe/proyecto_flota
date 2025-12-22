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

REM Ejecutar el launcher
echo ⏳ Cargando interfaz...
python launcher.py

pause
exit /b 0
