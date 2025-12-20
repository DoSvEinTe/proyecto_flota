@echo off
REM Verificación rápida de instalación
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════╗
echo ║  ✓ VERIFICACIÓN RÁPIDA - OPCIÓN 1            ║
echo ╚════════════════════════════════════════════════╝
echo.

echo ✓ Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Python encontrado
) else (
    echo   ❌ Python NO encontrado
    echo      Instala desde: https://www.python.org/
)

echo ✓ Checking files...
if exist INSTALAR.bat (echo   ✅ INSTALAR.bat) else (echo   ❌ INSTALAR.bat MISSING)
if exist EJECUTAR.bat (echo   ✅ EJECUTAR.bat) else (echo   ❌ EJECUTAR.bat MISSING)
if exist launcher.py (echo   ✅ launcher.py) else (echo   ❌ launcher.py MISSING)
if exist instalar.py (echo   ✅ instalar.py) else (echo   ❌ instalar.py MISSING)
if exist LEEME.txt (echo   ✅ LEEME.txt) else (echo   ❌ LEEME.txt MISSING)

echo.
echo ╔════════════════════════════════════════════════╗
echo ║  LISTO PARA USAR                              ║
echo ║  Ahora ejecuta: INSTALAR.bat                  ║
echo ╚════════════════════════════════════════════════╝
echo.

pause
