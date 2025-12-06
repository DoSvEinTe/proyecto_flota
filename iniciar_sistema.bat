@echo off
echo ===================================
echo  SISTEMA DE GESTION DE FLOTA  
echo ===================================

echo.
echo 1. Aplicando migraciones...
python manage.py migrate

echo.
echo 2. Recolectando archivos estaticos...
python manage.py collectstatic --noinput

echo.
echo 3. Verificando instalacion...
python verificar_instalacion.py

echo.
echo 4. Iniciando servidor de desarrollo...
echo Puede acceder al sistema en: http://127.0.0.1:8000/
echo.
echo ===================================
echo     SISTEMA INICIADO
echo ===================================
echo.
python manage.py runserver

pause