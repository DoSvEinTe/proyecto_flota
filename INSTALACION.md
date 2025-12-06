# Guía de Instalación - Sistema FlotaGest

Esta guía te ayudará a configurar el proyecto en cualquier PC desde cero.

## Requisitos Previos

- Python 3.12 o superior
- MySQL 8.0 o superior
- Git (opcional, para clonar el repositorio)

## Pasos de Instalación

### 1. Clonar o Copiar el Proyecto

```bash
# Si usas Git
git clone <url-del-repositorio>
cd proyecto_flota

# O simplemente copia la carpeta proyecto_flota a tu PC
```

### 2. Crear Entorno Virtual

**En Windows (PowerShell):**
```powershell
# Navega a la carpeta del proyecto
cd C:\ruta\a\proyecto_flota

# Crea el entorno virtual
python -m venv venv

# Activa el entorno virtual
.\venv\Scripts\Activate.ps1
```

**En Linux/Mac:**
```bash
# Crea el entorno virtual
python3 -m venv venv

# Activa el entorno virtual
source venv/bin/activate
```

### 3. Instalar Dependencias

Con el entorno virtual activado:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota**: Si `mysqlclient` da problemas en Windows, instala primero:
- Visual Studio Build Tools
- MySQL Connector/C

**Alternativa para Windows:**
```powershell
pip install mysqlclient-windows
```

### 4. Configurar Base de Datos

**Crear base de datos en MySQL:**

```sql
CREATE DATABASE flota_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'flota_user'@'localhost' IDENTIFIED BY 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON flota_db.* TO 'flota_user'@'localhost';
FLUSH PRIVILEGES;
```

**Verificar conexión:**
```bash
mysql -u flota_user -p flota_db
```

### 5. Configurar Variables de Entorno

**Crear archivo `.env` en la raíz del proyecto:**

```bash
# Copia el archivo de ejemplo
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac
```

**Edita `.env` con tus datos:**

```env
# Configuración de Email para Gmail
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion

# Base de datos (opcional si quieres usar variables de entorno)
DB_NAME=flota_db
DB_USER=flota_user
DB_PASSWORD=tu_contraseña_segura
DB_HOST=localhost
DB_PORT=3306
```

**Para obtener contraseña de aplicación de Gmail:**
1. Ve a https://myaccount.google.com/
2. Seguridad → Verificación en 2 pasos (actívala)
3. Contraseñas de aplicaciones
4. Genera una contraseña para "Correo"
5. Copia la contraseña (sin espacios) al `.env`

### 6. Ejecutar Migraciones

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones y proporciona:
- Nombre de usuario
- Email
- Contraseña

### 8. Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 9. Verificar Instalación

```bash
# Verificar que no haya errores
python manage.py check

# Resultado esperado:
# System check identified no issues (0 silenced).
```

### 10. Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

Abre tu navegador en: http://127.0.0.1:8000/

## Verificación de Funcionalidades

### ✅ Checklist de Pruebas

1. **Login y Autenticación**
   - [ ] Iniciar sesión con superusuario
   - [ ] Cerrar sesión

2. **Módulo Core**
   - [ ] Crear conductor con email válido
   - [ ] Subir fotos de cédula y licencia

3. **Módulo Flota**
   - [ ] Crear bus
   - [ ] Ver lista de buses

4. **Módulo Viajes**
   - [ ] Crear viaje
   - [ ] Ver detalles de viaje
   - [ ] Sistema calcula distancia automáticamente

5. **Módulo Costos**
   - [ ] Registrar costos de viaje
   - [ ] Ver gestión de costos
   - [ ] Descargar PDF formulario
   - [ ] **Enviar PDF por email** (botón verde "Email")
   - [ ] Generar informe de costos

## Solución de Problemas Comunes

### Error: "No module named 'decouple'"
```bash
pip install python-decouple
```

### Error: "No module named 'requests'"
```bash
pip install requests
```

### Error: "No module named 'reportlab'"
```bash
pip install reportlab
```

