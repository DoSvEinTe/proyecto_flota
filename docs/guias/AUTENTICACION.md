# 🔐 Sistema de Autenticación y Control de Acceso

## 📋 Resumen General

Se ha implementado un sistema de autenticación basado en roles de Django con dos tipos de usuarios:

### **ADMINISTRADOR (ADMIN)**
- ✅ Acceso completo a todas las funcionalidades
- ✅ CRUD completo de Buses
- ✅ CRUD completo de Conductores  
- ✅ CRUD completo de Viajes, Lugares y Pasajeros
- ✅ Acceso al panel de administración Django

**Credenciales de prueba:**
- Usuario: `admin`
- Contraseña: `admin123`

### **USUARIO REGULAR**
- ✅ Acceso al Dashboard/Inicio
- ✅ VER Viajes (lectura)
- ✅ CREAR Viajes (solo creación)
- ✅ VER Lugares (lectura)
- ✅ CREAR Lugares (solo creación)
- ✅ VER Pasajeros (lectura)
- ✅ CREAR Pasajeros (solo creación)
- ❌ NO puede editar/eliminar nada
- ❌ NO puede ver Buses ni Conductores

**Credenciales de prueba:**
- Usuario: `usuario`
- Contraseña: `usuario123`

---

## 🔧 Cómo Funciona

### Flujo de Autenticación
1. Usuario accede a la aplicación
2. Si NO está logueado → Redirige a `/core/login/`
3. Usuario ingresa credenciales
4. Django valida usuario y contraseña
5. Si es válido → Crea sesión y redirige a `/home/`
6. Si es inválido → Muestra error y permite reintentar

### Flujo de Control de Acceso
1. Usuario intenta acceder a una sección protegida
2. Decorador (`@admin_required` o `@usuario_or_admin_required`) intercepta
3. Verifica si usuario está logueado
4. Verifica si usuario tiene grupo/permisos
5. Si ✅ → Permite acceso
6. Si ❌ → Redirige a home y muestra mensaje

### Menú Dinámico
El menú se muestra/oculta basado en el rol del usuario:
- **Admin**: Ve "Inicio", "Buses", "Conductores", "Viajes", "Lugares", "Pasajeros"
- **Usuario**: Ve "Inicio", "Viajes", "Lugares", "Pasajeros" (NO ve "Buses" ni "Conductores")

---

## 📁 Archivos de Implementación

### Creados:
- `core/auth_views.py` - Vistas de autenticación (login, logout)
- `core/permissions.py` - Decoradores y funciones de permisos
- `templates/auth/login.html` - Template personalizado de login
- `setup_auth.py` - Script para crear usuarios y grupos
- `verificar_auth.py` - Script para verificar setup

### Modificados:
- `sistema_flota/settings.py` - URLs de auth
- `core/urls.py` - Rutas de login/logout
- `core/views.py` - Decoradores en vistas
- `flota/views.py` - Decoradores en vistas
- `viajes/views.py` - Decoradores en vistas
- `templates/base.html` - Menú dinámico
- `templates/home.html` - Dashboard dinámico

---

## 🎯 Protección de Vistas

### Decoradores Disponibles

#### `@admin_required`
Solo permite acceso a administradores
```python
@method_decorator(admin_required)
class BusListView(ListView):
    pass
```

#### `@usuario_or_admin_required`
Permite acceso a usuarios y administradores
```python
@method_decorator(usuario_or_admin_required)
class ViajeListView(ListView):
    pass
```

#### `@login_required`
Permite acceso a cualquier usuario logueado
```python
@require_login
def home_view(request):
    pass
```

---

## 🔐 Tabla de Protecciones

### Módulo: Conductores
| Vista | Protección | Admin | Usuario |
|-------|-----------|-------|---------|
| List | `@admin_required` | ✅ Ver | ❌ |
| Create | `@admin_required` | ✅ Crear | ❌ |
| Update | `@admin_required` | ✅ Editar | ❌ |
| Delete | `@admin_required` | ✅ Eliminar | ❌ |

### Módulo: Buses
| Vista | Protección | Admin | Usuario |
|-------|-----------|-------|---------|
| List | `@admin_required` | ✅ Ver | ❌ |
| Create | `@admin_required` | ✅ Crear | ❌ |
| Update | `@admin_required` | ✅ Editar | ❌ |
| Delete | `@admin_required` | ✅ Eliminar | ❌ |

### Módulo: Viajes
| Vista | Protección | Admin | Usuario |
|-------|-----------|-------|---------|
| List | `@usuario_or_admin_required` | ✅ Ver | ✅ Ver |
| Create | `@usuario_or_admin_required` | ✅ Crear | ✅ Crear |
| Detail | `@usuario_or_admin_required` | ✅ Ver | ✅ Ver |
| Update | `@admin_required` | ✅ Editar | ❌ |
| Delete | `@admin_required` | ✅ Eliminar | ❌ |

