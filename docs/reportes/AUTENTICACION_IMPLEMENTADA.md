# Implementación de Autenticación y Control de Acceso - Sistema de Flota

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

## 🔧 Cambios Implementados

### 1. **Configuración Django (settings.py)**
```python
# Idioma y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Santiago'

# URLs de autenticación
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```

### 2. **Decoradores Personalizados (core/permissions.py)**
Se crearon decoradores para proteger vistas:

- `@admin_required` - Solo Administradores
- `@usuario_or_admin_required` - Usuarios y Administradores
- `get_user_role(user)` - Obtiene el rol del usuario
- `can_view_section(user, section)` - Verifica permisos de sección

### 3. **Vistas de Autenticación (core/auth_views.py)**
- `login_view()` - Página de login con formulario personalizado
- `logout_view()` - Cerrar sesión
- `LoginForm` - Formulario de login personalizado

### 4. **Protección de Vistas**

#### Core (Conductores, Lugares, Pasajeros):
| Vista | Protección | Detalles |
|-------|-----------|----------|
| ConductorListView | `@admin_required` | Solo admin |
| LugarListView | `@usuario_or_admin_required` | Lee ambos |
| LugarCreateView | `@usuario_or_admin_required` | Ambos pueden crear |
| LugarUpdateView | `@admin_required` | Solo admin edita |
| LugarDeleteView | `@admin_required` | Solo admin elimina |
| PasajeroListView | `@usuario_or_admin_required` | Lee ambos |
| PasajeroCreateView | `@usuario_or_admin_required` | Ambos crean |
| home_view | `@login_required` | Todos logueados |

#### Flota (Buses):
| Vista | Protección |
|-------|-----------|
| BusListView | `@admin_required` |
| BusCreateView | `@admin_required` |
| BusUpdateView | `@admin_required` |
| BusDeleteView | `@admin_required` |
| MantenimientoCreateView | `@admin_required` |
| DocumentoVehiculoCreateView | `@admin_required` |

#### Viajes:
| Vista | Protección |
|-------|-----------|
| ViajeListView | `@usuario_or_admin_required` |
| ViajeDetailView | `@usuario_or_admin_required` |
| ViajeCreateView | `@usuario_or_admin_required` |
| ViajeUpdateView | `@admin_required` |
| ViajeDeleteView | `@admin_required` |
| agregar_pasajero_viaje | `@login_required` |

### 5. **Template de Login (templates/auth/login.html)**
- Diseño moderno con gradiente azul/morado
- Campos personalizados (usuario, contraseña)
- Información de credenciales de prueba
- Mensajes de error personalizados
- Responsive para móviles

### 6. **Actualización de Base.html**
- Mostrador de usuario logueado en navbar superior
- Rol visible (ADMIN/USUARIO)
- Botón de Logout con confirmación
- Menú dinámico que se muestra según rol:
  - Admin: Ve "Buses" y "Conductores"
  - Usuario: NO ve "Buses" ni "Conductores"
  - Ambos: Ven "Viajes", "Lugares", "Pasajeros"

### 7. **Grupos de Usuarios**
Se crearon dos grupos automáticamente:
- **Grupo "Admin"** - Para administradores
- **Grupo "Usuario"** - Para usuarios regulares

### 8. **URLs Configuradas (core/urls.py)**
```python
path('login/', auth_views.login_view, name='login'),
path('logout/', auth_views.logout_view, name='logout'),
```

---

## 🚀 Cómo Funciona

### Flujo de Autenticación:
1. Usuario accede a la aplicación
2. Si NO está logueado → Redirige a `/core/login/`
3. Usuario ingresa credenciales
4. Django valida usuario y contraseña
5. Si es válido → Crea sesión y redirige a `/home/`
6. Si es inválido → Muestra error y permite reintentar