### Error: "Authentication failed" al enviar email
- Verifica que la contraseña de aplicación esté correcta en `.env`
- Asegúrate de tener activada la verificación en 2 pasos en Gmail
- Reinicia el servidor Django después de cambiar `.env`

### Error: "mysqlclient" en Windows
1. Descarga e instala: https://www.mysql.com/products/connector/
2. O usa: `pip install mysqlclient-windows`

### Error: "Access denied" en MySQL
- Verifica usuario y contraseña
- Asegúrate de haber creado la base de datos
- Verifica los permisos con `SHOW GRANTS FOR 'flota_user'@'localhost';`

## Estructura de Archivos Importantes

```
proyecto_flota/
├── .env                          # ❗ Configuración sensible (NO subir a Git)
├── .env.example                  # Plantilla de configuración
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias del proyecto
├── manage.py                     # Comando principal de Django
├── db.sqlite3                    # Base de datos (si usas SQLite)
├── README.md                     # Documentación principal
├── CONFIGURACION_EMAIL.md        # Guía de configuración de email
├── SOLUCION_ERROR_EMAIL.md       # Solución de errores de email
│
├── sistema_flota/
│   ├── settings.py               # Configuración principal
│   ├── urls.py                   # URLs principales
│   └── wsgi.py                   # Configuración WSGI
│
├── core/                         # Conductores y autenticación
├── flota/                        # Gestión de buses
├── viajes/                       # Gestión de viajes
├── costos/                       # Gestión de costos
│   ├── views.py                  # Incluye función de envío de email
│   ├── informe_costos.py         # Generación de informes PDF
│   └── urls.py                   # URLs de costos
│
├── templates/                    # Plantillas HTML
├── static/                       # Archivos estáticos (CSS, JS)
├── media/                        # Archivos subidos (cédulas, licencias)
└── scripts/
    └── test_email.py             # Script de prueba de email
```

## Comandos Útiles

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1    # Windows
source venv/bin/activate        # Linux/Mac

# Desactivar entorno virtual
deactivate

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Crear migraciones después de cambios en models.py
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario adicional
python manage.py createsuperuser

# Ejecutar shell de Django
python manage.py shell

# Verificar configuración
python manage.py check

# Probar envío de email
python scripts/test_email.py

# Iniciar servidor
python manage.py runserver

# Iniciar servidor en puerto diferente
python manage.py runserver 8080

# Iniciar servidor accesible desde red
python manage.py runserver 0.0.0.0:8000
```

## Despliegue en Producción

### Variables de Entorno Adicionales

```env
DEBUG=False
SECRET_KEY=genera_una_clave_secreta_nueva
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

### Servidor Web Recomendado

```bash
# Con Gunicorn
gunicorn sistema_flota.wsgi:application --bind 0.0.0.0:8000

# Con Nginx como proxy inverso
# Configurar Nginx para servir archivos estáticos y hacer proxy a Gunicorn
```

## Mantenimiento

### Backup de Base de Datos

```bash
# MySQL
mysqldump -u flota_user -p flota_db > backup_$(date +%Y%m%d).sql

# Restaurar
mysql -u flota_user -p flota_db < backup_20251205.sql
```

### Actualizar Dependencias

```bash
pip list --outdated
pip install --upgrade <paquete>
pip freeze > requirements.txt
```

## Seguridad

### ❗ IMPORTANTE - NO SUBIR A GIT:
- `.env` (contraseñas y claves)
- `db.sqlite3` (si contiene datos reales)
- `media/` (cédulas y licencias de conductores)
- `__pycache__/` (archivos temporales)

### ✅ Verificar antes de commit:
```bash
git status
# Asegúrate de que .env no aparezca
```

## Soporte

- Documentación adicional en carpeta `docs/`
- Archivos de referencia en `docs/referencias/`
- Reportes de funcionalidades en `docs/reportes/`

## Notas de Versión

- **Python**: 3.12+
- **Django**: 5.0+
- **MySQL**: 8.0+
- **ReportLab**: 4.0+

## Contacto

Sistema desarrollado para FlotaGest
Fecha: Diciembre 2025