### Módulo: Lugares
| Vista | Protección | Admin | Usuario |
|-------|-----------|-------|---------|
| List | `@usuario_or_admin_required` | ✅ Ver | ✅ Ver |
| Create | `@usuario_or_admin_required` | ✅ Crear | ✅ Crear |
| Detail | `@usuario_or_admin_required` | ✅ Ver | ✅ Ver |
| Update | `@admin_required` | ✅ Editar | ❌ |
| Delete | `@admin_required` | ✅ Eliminar | ❌ |

### Módulo: Pasajeros
| Vista | Protección | Admin | Usuario |
|-------|-----------|-------|---------|
| List | `@usuario_or_admin_required` | ✅ Ver | ✅ Ver |
| Create | `@usuario_or_admin_required` | ✅ Crear | ✅ Crear |
| Update | `@admin_required` | ✅ Editar | ❌ |
| Delete | `@admin_required` | ✅ Eliminar | ❌ |

---

## 🖥️ Interfaz de Usuario

### Navbar Superior
- Nombre del usuario logueado
- Rol visible (ADMIN en rojo, USUARIO en azul)
- Botón Salir (logout)

### Sidebar Dinámico
```
Usuarios Admin ven:
├─ Inicio
├─ Buses         ← Solo Admin
├─ Conductores   ← Solo Admin
├─ Viajes
├─ Lugares
└─ Pasajeros

Usuarios Regulares ven:
├─ Inicio
├─ Viajes
├─ Lugares
└─ Pasajeros
```

### Botones de Acción
- Los botones "Editar" y "Eliminar" se muestran/ocultan según rol
- En listas: Los botones aparecen solo para admin
- En detalles: Los botones aparecen solo para admin

---

## 🛠️ Configuración en Settings.py

```python
# Autenticación
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Idioma y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Santiago'
```

---

## 🚀 Cómo Usar

### Iniciar Sistema
```bash
# 1. Ejecutar migraciones
python manage.py migrate

# 2. Crear usuarios
python setup_auth.py

# 3. Verificar
python verificar_auth.py

# 4. Iniciar servidor
python manage.py runserver
```

### Crear Nuevo Usuario
```bash
# Opción 1: Django shell
python manage.py shell
>>> from django.contrib.auth.models import User, Group
>>> user = User.objects.create_user('nuevo', 'nuevo@test.com', 'password123')
>>> user.groups.add(Group.objects.get(name='Usuario'))
>>> user.save()

# Opción 2: Django admin
http://localhost:8000/admin/
```

### Cambiar Rol de Usuario
```python
from django.contrib.auth.models import User, Group
user = User.objects.get(username='usuario')
# Cambiar a admin
user.groups.clear()
user.groups.add(Group.objects.get(name='Admin'))
user.save()
```

---

## 📝 Funciones de Permisos

### `get_user_role(user)`
Retorna el rol del usuario:
```python
from core.permissions import get_user_role
role = get_user_role(request.user)
# Retorna: 'admin', 'usuario', o None
```

### `can_view_section(user, section)`
Verifica si usuario puede ver una sección:
```python
from core.permissions import can_view_section
if can_view_section(request.user, 'buses'):
    # Mostrar sección de buses
```

---

## ✅ Seguridad Implementada

✅ Protección CSRF en todos los formularios  
✅ Decoradores de login en todas las vistas  
✅ Control granular de acceso por rol  
✅ Validación de contraseñas  
✅ Sesiones de usuario seguras  
✅ Redirección automática a login  
✅ Mensajes de error claros  
✅ Botones dinámicos según permisos  

---

## 🐛 Troubleshooting

### Usuario no puede loguarse
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='usuario')
>>> user.set_password('new_password')
>>> user.save()
```

### Menú no se muestra dinámicamente
- Verifica que `{% if user.is_authenticated %}` está en base.html
- Asegúrate que el usuario tiene un grupo asignado
- Limpia caché del navegador (Ctrl+F5)

### Decoradores no funcionan
- Importa desde `core.permissions`
- Usa `@method_decorator()` en class-based views
- Usa directamente en function-based views

---

## 📚 Documentación Relacionada

Ver:
- `docs/INDICE_MAESTRO.md` - Índice maestro
- `docs/referencias/URLS_ENRUTAMIENTO.md` - Todas las rutas
- `docs/guias/GUIA_ESTRUCTURA.md` - Arquitectura general

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0  
**Estado**: ✅ Completo y Funcional
