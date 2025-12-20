# 🔐 Documentación - Gestión de Contraseñas

## 📋 Descripción General

Se ha implementado un sistema completo de gestión de contraseñas que permite:

1. **Cambio de contraseña del usuario actual** - Con autenticación mediante contraseña maestra
2. **Cambio de contraseña por administrador** - Admin puede cambiar contraseña de cualquier usuario
3. **Gestión de usuarios** - Vista para listar todos los usuarios y acceder a sus opciones
4. **Configuración personal** - Panel de usuario con opciones de seguridad

---

## 🔒 Seguridad Implementada

### Contraseña Maestra
- Requerida para autorizar cambios de contraseña
- Configurada en `.env` como `MASTER_PASSWORD=admin123`
- **IMPORTANTE**: Cambiar en producción por una contraseña segura

### Validación de Contraseña
- Mínimo 8 caracteres
- Debe contener letras mayúsculas y minúsculas
- Debe contener números
- Debe contener caracteres especiales

### Control de Acceso
- Solo admin/superuser puede ver lista de usuarios
- Solo admin puede cambiar contraseña de otros
- Cada usuario puede cambiar solo su propia contraseña

### Auditoría
- Se registran cambios en consola (mejorable con logs persistentes)
- Formato: `[AUDITORIA] Usuario X cambió contraseña - TIMESTAMP`

---

## 🚀 Funcionalidades Creadas

### 1. Cambiar Mi Contraseña (Usuario)
**URL**: `/core/cambiar-contrasena/`  
**Template**: `core/change_password.html`

**Requiere**:
- Login activo
- Contraseña maestra correcta
- Nueva contraseña que cumpla requisitos

**Flujo**:
1. Usuario ingresa contraseña maestra
2. Usuario ingresa nueva contraseña
3. Confirma la nueva contraseña
4. Al confirmar, se desloguea automáticamente
5. Debe iniciar sesión con nueva contraseña

### 2. Cambiar Contraseña de Usuario (Admin)
**URL**: `/core/usuarios/<username>/cambiar-contrasena/`  
**Template**: `core/admin_change_password.html`

**Requiere**:
- Usuario debe ser staff/superuser
- No requiere contraseña maestra
- Muestra información del usuario a modificar

**Flujo**:
1. Admin accede desde lista de usuarios
2. Admin ingresa nueva contraseña
3. Confirma la contraseña
4. Sistema cambia la contraseña inmediatamente

### 3. Listar Usuarios (Admin)
**URL**: `/core/usuarios/listar/`  
**Template**: `core/users_list_admin.html`

**Características**:
- Tabla de todos los usuarios
- Información: usuario, email, nombre, tipo, estado
- Botones de acción:
  - 🔑 Cambiar contraseña
  - ✏️ Editar en admin Django

### 4. Configuración de Usuario
**URL**: `/core/configuracion/`  
**Template**: `core/settings.html`

**Secciones**:
- **Seguridad**: Opciones de contraseña y sesiones
- **Mi Perfil**: Información del usuario
- **Mi Cuenta**: Datos de registro y estado

---

## 📂 Archivos Creados

### Backend
- `core/password_forms.py` - Formularios para cambio de contraseña
- `core/password_views.py` - Vistas para gestión de contraseñas

### Frontend
- `templates/core/change_password.html` - Cambiar mi contraseña
- `templates/core/admin_change_password.html` - Admin cambia contraseña
- `templates/core/users_list_admin.html` - Listar usuarios
- `templates/core/settings.html` - Configuración de usuario

### Configuración
- `core/urls.py` - URLs actualizadas
- `sistema_flota/settings.py` - Configuración de MASTER_PASSWORD
- `.env` - Variable MASTER_PASSWORD
- `templates/base.html` - Menú dropdown en navbar

---

## ⚙️ Configuración

### 1. Variable de Entorno (.env)
```env
# Contraseña maestra para autorizar cambios de contraseña
MASTER_PASSWORD=admin123
```

