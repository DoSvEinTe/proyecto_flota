@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║  GENERADOR DE EXE - Sistema FlotaGest                    ║
echo ║                                                            ║
echo ║  Este script crea un EXE para distribuir el sistema       ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado
    echo Por favor instala Python desde: https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python detectado

REM Instalar PyInstaller
echo.
echo 📦 Instalando PyInstaller...
python -m pip install pyinstaller

if %errorlevel% neq 0 (
    echo ❌ Error al instalar PyInstaller
    pause
    exit /b 1
)

echo ✅ PyInstaller instalado

REM Ir al directorio del proyecto
cd /d "%~dp0"

REM Crear el EXE
echo.
echo 🔨 Generando EXE...
echo Esto puede tomar 1-2 minutos...
echo.

pyinstaller --onefile --windowed --name "FlotaGest" --distpath ".\dist" launcher.py

if %errorlevel% neq 0 (
    echo ❌ Error al generar EXE
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          ✅ EXE GENERADO CORRECTAMENTE                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📁 El archivo se encuentra en: dist\FlotaGest.exe
echo.
echo 📋 Para distribuir:
echo    1. Copia la carpeta del proyecto completa
echo    2. Incluye el archivo: dist\FlotaGest.exe
echo    3. Incluye el archivo: INSTALAR.bat
echo    4. Usuarios ejecutan INSTALAR.bat primero
echo    5. Luego ejecutan FlotaGest.exe
echo.

pause
exit /b 0
