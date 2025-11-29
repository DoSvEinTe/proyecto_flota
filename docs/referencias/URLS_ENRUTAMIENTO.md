# 🌐 URLs y Enrutamiento - Sistema de Gestión de Flota

## 📊 Tabla de Rutas Completa

### URLs Principales

| Ruta | Nombre | Protección | Vista | Descripción |
|------|--------|-----------|-------|-------------|
| `/` | `home` | `@login_required` | `home_view` | Dashboard principal |
| `/core/login/` | `login` | `None` | `login_view` | Página de login |
| `/core/logout/` | `logout` | `@login_required` | `logout_view` | Cerrar sesión |
| `/admin/` | `admin:index` | `@staff_required` | Django Admin | Panel administrativo |

---

## 🚌 Módulo: Flota (Buses)

**Prefijo**: `/flota/`  
**Protección General**: `@admin_required`  
**Rol Requerido**: Solo Admin

| Ruta | Nombre | Método HTTP | Vista | Descripción |
|------|--------|------------|-------|-------------|
| `buses/` | `flota:bus_list` | GET | `BusListView` | Listar buses |
| `buses/crear/` | `flota:bus_create` | GET, POST | `BusCreateView` | Crear bus |
| `buses/<int:pk>/` | `flota:bus_detail` | GET | `BusDetailView` | Ver detalles |
| `buses/<int:pk>/editar/` | `flota:bus_update` | GET, POST | `BusUpdateView` | Editar bus |
| `buses/<int:pk>/eliminar/` | `flota:bus_delete` | GET, POST | `BusDeleteView` | Eliminar bus |
| `mantenimientos/` | `flota:mantenimiento_list` | GET | `MantenimientoListView` | Listar mantenimientos |
| `mantenimientos/crear/` | `flota:mantenimiento_create` | GET, POST | `MantenimientoCreateView` | Crear mantenimiento |
| `mantenimientos/<int:pk>/` | `flota:mantenimiento_detail` | GET | `MantenimientoDetailView` | Ver detalles |
| `mantenimientos/<int:pk>/editar/` | `flota:mantenimiento_update` | GET, POST | `MantenimientoUpdateView` | Editar |
| `mantenimientos/<int:pk>/eliminar/` | `flota:mantenimiento_delete` | GET, POST | `MantenimientoDeleteView` | Eliminar |
| `documentos/` | `flota:documento_list` | GET | `DocumentoVehiculoListView` | Listar documentos |
| `documentos/crear/` | `flota:documento_create` | GET, POST | `DocumentoVehiculoCreateView` | Crear documento |
| `documentos/<int:pk>/editar/` | `flota:documento_update` | GET, POST | `DocumentoVehiculoUpdateView` | Editar documento |
| `documentos/<int:pk>/eliminar/` | `flota:documento_delete` | GET, POST | `DocumentoVehiculoDeleteView` | Eliminar documento |

---

## 👨‍✈️ Módulo: Core (Conductores, Lugares, Pasajeros)

### Conductores

**Prefijo**: `/core/`  
**Protección General**: `@admin_required`  
**Rol Requerido**: Solo Admin

| Ruta | Nombre | Método HTTP | Vista | Descripción |
|------|--------|------------|-------|-------------|
| `conductores/` | `conductor_list` | GET | `ConductorListView` | Listar |
| `conductores/crear/` | `conductor_create` | GET, POST | `ConductorCreateView` | Crear |
| `conductores/<int:pk>/` | `conductor_detail` | GET | `ConductorDetailView` | Ver detalles |
| `conductores/<int:pk>/editar/` | `conductor_update` | GET, POST | `ConductorUpdateView` | Editar |
| `conductores/<int:pk>/eliminar/` | `conductor_delete` | GET, POST | `ConductorDeleteView` | Eliminar |

### Lugares

**Prefijo**: `/core/`  
**Protección General**: `@usuario_or_admin_required`  
**Rol Requerido**: Admin o Usuario

| Ruta | Nombre | Método HTTP | Vista | Protección Específica |
|------|--------|------------|-------|----------------------|
| `lugares/` | `lugar_list` | GET | `LugarListView` | `@usuario_or_admin_required` |
| `lugares/crear/` | `lugar_create` | GET, POST | `LugarCreateView` | `@usuario_or_admin_required` |
| `lugares/<int:pk>/` | `lugar_detail` | GET | `LugarDetailView` | `@usuario_or_admin_required` |
| `lugares/<int:pk>/editar/` | `lugar_update` | GET, POST | `LugarUpdateView` | `@admin_required` |
| `lugares/<int:pk>/eliminar/` | `lugar_delete` | GET, POST | `LugarDeleteView` | `@admin_required` |

### Pasajeros

**Prefijo**: `/core/`  
**Protección General**: `@usuario_or_admin_required`  
**Rol Requerido**: Admin o Usuario

| Ruta | Nombre | Método HTTP | Vista | Protección Específica |
|------|--------|------------|-------|----------------------|
| `pasajeros/` | `pasajero_list` | GET | `PasajeroListView` | `@usuario_or_admin_required` |
| `pasajeros/crear/` | `pasajero_create` | GET, POST | `PasajeroCreateView` | `@usuario_or_admin_required` |
| `pasajeros/<int:pk>/` | `pasajero_detail` | GET | `PasajeroDetailView` | `@usuario_or_admin_required` |
| `pasajeros/<int:pk>/editar/` | `pasajero_update` | GET, POST | `PasajeroUpdateView` | `@admin_required` |
| `pasajeros/<int:pk>/eliminar/` | `pasajero_delete` | GET, POST | `PasajeroDeleteView` | `@admin_required` |

---

## 🛣️ Módulo: Viajes

