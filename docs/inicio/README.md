# Sistema de Gestión de Flota de Buses

## Descripción
Sistema web desarrollado en Django para la gestión integral de una flota de buses, incluyendo la administración de buses, conductores, lugares y viajes.

## Características Implementadas

### ✅ CRUD de Buses
- **Listar buses**: Visualización de todos los buses con información clave
- **Agregar bus**: Formulario completo para registrar nuevos buses
- **Ver detalles**: Vista detallada con información completa del bus
- **Editar bus**: Modificación de datos existentes
- **Eliminar bus**: Confirmación de eliminación con advertencias

### ✅ CRUD de Conductores
- **Listar conductores**: Vista de todos los conductores registrados
- **Agregar conductor**: Formulario para nuevos conductores
- **Ver detalles**: Información completa del conductor con estadísticas
- **Editar conductor**: Actualización de datos del conductor
- **Eliminar conductor**: Eliminación con confirmación

### ✅ CRUD de Lugares
- **Listar lugares**: Visualización de lugares con coordenadas
- **Agregar lugar**: Formulario con soporte para coordenadas GPS
- **Ver detalles**: Vista con información geográfica
- **Editar lugar**: Modificación de información del lugar
- **Eliminar lugar**: Eliminación con advertencias

### ✅ CRUD de Viajes
- **Listar viajes**: Visualización de todos los viajes programados y completados
- **Agregar viaje**: Formulario completo para registrar nuevos viajes
- **Ver detalles**: Información completa del viaje con coordenadas de origen y destino
- **Editar viaje**: Actualización de información del viaje
- **Eliminar viaje**: Eliminación con confirmación
- **Captura automática de coordenadas**: Las coordenadas se guardan automáticamente desde los lugares de origen y destino

### ✅ Interfaz de Usuario
- **Diseño responsivo**: Compatible con dispositivos móviles y desktop
- **Bootstrap 5**: Interfaz moderna y profesional
- **Font Awesome**: Iconografía completa
- **Navegación intuitiva**: Sidebar con navegación clara
- **Mensajes de feedback**: Confirmaciones y errores claros
- **Autenticación**: Sistema de login con roles (Admin, Usuario)

## Tecnologías Utilizadas
- **Backend**: Django 5.2.8
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Base de datos**: MySQL
- **Iconos**: Font Awesome 6
- **Estilos**: Bootstrap + CSS personalizado
- **Tipografía**: Google Fonts (Poppins)

## Características de Seguridad

### ✅ Autenticación
- Sistema de login con Django auth
- Sesiones seguras
- Logout con confirmación

### ✅ Control de Acceso
- Dos roles: Admin y Usuario Regular
- Decoradores de protección de vistas
- Menú dinámico según rol
- Botones de acción ocultos para usuarios sin permisos

### ✅ Protección
- CSRF protection
- Validación de formularios
- Confirmación para operaciones peligrosas
- Redirección automática a login

## Estructura del Proyecto

