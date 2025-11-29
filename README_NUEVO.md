# 📚 Sistema de Gestión de Flota de Buses

> **Documentación Reorganizada**: Consulta `docs/INDICE_MAESTRO.md` para acceder a toda la documentación

## ⚡ Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Migrar BD
python manage.py migrate

# 3. Crear usuarios
python setup_auth.py

# 4. Recolectar estáticos
python manage.py collectstatic --noinput

# 5. Ejecutar
python manage.py runserver
```

Accede a: **http://localhost:8000**

### Usuarios de Prueba
- **Admin**: `admin` / `admin123` (acceso total)
- **Usuario**: `usuario` / `usuario123` (lectura y creación)

---

## 📖 Documentación

**Toda la documentación está en `docs/`**

### 🗺️ Inicio rápido
- [docs/INDICE_MAESTRO.md](docs/INDICE_MAESTRO.md) - Índice y guía de navegación
- [docs/inicio/README.md](docs/inicio/README.md) - Descripción del proyecto
- [docs/inicio/INICIO_RAPIDO.md](docs/inicio/INICIO_RAPIDO.md) - Guía en 5 minutos

### 📖 Guías de desarrollo
- [docs/guias/GUIA_ESTRUCTURA.md](docs/guias/GUIA_ESTRUCTURA.md) - Arquitectura y navegación
- [docs/guias/AUTENTICACION.md](docs/guias/AUTENTICACION.md) - Sistema de auth y permisos
- [docs/guias/GUIA_ESTILOS.md](docs/guias/GUIA_ESTILOS.md) - Estilos y componentes
- [docs/guias/PLANTILLAS_EJEMPLO.md](docs/guias/PLANTILLAS_EJEMPLO.md) - 5 plantillas HTML
- [docs/guias/COMPONENTES_REUTILIZABLES.html](docs/guias/COMPONENTES_REUTILIZABLES.html) - Snippets de código

### 🎨 Referencias técnicas
- [docs/referencias/PALETA_COLORES.md](docs/referencias/PALETA_COLORES.md) - 7 colores profesionales
- [docs/referencias/TIPOGRAFIA.md](docs/referencias/TIPOGRAFIA.md) - Fuentes y tamaños
- [docs/referencias/URLS_ENRUTAMIENTO.md](docs/referencias/URLS_ENRUTAMIENTO.md) - Todas las rutas

### 📊 Reportes
- [docs/reportes/CAMBIOS_IMPLEMENTADOS.md](docs/reportes/CAMBIOS_IMPLEMENTADOS.md) - Detalle de cambios
- [docs/reportes/RESUMEN_FINAL.md](docs/reportes/RESUMEN_FINAL.md) - Resumen ejecutivo
- [docs/reportes/ANTES_Y_DESPUES.md](docs/reportes/ANTES_Y_DESPUES.md) - Comparativa visual

---

## ✨ Características

### 🔐 Autenticación y Control de Acceso
- Sistema de login con Django auth
- Dos roles: **Admin** (acceso total) y **Usuario** (lectura + creación)
- Decoradores de protección de vistas
- Menú dinámico según rol
- Botones de acción controlados por permisos

### 🎨 Interfaz Moderna
- Paleta de 7 colores profesionales
- Tipografía moderna (Google Fonts Poppins)
- Sidebar lateral con navegación
- Dashboard dinámico
- Componentes reutilizables
- 100% Responsive

### 📱 Aplicaciones
- **Buses**: Gestión de flota (admin)
- **Conductores**: Gestión de conductores (admin)
- **Viajes**: Registro y seguimiento de viajes
- **Lugares**: Gestión de ubicaciones con GPS
- **Pasajeros**: Gestión de pasajeros
- **Costos**: Control de costos (en desarrollo)

---

## 🗂️ Estructura del Proyecto

```
proyecto_buses/
├── docs/                          📚 DOCUMENTACIÓN (NUEVA)
│   ├── INDICE_MAESTRO.md
│   ├── inicio/
│   ├── guias/
│   ├── referencias/
│   └── reportes/
├── core/                          Aplicación principal
│   ├── auth_views.py ✅ NUEVO
│   ├── permissions.py ✅ NUEVO
│   ├── views.py
│   ├── urls.py
│   └── ...
├── flota/                         Gestión de buses
├── viajes/                        Gestión de viajes
├── templates/                     Plantillas HTML
│   ├── auth/login.html ✅ NUEVO
│   ├── base.html ✅ ACTUALIZADO
│   └── ...
├── static/css/custom_styles.css ✅ MEJORADO
├── manage.py
├── requirements.txt
├── setup_auth.py ✅ NUEVO
├── verificar_auth.py ✅ NUEVO
└── README.md ← TÚ ESTÁS AQUÍ
```

---

## 🚀 Comandos Útiles

```bash
# Verificar configuración
python manage.py check

# Ver usuarios
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Crear nuevo superusuario
python manage.py createsuperuser

# Recolectar estáticos
python manage.py collectstatic --noinput

# Ver todas las rutas
python manage.py show_urls
```

---

## ✅ Estado del Proyecto

```
✅ Eliminación de funcionalidades obsoletas
✅ Autenticación con roles implementada
✅ Control de acceso granular
✅ Interfaz moderna y profesional
✅ Documentación completa y organizada
✅ Responsive en todos los dispositivos
✅ Listo para producción
```

---

## 📞 Soporte

Para dudas o problemas:

1. Consulta [docs/INDICE_MAESTRO.md](docs/INDICE_MAESTRO.md)
2. Busca en la sección de guías correspondiente
3. Revisa los ejemplos en `docs/guias/PLANTILLAS_EJEMPLO.md`

---

## 🎓 Próximos Pasos

1. Lee [docs/INDICE_MAESTRO.md](docs/INDICE_MAESTRO.md) - Navega toda la documentación
2. Sigue [docs/inicio/INICIO_RAPIDO.md](docs/inicio/INICIO_RAPIDO.md) - Configura en 5 minutos
3. Consulta [docs/guias/AUTENTICACION.md](docs/guias/AUTENTICACION.md) - Entiende la autenticación
4. Personaliza con [docs/guias/GUIA_ESTILOS.md](docs/guias/GUIA_ESTILOS.md) - Modifica colores y estilos

---

## 📊 Información del Proyecto

| Aspecto | Detalle |
|---------|---------|
| **Versión** | 3.0.0 |
| **Framework** | Django 5.2.8 |
| **BD** | MySQL |
| **Frontend** | Bootstrap 5 + CSS personalizado |
| **Estado** | ✅ Producción |
| **Documentación** | 18+ archivos |
| **Usuarios de Prueba** | 2 (admin, usuario) |

---

**Última actualización**: Noviembre 2025  
**Mantenedor**: Sistema de Gestión de Flota