### Flujo de Control de Acceso:
1. Usuario intenta acceder a una sección protegida
2. Decorador `@admin_required` o `@usuario_or_admin_required` intercepta
3. Verifica si usuario está logueado
4. Verifica si usuario tiene grupo/permisos
5. Si ✅ → Permite acceso
6. Si ❌ → Redirige a home y muestra mensaje de error

### Menú Dinámico:
```django
{% if user.is_authenticated %}
    {% if user.is_superuser or user.groups.all.0.name == 'Admin' %}
        <!-- Mostrar menú ADMIN -->
        - Buses
        - Conductores
    {% endif %}
    <!-- Mostrar menú para todos -->
    - Viajes
    - Lugares
    - Pasajeros
{% endif %}
```

---

## 📝 Archivos Modificados/Creados

### Creados:
- `core/auth_views.py` - Vistas de autenticación
- `core/permissions.py` - Decoradores y funciones de permisos (ACTUALIZADO)
- `templates/auth/login.html` - Template de login
- `setup_auth.py` - Script para crear usuarios y grupos

### Modificados:
- `sistema_flota/settings.py` - Configuración de autenticación
- `core/urls.py` - Rutas de login/logout
- `core/views.py` - Decoradores en vistas
- `flota/views.py` - Decoradores en vistas
- `viajes/views.py` - Decoradores en vistas
- `templates/base.html` - Menú dinámico y usuario en navbar

---

## 🔐 Seguridad Implementada

✅ Protección CSRF en todos los formularios
✅ Decoradores de login en todas las vistas
✅ Control granular de acceso por rol
✅ Validación de contraseñas
✅ Sesiones de usuario
✅ Redirección automática a login
✅ Mensajes de error claros
✅ Botón de logout seguro

---

## 📱 Interfaz de Usuario

### Navbar Superior:
- Nombre del usuario logueado
- Rol visible (ADMIN en rojo, USUARIO en azul)
- Botón Salir (logout)

### Sidebar:
- Menú dinámico según rol
- Enlaces activos resaltados
- Secciones agrupadas:
  - Principal (Inicio)
  - Operaciones (Solo Admin: Buses, Conductores)
  - Gestión (Todos: Viajes, Lugares, Pasajeros)

### Login:
- Formulario elegante con Bootstrap 5
- Información de credenciales de prueba
- Mensajes de error informativos
- Diseño responsive

---

## ✅ Checklist de Funcionalidades

### Autenticación:
- ✅ Login funcional
- ✅ Logout funcional
- ✅ Redirección automática a login
- ✅ Validación de credenciales

### Roles y Permisos:
- ✅ Grupo ADMIN con acceso completo
- ✅ Grupo USUARIO con acceso limitado
- ✅ Menú dinámico según rol
- ✅ Decoradores de protección

### Interfaz:
- ✅ Mostrador de usuario en navbar
- ✅ Rol visible
- ✅ Botón logout
- ✅ Menú dinámico
- ✅ Login responsive

### Base de Datos:
- ✅ Usuarios creados
- ✅ Grupos creados
- ✅ Asociaciones de grupos

---

## 🔄 Próximas Mejoras (Opcionales)

- [ ] Recuperación de contraseña por email
- [ ] Registro de nuevos usuarios (con aprobación admin)
- [ ] Autenticación de dos factores (2FA)
- [ ] Logs de auditoría de acceso
- [ ] Cambio de contraseña de usuario
- [ ] Perfil de usuario editable
- [ ] Permisos más granulares por modelo

---

## 📞 Soporte

Para cambiar contraseñas o crear nuevos usuarios:
```bash
python manage.py shell
from django.contrib.auth.models import User, Group
# Crear usuario
user = User.objects.create_user('username', 'email@test.com', 'password')
# Agregar a grupo
user.groups.add(Group.objects.get(name='Admin'))
```

O ejecutar el script:
```bash
python setup_auth.py
```

---

**Implementado en:** 27 de Noviembre de 2025
**Versión:** 1.0
**Estado:** ✅ Completo y Funcional
