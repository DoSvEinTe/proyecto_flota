# Solución al Error de Autenticación de Email

## Error que viste:
```
Error al enviar el correo: (530, b'5.7.0 Authentication Required')
```

## ✅ Solución Implementada

He configurado el sistema para que lea las credenciales desde el archivo `.env` usando `python-decouple`, lo que garantiza que siempre estén disponibles.

### Pasos para que funcione correctamente:

#### 1. **Reinicia el servidor Django** (IMPORTANTE)

Si tienes el servidor corriendo, debes reiniciarlo para que cargue la nueva configuración:

```powershell
# Detén el servidor (Ctrl+C)
# Luego inicia de nuevo:
python manage.py runserver
```

#### 2. Verifica que el archivo .env existe

El archivo `.env` debe estar en la raíz del proyecto con este contenido:

```
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
```

✅ Ya está creado y configurado

#### 3. Prueba el envío de email

Ve a: http://127.0.0.1:8000/costos/

Haz clic en el botón verde **"Email"** de algún viaje.

## ¿Por qué ocurrió el error?

Gmail requiere autenticación SMTP. El error ocurre cuando:
1. Las variables de entorno no están disponibles
2. El servidor Django no se reinició después de configurar las variables
3. La contraseña de aplicación es incorrecta

## Cambios Realizados

### 1. Instalado python-decouple
```bash
pip install python-decouple
```

### 2. Actualizado settings.py
Ahora usa `config()` de decouple en lugar de `os.environ.get()`:

```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```

Esto garantiza que las credenciales se carguen automáticamente desde `.env`

### 3. Actualizado requirements.txt
Agregado `python-decouple==3.8`

## Verificación

Ejecuta este comando para verificar que todo funciona:

```bash
python scripts/test_email.py
```

**Resultado esperado:**
```
✅ ¡Email enviado exitosamente!
   Revisa la bandeja de entrada de: tu_correo@gmail.com
```

## Si el Error Persiste

### Opción 1: Verificar credenciales en Django
```bash
python manage.py shell
```

Dentro del shell:
```python
from django.conf import settings
print(settings.EMAIL_HOST_USER)
print('Contraseña configurada:', bool(settings.EMAIL_HOST_PASSWORD))
```

Deberías ver:
```
tu_correo@gmail.com
Contraseña configurada: True
```

### Opción 2: Verificar archivo .env
```bash
cat .env
```

Debe mostrar:
```
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
```

### Opción 3: Verificar que el conductor tenga email

Si el error dice "El conductor no tiene email registrado":
1. Ve al Admin: http://127.0.0.1:8000/admin/
2. Busca el conductor en "Conductores"
3. Asegúrate de que tenga un email válido

## Prueba Rápida Ahora

1. **Reinicia el servidor**:
   ```bash
   python manage.py runserver
   ```

2. **Ve a**: http://127.0.0.1:8000/costos/

3. **Haz clic en "Email"** de un viaje

4. **Deberías ver**: 
   ```
   ✅ Formulario enviado exitosamente a [email del conductor]
   ```

## Notas Importantes

- ⚠️ **SIEMPRE reinicia el servidor** después de cambiar variables de entorno
- ✅ El archivo `.env` se carga automáticamente al iniciar Django
- ✅ No necesitas configurar variables en PowerShell cada vez
- ✅ Las credenciales están seguras (`.env` está en `.gitignore`)

## Contacto del Conductor

Para que funcione, el conductor debe tener un email registrado. Verifica en:
- Admin > Core > Conductores
- Busca el conductor del viaje
- Asegúrate de que el campo "Email" esté completo