### 2. URLs a Agregar (Ya incluidas en urls.py)
```python
path('cambiar-contrasena/', password_views.change_password_view, name='change_password'),
path('configuracion/', password_views.settings_view, name='settings'),
path('usuarios/listar/', password_views.list_users_admin_view, name='user_list_admin'),
path('usuarios/<str:username>/cambiar-contrasena/', password_views.change_user_password_admin_view, name='admin_change_user_password'),
```

### 3. Acceso desde Menú
- Nuevo menú dropdown en navbar (esquina superior derecha)
- Opciones: Configuración, Cambiar Contraseña, Gestionar Usuarios (si es admin)

---

## 🔄 Flujos de Uso

### Usuario Regular Cambia Su Contraseña

```
1. Usuario hace click en dropdown (esquina arriba a la derecha)
   ↓
2. Selecciona "Cambiar Contraseña"
   ↓
3. Ingresa contraseña maestra (ej: admin123)
   ↓
4. Ingresa nueva contraseña (ej: MiPass123!@#)
   ↓
5. Confirma la contraseña
   ↓
6. Sistema valida y cambia
   ↓
7. Usuario es deslogueado automáticamente
   ↓
8. Inicia sesión con nueva contraseña
```

### Admin Cambia Contraseña de Usuario

```
1. Admin hace click en dropdown
   ↓
2. Selecciona "Gestionar Usuarios"
   ↓
3. Ve tabla de usuarios
   ↓
4. Hace click en icono 🔑 (cambiar contraseña)
   ↓
5. Ingresa nueva contraseña
   ↓
6. Confirma la contraseña
   ↓
7. Sistema cambia inmediatamente
   ↓
8. Vuelve a lista de usuarios
   ↓
9. El usuario afectado debe usar nueva contraseña en próximo login
```

---

## 🛡️ Mejoras de Seguridad Recomendadas

### Inmediatas
1. Cambiar `MASTER_PASSWORD` en producción por algo seguro
2. Usar HTTPS en producción
3. Implementar rate limiting en cambio de contraseña

### Futuras
1. Auditoría persistente en base de datos
2. Historial de cambios de contraseña
3. Autenticación multifactor (2FA)
4. Recuperación de contraseña por email
5. Expiración de contraseña cada X días
6. Historial de sesiones activas

---

## 📋 Requisitos Cumplidos

✅ Cambio de contraseña de usuario con contraseña maestra  
✅ Cambio de contraseña de admin para otros usuarios  
✅ Validación de fuerza de contraseña  
✅ Gestión de usuarios desde admin  
✅ Panel de configuración personal  
✅ Menú integrado en navbar  
✅ Auditoría de cambios  
✅ Control de acceso por permisos  

---

## 🧪 Testing

### Prueba 1: Usuario Cambia Contraseña
1. Login como usuario regular
2. Click en dropdown → "Cambiar Contraseña"
3. Ingresa contraseña maestra: `admin123`
4. Nueva contraseña: `Test1234!@#`
5. Confirma
6. Verifica que se desloguea
7. Login con nueva contraseña debe funcionar

### Prueba 2: Admin Cambia Contraseña
1. Login como admin
2. Click en dropdown → "Gestionar Usuarios"
3. Busca usuario
4. Click en icono 🔑
5. Ingresa nueva contraseña: `NewPass456!@#`
6. Confirma
7. Verifica que el cambio se aplicó

### Prueba 3: Validación de Contraseña
1. Intenta cambiar a contraseña débil: `123`
2. Debe mostrar error
3. Intenta sin caracteres especiales: `Password123`
4. Debe mostrar error

---

## 📞 Soporte

¿Olvidó la contraseña maestra?
- Cambiar directamente en `.env`: `MASTER_PASSWORD=nueva_contraseña`
- Reiniciar aplicación

¿Usuario olvidó su contraseña?
- Admin va a "Gestionar Usuarios"
- Busca el usuario
- Hace click en 🔑
- Cambia a contraseña temporal
- Comunica contraseña al usuario

---

**Sistema de gestión de contraseñas completamente funcional ✅**