```
proyecto_buses/
├── core/                   # App principal (conductores, lugares)
│   ├── auth_views.py      # Vistas de autenticación ✅ NUEVO
│   ├── permissions.py     # Decoradores de permisos ✅ NUEVO
│   ├── models.py          # Modelos Conductor, Lugar, Pasajero
│   ├── views.py           # Vistas CRUD
│   ├── urls.py            # URLs de core
│   ├── admin.py           # Admin de Django
│   └── migrations/
├── flota/                 # App de gestión de buses
│   ├── models.py          # Modelos Bus, Documento, Mantenimiento
│   ├── views.py           # Vistas CRUD de buses
│   ├── urls.py            # URLs de flota
│   ├── admin.py           # Admin de Django
│   └── migrations/
├── viajes/                # App de gestión de viajes
│   ├── models.py          # Modelo Viaje
│   ├── views.py           # Vistas CRUD de viajes
│   ├── urls.py            # URLs de viajes
│   ├── admin.py           # Admin de Django
│   └── migrations/
├── costos/                # App de costos
│   ├── models.py          # Modelos de costos
│   ├── views.py           # Vistas
│   ├── urls.py            # URLs de costos
│   └── migrations/
├── templates/             # Plantillas HTML
│   ├── base.html          # Plantilla base
│   ├── home.html          # Página principal
│   ├── auth/              # Templates de autenticación ✅ NUEVO
│   │   └── login.html
│   ├── core/              # Templates de conductores y lugares
│   ├── flota/             # Templates de buses
│   └── viajes/            # Templates de viajes
├── docs/                  # 📚 DOCUMENTACIÓN ✅ NUEVO
│   ├── INDICE_MAESTRO.md
│   ├── inicio/
│   ├── guias/
│   ├── referencias/
│   └── reportes/
├── static/                # Archivos estáticos
│   └── css/
│       └── custom_styles.css
├── staticfiles/           # Se crea con collectstatic
├── sistema_flota/         # Configuración del proyecto
│   ├── settings.py        # Configuración principal
│   ├── urls.py            # URLs principales
│   └── wsgi.py
├── manage.py
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Este archivo
├── setup_auth.py          # Script de inicialización auth ✅ NUEVO
└── verificar_auth.py      # Script de verificación ✅ NUEVO
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- MySQL Server
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto_buses
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   - Crear base de datos MySQL llamada `db_flota`
   - Verificar credenciales en `sistema_flota/settings.py`

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Recolectar archivos estáticos**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Crear usuarios de prueba (opcional)**
   ```bash
   python setup_auth.py
   ```

8. **Iniciar servidor**
   ```bash
   python manage.py runserver
   ```

## Acceso al Sistema

### En Desarrollo
- **URL**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

### Usuarios de Prueba
Si ejecutaste `setup_auth.py`:
- **Admin**: usuario: `admin` | contraseña: `admin123`
- **Usuario**: usuario: `usuario` | contraseña: `usuario123`

## Uso del Sistema

### Página Principal (/)
- Dashboard con estadísticas
- Acceso rápido a todas las funciones
- Información del sistema
- Acciones según rol

### Gestión de Buses (/flota/buses/)
- **Requisitos**: Solo Admin
- CRUD completo de buses
- Información técnica y administrativa
- Estados: Activo, En Mantenimiento, Inactivo

### Gestión de Conductores (/core/conductores/)
- **Requisitos**: Solo Admin
- CRUD completo de conductores
- Información personal y laboral
- Validación de datos únicos

### Gestión de Viajes (/viajes/)
- **Requisitos**: Admin puede hacer todo, Usuario puede crear/leer
- Registro de viajes con origen y destino
- Captura automática de coordenadas
- Gestión de pasajeros en viajes
- Estados: Programado, En Curso, Completado, Cancelado

### Gestión de Lugares (/core/lugares/)
- **Requisitos**: Admin puede hacer todo, Usuario puede crear/leer
- Información geográfica
- Coordenadas GPS
- Información de ciudad y país

### Gestión de Pasajeros (/core/pasajeros/)
- **Requisitos**: Admin puede hacer todo, Usuario puede crear/leer
- Información de pasajeros
- Validación de datos únicos
- Asociación a viajes

## Características de la Interfaz

### Diseño Responsivo
- Adaptable a cualquier tamaño de pantalla
- Navegación optimizada para móviles
- Tablas con scroll horizontal en dispositivos pequeños

### Experiencia de Usuario
- Mensajes de confirmación y error claros
- Formularios con validación
- Confirmaciones antes de eliminar
- Menú dinámico según rol
- Mostrador de usuario logueado

### Navegación
- Sidebar lateral con navegación principal
- Top navbar dinámico con título actual
- Menú adaptado al rol del usuario
- Enlaces rápidos según permisos

## Próximas Implementaciones

### ✅ Completado
- [x] Gestión de buses
- [x] Gestión de conductores
- [x] Gestión de lugares
- [x] Gestión de viajes
- [x] Sistema de autenticación
- [x] Control de roles y permisos
- [x] Mejoras visuales profesionales
- [x] Documentación completa

### En desarrollo
- [ ] Reportes avanzados
- [ ] Exportación de datos
- [ ] Notificaciones automáticas
- [ ] APIs REST

## Documentación Disponible

La documentación completa está organizada en la carpeta `docs/`:

- **docs/INDICE_MAESTRO.md** - Índice maestro de toda la documentación
- **docs/inicio/** - Guías de inicio rápido
- **docs/guias/** - Guías de desarrollo
- **docs/referencias/** - Documentación de consulta
- **docs/reportes/** - Reportes y cambios

Para más información, consulta `docs/INDICE_MAESTRO.md`

## Soporte y Contacto

Para soporte técnico:
1. Consulta la documentación en `docs/`
2. Revisa el archivo de errores y soluciones
3. Ejecuta verificaciones con `python manage.py check`
4. Verifica usuarios con `python verificar_auth.py`

## Licencia

Este proyecto está desarrollado para uso interno de la organización.

---

**Versión**: 3.0.0  
**Última actualización**: Noviembre 2025  
**Estado**: ✅ Producción
