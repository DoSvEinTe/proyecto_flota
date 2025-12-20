@echo off
REM =======================================================
REM Script de bienvenida - Se ejecuta tras descargar
REM =======================================================

chcp 65001 >nul
cls

color 0A

echo.
echo.
echo  ╔════════════════════════════════════════════════════╗
echo  ║                                                    ║
echo  ║      🚌 BIENVENIDO - SISTEMA FLOTAGEST 🚌        ║
echo  ║                                                    ║
echo  ║  Tu proyecto está listo para ejecutarse           ║
echo  ║                                                    ║
echo  ╚════════════════════════════════════════════════════╝
echo.

timeout /t 2 /nobreak

echo.
echo  ✅ Este es un sistema de gestión de flota de buses
echo.
echo  📋 Documentación disponible:
echo.
echo     • LEEME.txt .................... Guía principal
echo     • INICIO_RAPIDO.txt ............ 3 pasos rápidos
echo     • INDICE_INSTALACION.txt ....... Archivo completo
echo.

timeout /t 3 /nobreak

echo.
echo  🎯 Para comenzar:
echo.
echo     1. Abre el archivo: INICIO_RAPIDO.txt
echo     2. Sigue las instrucciones paso a paso
echo     3. Ejecuta INSTALAR.bat (primera vez)
echo     4. Ejecuta EJECUTAR.bat (cada sesión)
echo.

timeout /t 3 /nobreak

echo.
echo  ⏳ Presiona ENTER para cerrar esta ventana...
echo.

pause >nul

cls
