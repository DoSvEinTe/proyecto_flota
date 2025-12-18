# 🔐 Auditoría de Control de Acceso - OWASP #1

**Fecha:** 17 de diciembre de 2025  
**Problema:** Broken Access Control (IDOR - Insecure Direct Object References)

---

## ❓ ¿Qué es IDOR?

Un usuario accede a un objeto que NO debería poder acceder solo cambiando el ID en la URL.

**Ejemplo:**
```
Usuario 1 accede a: /viajes/10/editar
├─ Ve viaje suyo ✅

Usuario 1 cambia a: /viajes/11/editar
├─ Ve viaje de Usuario 2 ❌ IDOR ENCONTRADO
```

---

## 🔍 Dónde revisar en tu proyecto

### 1️⃣ **Vistas de Detalle** (DetailView)
**Archivos:** `viajes/views.py`, `flota/views.py`, `core/views.py`, `costos/views.py`

**Buscar:** Líneas con `DetailView` o `get_object_or_404`

**Verificar:**
```python
# ❌ INSEGURO - No valida permisos
class ViajeDetailView(DetailView):
    model = Viaje
    pk_url_kwarg = 'pk'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # FALTA: check_object_access(self.request.user, obj)
        return obj

# ✅ SEGURO - Valida que el usuario es propietario
class ViajeDetailView(DetailView):
    model = Viaje
    pk_url_kwarg = 'pk'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        check_object_access(self.request.user, obj)  # ← VALIDAR
        return obj
```

**Qué revisar:**
- [ ] ViajeDetailView / ViajeUpdateView / ViajeDeleteView
- [ ] ConductorDetailView / ConductorUpdateView
- [ ] CostosViajeDetailView / CostosViajeUpdateView
- [ ] BusDetailView / BusUpdateView
- [ ] DocumentoVehiculoDetailView
- [ ] PuntoRecargaDetailView / PuntoRecargaUpdateView
- [ ] PeajeDetailView / PeajeUpdateView

---

### 2️⃣ **Vistas de Actualización** (UpdateView)
**El peligro máximo:** Si un usuario sin permisos puede editar datos.

**Verificar:**
```python
# Antes de cada UPDATE/DELETE, validar:
def post(self, request, *args, **kwargs):
    obj = self.get_object()
    check_object_access(request.user, obj)  # ← AGREGAR ESTA LÍNEA
    return super().post(request, *args, **kwargs)
```

---

### 3️⃣ **Vistas de Lista** (ListView)
**El peligro:** Si un Usuario ve viajes/costos de otros usuarios.

**Verificar:**
```python
# ❌ INSEGURO - Todos ven todos los viajes
class ViajeListView(ListView):
    queryset = Viaje.objects.all()

# ✅ SEGURO - Cada usuario ve solo los suyos
class ViajeListView(ListView):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Viaje.objects.all()  # Admin ve todos
        
        # Usuario normal: solo sus viajes
        return Viaje.objects.filter(usuario=self.request.user)
```

**Qué revisar:**
- [ ] ViajeListView - ¿Filtra por usuario?
- [ ] CostosViajeListView - ¿Filtra por usuario?
- [ ] PeajeListView - ¿Filtra por usuario?

---

### 4️⃣ **APIs/AJAX** (si existen)
**El peligro:** Endpoints que devuelven datos sin validar acceso.

**Buscar:** `@csrf_exempt`, `JsonResponse`, `@api_view`, endpoints AJAX

**Verificar:**
```python
# ❌ INSEGURO - Devuelve datos sin validar
def get_costos_ajax(request, viaje_id):
    costos = CostosViaje.objects.get(viaje_id=viaje_id)
    return JsonResponse(costos.datos)

# ✅ SEGURO - Valida acceso
def get_costos_ajax(request, viaje_id):
    viaje = Viaje.objects.get(id=viaje_id)
    check_object_access(request.user, viaje)
    costos = viaje.costos
    return JsonResponse(costos.datos)
```

---

## ✅ Checklist de Auditoría

### Viajes
- [ ] DetailView valida acceso
- [ ] UpdateView valida acceso
- [ ] DeleteView valida acceso
- [ ] ListView filtra por usuario
- [ ] APIs validan acceso

### Conductores
- [ ] Solo admin puede ver todos
- [ ] UpdateView requiere admin
- [ ] DeleteView requiere admin

### Costos
- [ ] Solo admin o propietario del viaje puede ver
- [ ] UpdateView valida acceso al viaje
- [ ] DeleteView valida acceso al viaje

### Documentos/Comprobantes
- [ ] Descarga valida acceso (ya tiene `@admin_required`)
- [ ] Edición valida acceso
- [ ] Eliminación valida acceso

---

## 📝 Cómo Implementar Rápido

**Paso 1:** Importar función en vista
```python
from core.access_control import check_object_access, validate_viaje_access
```

**Paso 2:** Usar en vistas
```python
class ViajeDetailView(DetailView):
    model = Viaje
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        validate_viaje_access(self.request, obj)  # ← AGREGAR
        return obj
```

**Paso 3:** Usar en ListViews
```python
class ViajeListView(ListView):
    model = Viaje
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Viaje.objects.all()
        return Viaje.objects.filter(usuario=self.request.user)
```

---

## ⚠️ Falsos Positivos a Evitar

**Algunos accesos SÍ deben ser públicos:**
- [ ] Listar lugares (origen/destino)
- [ ] Ver horarios/rutas públicas
- [ ] Páginas estáticas (home, contacto)

**Estos SÍ requieren validación:**
- [ ] Ver detalles de viaje (costo, conductor, etc.)
- [ ] Editar/borrar cualquier dato
- [ ] Descargar comprobantes/documentos
- [ ] Ver costos/análisis

---

## 🧪 Cómo Testear

### Test 1: Intento IDOR
```bash
# 1. Login como Usuario 1
curl -c cookies.txt http://localhost:8000/login/ -d "username=user1&password=pass"

# 2. Intentar acceder a viaje de Usuario 2
curl -b cookies.txt http://localhost:8000/viajes/2/editar

# Resultado esperado: 403 Forbidden ✅
# Resultado malo: 200 OK + datos ajenos ❌
```

### Test 2: DetailView sin permisos
```python
# En tests.py
from django.test import TestCase, Client

class ViajeAccessTest(TestCase):
    def test_user_cannot_view_other_user_viaje(self):
        user1 = User.objects.create_user('user1', 'pass1')
        user2 = User.objects.create_user('user2', 'pass2')
        
        viaje = Viaje.objects.create(usuario=user1, ...)
        
        client = Client()
        client.login(username='user2', password='pass2')
        
        response = client.get(f'/viajes/{viaje.id}/')
        self.assertEqual(response.status_code, 403)  # ← Esperar 403
```

---

## 🔗 Referencias

- [Django: Autorización](https://docs.djangoproject.com/en/5.2/topics/auth/default/)
- [OWASP #1: Broken Access Control](https://owasp.org/www-project-top-ten/2021/A01_2021-Broken_Access_Control/)
- [IDOR - Insecure Direct Object Reference](https://owasp.org/www-community/attacks/Insecure_Direct_Object_References)