**Prefijo**: `/viajes/`  
**Protección General**: `@usuario_or_admin_required` (con excepciones)

| Ruta | Nombre | Método HTTP | Vista | Protección Específica |
|------|--------|------------|-------|----------------------|
| `` | `viajes:viaje_list` | GET | `ViajeListView` | `@usuario_or_admin_required` |
| `crear/` | `viajes:viaje_create` | GET, POST | `ViajeCreateView` | `@usuario_or_admin_required` |
| `<int:pk>/` | `viajes:viaje_detail` | GET | `ViajeDetailView` | `@usuario_or_admin_required` |
| `<int:pk>/editar/` | `viajes:viaje_update` | GET, POST | `ViajeUpdateView` | `@admin_required` |
| `<int:pk>/eliminar/` | `viajes:viaje_delete` | GET, POST | `ViajeDeleteView` | `@admin_required` |
| `<int:viaje_id>/pasajeros/` | `viajes:viaje_pasajeros` | GET | `viaje_pasajeros_view` | `@login_required` |
| `<int:viaje_id>/pasajeros/agregar/<int:pasajero_id>/` | `viajes:agregar_pasajero_viaje` | POST | `agregar_pasajero_viaje` | `@login_required` |
| `<int:viaje_id>/pasajeros/quitar/<int:pasajero_id>/` | `viajes:quitar_pasajero_viaje` | POST | `quitar_pasajero_viaje` | `@login_required` |
| `<int:viaje_id>/pasajeros/editar/<int:pasajero_id>/` | `viajes:editar_pasajero_viaje` | GET, POST | `editar_pasajero_viaje` | `@login_required` |

---

## 💰 Módulo: Costos

**Prefijo**: `/costos/`  
**Protección General**: `@admin_required`

| Ruta | Nombre | Método HTTP | Vista | Descripción |
|------|--------|------------|-------|-------------|
| `` | `costos:index` | GET | `CostosListView` | Listar costos |
| `crear/` | `costos:create` | GET, POST | `CostosCreateView` | Crear costo |
| `<int:pk>/editar/` | `costos:update` | GET, POST | `CostosUpdateView` | Editar costo |
| `<int:pk>/eliminar/` | `costos:delete` | GET, POST | `CostosDeleteView` | Eliminar costo |

---

## 🔑 Cómo Usar las URLs en Templates

### Enlace Simple
```django
<a href="{% url 'home' %}">Inicio</a>
<a href="{% url 'flota:bus_list' %}">Buses</a>
```

### Con Parámetro
```django
<a href="{% url 'flota:bus_detail' pk=bus.id %}">Ver Detalles</a>
<a href="{% url 'flota:bus_update' pk=bus.id %}">Editar</a>
```

### En URLs de Django
```python
# core/urls.py
from django.urls import path, include

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('conductores/', ConductorListView.as_view(), name='conductor_list'),
]

# Incluidas en urls.py principal:
urlpatterns = [
    path('core/', include('core.urls')),
    path('flota/', include('flota.urls', namespace='flota')),
]
```

---

## 🔐 Matriz de Acceso por Rol

### Admin (Superusuario)

| Módulo | List | Create | Detail | Update | Delete |
|--------|------|--------|--------|--------|--------|
| Buses | ✅ | ✅ | ✅ | ✅ | ✅ |
| Conductores | ✅ | ✅ | ✅ | ✅ | ✅ |
| Viajes | ✅ | ✅ | ✅ | ✅ | ✅ |
| Lugares | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pasajeros | ✅ | ✅ | ✅ | ✅ | ✅ |

### Usuario Regular

| Módulo | List | Create | Detail | Update | Delete |
|--------|------|--------|--------|--------|--------|
| Buses | ❌ | ❌ | ❌ | ❌ | ❌ |
| Conductores | ❌ | ❌ | ❌ | ❌ | ❌ |
| Viajes | ✅ | ✅ | ✅ | ❌ | ❌ |
| Lugares | ✅ | ✅ | ✅ | ❌ | ❌ |
| Pasajeros | ✅ | ✅ | ✅ | ❌ | ❌ |

### No Autenticado

- ❌ Acceso a cualquier sección
- ✅ Solo puede acceder a `/core/login/`
- Redirección automática a login

---

## 📱 Rutas por Aplicación

### App: `core` (Sin namespace)
```
/core/login/
/core/logout/
/core/conductores/...
/core/lugares/...
/core/pasajeros/...
```

### App: `flota` (Namespace: `flota`)
```
/flota/buses/...
/flota/mantenimientos/...
/flota/documentos/...
```

### App: `viajes` (Namespace: `viajes`)
```
/viajes/...
/viajes/crear/...
/viajes/<id>/...
```

### App: `costos` (Namespace: `costos`)
```
/costos/...
/costos/crear/...
```

---

## 🧪 Testear URLs

### En Django Shell
```bash
python manage.py shell
>>> from django.urls import reverse
>>> reverse('home')
'/'
>>> reverse('flota:bus_list')
'/flota/buses/'
>>> reverse('flota:bus_detail', kwargs={'pk': 1})
'/flota/buses/1/'
```

### En Tests
```python
from django.test import TestCase
from django.urls import reverse

class BusURLTests(TestCase):
    def test_bus_list_url(self):
        url = reverse('flota:bus_list')
        self.assertEqual(url, '/flota/buses/')
```

---

## ⚠️ Rutas Protegidas

Todas las rutas excepto `login/` y `logout/` requieren autenticación.

Si intenta acceder sin autenticación:
1. Django redirige a `LOGIN_URL` (por defecto `/core/login/`)
2. Después de login, redirige a `LOGIN_REDIRECT_URL` (por defecto `/home/`)

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
