# 🚌 Sistema FlotaGest - Gestión de Flota de Buses

Sistema completo de gestión de flota de buses desarrollado con Django, que incluye gestión de conductores, buses, viajes y costos operacionales.

## 🌟 Características Principales

### 👥 Gestión de Conductores
- Registro completo con datos personales
- Upload de documentos (cédula y licencia de conducir)
- Gestión de correos electrónicos para notificaciones
- Control de licencias habilitadas

### 🚍 Gestión de Buses
- Registro de vehículos con detalles técnicos
- Control de capacidad de pasajeros
- Seguimiento de estado y disponibilidad
- Historial de mantenimientos

### 🗺️ Gestión de Viajes
- Creación de viajes con origen y destino
- Cálculo automático de distancia usando API de rutas
- Asignación de conductores y buses
- Estados de viaje (Programado, En Curso, Completado, Cancelado)
- Registro de pasajeros

### 💰 Gestión de Costos
- Registro detallado de costos por viaje:
  - Combustible (puntos de recarga múltiples)
  - Peajes
  - Mantenimientos
  - Otros costos operacionales
- Cálculo automático de totales
- **Generación de formularios PDF editables**
- **Envío automático por email a conductores**
- Informes de costos en PDF con análisis detallado

## 📧 Funcionalidad de Email (NUEVO)

El sistema incluye funcionalidad de envío automático de formularios PDF por correo electrónico:

- **Botón "Email"** en la gestión de costos
- Envío automático al email del conductor asignado
- PDF adjunto con formulario editable
- Email formal con instrucciones para dispositivos móviles
- Recomendaciones de aplicaciones PDF (Adobe Reader, Xodo, Foxit)

### Configuración de Email

Ver archivo `CONFIGURACION_EMAIL.md` para instrucciones detalladas de configuración con Gmail.

## 🚀 Instalación Rápida

### Requisitos
- Python 3.12+
- MySQL 8.0+
- Git (opcional)

### Pasos de Instalación

```bash
# 1. Clonar o copiar el proyecto
cd proyecto_flota

# 2. Crear entorno virtual
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Edita .env con tus credenciales

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Recolectar archivos estáticos
python manage.py collectstatic

# 8. Verificar instalación
python verificar_instalacion.py

# 9. Iniciar servidor
python manage.py runserver
```

Ver `INSTALACION.md` para instrucciones detalladas.

## 📦 Dependencias Principales

```
Django >= 5.0
mysqlclient == 2.2.7
Pillow >= 10.0.0
reportlab >= 4.0.0
PyPDF2 >= 3.0.0
python-decouple == 3.8
requests >= 2.31.0
whitenoise == 6.4.0
```

## 🗂️ Estructura del Proyecto

```
proyecto_flota/
├── core/                    # Conductores y autenticación
├── flota/                   # Gestión de buses
├── viajes/                  # Gestión de viajes
├── costos/                  # Gestión de costos
│   ├── views.py            # Incluye envío de email
│   ├── informe_costos.py   # Generación de informes PDF
│   └── urls.py
├── templates/              # Plantillas HTML
├── static/                 # CSS, JavaScript
├── media/                  # Archivos subidos
├── docs/                   # Documentación
├── scripts/                # Scripts auxiliares
│   └── test_email.py      # Prueba de email
├── .env                    # Configuración (NO subir a Git)
├── .env.example           # Plantilla de configuración
├── requirements.txt       # Dependencias
├── manage.py              # Comando principal Django
├── INSTALACION.md         # Guía de instalación completa
├── CONFIGURACION_EMAIL.md # Guía de configuración de email
└── verificar_instalacion.py # Script de verificación
```

## 🔧 Configuración

### Base de Datos (MySQL)

```sql
CREATE DATABASE flota_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'flota_user'@'localhost' IDENTIFIED BY 'contraseña_segura';
GRANT ALL PRIVILEGES ON flota_db.* TO 'flota_user'@'localhost';
FLUSH PRIVILEGES;
```

### Variables de Entorno (.env)

```env
# Email (Gmail)
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion

# Base de Datos (opcional)
DB_NAME=flota_db
DB_USER=flota_user
DB_PASSWORD=contraseña_segura
DB_HOST=localhost
DB_PORT=3306
```

