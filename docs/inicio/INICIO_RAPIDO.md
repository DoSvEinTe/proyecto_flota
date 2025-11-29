# 🚀 Guía Rápida de Inicio

## En 5 minutos: Activar el Sistema

### Paso 1: Instalar Dependencias (1 minuto)
```bash
pip install -r requirements.txt
```

### Paso 2: Migrar Base de Datos (1 minuto)
```bash
python manage.py migrate
```

### Paso 3: Recolectar Archivos Estáticos (1 minuto)
```bash
python manage.py collectstatic --noinput
```

### Paso 4: Crear Usuarios (1 minuto)
```bash
python setup_auth.py
```

Esto crea:
- **Usuario Admin**: `admin` / `admin123`
- **Usuario Regular**: `usuario` / `usuario123`

### Paso 5: Ejecutar Servidor (1 minuto)
```bash
python manage.py runserver
```

**¡Listo!** Accede a: http://localhost:8000

---

## Verificar que Todo Funciona

### ✅ Test Rápido
```bash
python verificar_auth.py
```

Debería mostrar:
```
✓ Usuarios: 2 encontrados
✓ Grupos: 2 encontrados
✓ Sistema funcionando correctamente
```

### ✅ Prueba en Navegador

1. Ve a http://localhost:8000
2. Deberías ver la **página de login**
3. Ingresa: `admin` / `admin123`
4. Deberías ver el **dashboard** con estadísticas

---

## Comandos Esenciales

```bash
# Verificar configuración
python manage.py check

# Ver usuarios
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Crear superusuario adicional
python manage.py createsuperuser

# Resetear base de datos (cuidado)
python manage.py flush

# Ver todas las rutas
python manage.py show_urls
```

---

## Solución de Problemas Rápida

### "No se conecta a la BD"
- Verifica MySQL está corriendo
- Comprueba credenciales en `sistema_flota/settings.py`
- BD debe existir: `CREATE DATABASE db_flota;`

### "Los estilos no se cargan"
- Ejecuta: `python manage.py collectstatic --noinput`
- Limpia caché: Ctrl+F5 (Windows) o Cmd+Shift+R (Mac)

### "Login no funciona"
- Ejecuta: `python setup_auth.py`
- O: `python verificar_auth.py` para ver si existen usuarios

### "Error en migraciones"
- Ejecuta: `python manage.py migrate --run-syncdb`
- O: Elimina `db_flota` y recreala

---

## ¿Cuál es mi Rol?

### 👑 Admin (admin/admin123)
Ve y maneja:
- ✅ Buses
- ✅ Conductores
- ✅ Viajes (CRUD completo)
- ✅ Lugares (CRUD completo)
- ✅ Pasajeros (CRUD completo)
- ✅ Admin Django (/admin/)

### 👤 Usuario (usuario/usuario123)
Ve y maneja:
- ✅ Viajes (Ver, Crear)
- ✅ Lugares (Ver, Crear)
- ✅ Pasajeros (Ver, Crear)
- ❌ No puede: Editar, Eliminar
- ❌ No ve: Buses, Conductores

---

## Próximos Pasos

1. **Leer README.md** para entender el proyecto
2. **Explorar docs/INDICE_MAESTRO.md** para toda la documentación
3. **Leer GUIA_ESTRUCTURA.md** para entender la arquitectura
4. **Personalizar con GUIA_ESTILOS.md** si quieres cambiar colores

---

## Links Útiles

| Recurso | URL |
|---------|-----|
| Inicio | http://localhost:8000 |
| Admin Django | http://localhost:8000/admin/ |
| Buses | http://localhost:8000/flota/buses/ |
| Viajes | http://localhost:8000/viajes/ |
| Lugares | http://localhost:8000/core/lugares/ |
| Login | http://localhost:8000/core/login/ |

---

**¡Disfruta del sistema!** 🚀