## 📱 Uso del Sistema

### Admin

Accede al panel de administración en: `http://127.0.0.1:8000/admin/`

### Módulos Principales

- **Inicio**: `/` - Dashboard principal
- **Conductores**: `/core/conductores/` - Gestión de conductores
- **Buses**: `/flota/buses/` - Gestión de buses
- **Viajes**: `/viajes/` - Gestión de viajes
- **Costos**: `/costos/` - Gestión de costos

### Flujo de Trabajo Típico

1. **Registrar Conductor** con email válido
2. **Registrar Bus** con capacidad y características
3. **Crear Viaje** asignando conductor y bus
4. **Registrar Costos** del viaje:
   - Opción A: Registro directo en el sistema
   - Opción B: Enviar formulario PDF por email al conductor
5. **Generar Informes** de costos con análisis detallado

## 🧪 Verificación

### Script de Verificación Automática

```bash
python verificar_instalacion.py
```

Este script verifica:
- ✓ Versión de Python
- ✓ Módulos instalados
- ✓ Configuración de .env
- ✓ Conexión a base de datos
- ✓ Migraciones aplicadas
- ✓ Modelos funcionando
- ✓ Archivos estáticos y media

### Prueba de Email

```bash
python scripts/test_email.py
```

### Verificación Manual

```bash
# Verificar sistema
python manage.py check

# Ejecutar tests
python manage.py test

# Shell interactivo
python manage.py shell
```

## 📚 Documentación

- `INSTALACION.md` - Guía completa de instalación
- `CONFIGURACION_EMAIL.md` - Configuración de email con Gmail
- `SOLUCION_ERROR_EMAIL.md` - Solución de problemas de email
- `docs/` - Documentación técnica adicional

## 🔒 Seguridad

### Archivos Sensibles (NO subir a Git)

- `.env` - Credenciales y configuración
- `db.sqlite3` - Base de datos de desarrollo
- `media/` - Documentos de conductores
- `__pycache__/` - Archivos temporales

Estos archivos están incluidos en `.gitignore`

### Recomendaciones

- ✅ Usa contraseñas de aplicación para Gmail (no contraseña real)
- ✅ Mantén `.env` fuera del control de versiones
- ✅ Cambia `SECRET_KEY` en producción
- ✅ Establece `DEBUG = False` en producción
- ✅ Usa HTTPS en producción
- ✅ Realiza backups periódicos de la base de datos

## 🐛 Solución de Problemas

### Error: "No module named 'X'"
```bash
pip install -r requirements.txt
```

### Error: "Authentication failed" (Email)
- Verifica credenciales en `.env`
- Activa verificación en 2 pasos en Gmail
- Genera contraseña de aplicación nueva
- Reinicia el servidor Django

### Error: "Access denied" (MySQL)
- Verifica usuario y contraseña
- Confirma que la base de datos existe
- Revisa permisos del usuario

Ver `SOLUCION_ERROR_EMAIL.md` para más detalles.

## 📊 Características Técnicas

### Backend
- Django 5.0+
- Python 3.12+
- MySQL 8.0+

### Frontend
- Bootstrap 5.1.3
- Font Awesome 6.0
- JavaScript vanilla

### Generación de PDF
- ReportLab 4.0+ (informes)
- PyPDF2 3.0+ (manipulación)
- Formularios PDF interactivos con campos editables

### Email
- SMTP de Gmail
- Soporte para archivos adjuntos
- Templates personalizables

## 🤝 Contribución

Este es un proyecto educativo. Para mejoras:

1. Crea un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 📞 Soporte

Para preguntas o problemas:
- Revisa la documentación en `docs/`
- Ejecuta `python verificar_instalacion.py`
- Consulta los archivos de configuración en la raíz

## 🎯 Roadmap

- [ ] Dashboard con gráficos y estadísticas
- [ ] Notificaciones push
- [ ] Integración con GPS para tracking en tiempo real
- [ ] App móvil nativa
- [ ] API REST para integraciones
- [ ] Reportes exportables (Excel, CSV)

## 👏 Créditos

Desarrollado para FlotaGest
Fecha: Diciembre 2025
Python + Django + MySQL + ReportLab

---

**¿Necesitas ayuda?** Consulta `INSTALACION.md` para instrucciones paso a paso.
