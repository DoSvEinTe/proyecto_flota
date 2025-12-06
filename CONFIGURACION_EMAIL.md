# Configuración de Email para Gmail

## Requisitos
- Cuenta de Gmail
- Verificación en 2 pasos activada
- Contraseña de aplicación generada

## Pasos para Configurar

### 1. Activar Verificación en 2 Pasos

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. En el menú izquierdo, haz clic en **Seguridad**
3. En la sección "Cómo inicias sesión en Google", haz clic en **Verificación en dos pasos**
4. Sigue los pasos para activarla (necesitarás tu teléfono)

### 2. Generar Contraseña de Aplicación

1. Una vez activada la verificación en 2 pasos, regresa a **Seguridad**
2. Busca **Contraseñas de aplicaciones** (al final de la sección "Cómo inicias sesión en Google")
3. Haz clic en **Contraseñas de aplicaciones**
4. Te pedirá tu contraseña de Gmail
5. En "Seleccionar aplicación", elige **Correo**
6. En "Seleccionar dispositivo", elige **Windows Computer** (o el que uses)
7. Haz clic en **Generar**
8. Google generará una contraseña de 16 caracteres (algo como: `abcd efgh ijkl mnop`)
9. **COPIA ESTA CONTRASEÑA** (no podrás verla de nuevo)

### 3. Configurar Variables de Entorno

#### Opción A: Usando archivo .env (Recomendado para desarrollo)

1. Instala python-decouple:
   ```bash
   pip install python-decouple
   ```

2. Crea un archivo `.env` en la raíz del proyecto (copia desde `.env.example`):
   ```bash
   copy .env.example .env
   ```

3. Edita el archivo `.env` con tus datos:
   ```
   EMAIL_HOST_USER=tu_correo@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   **Nota**: La contraseña va SIN ESPACIOS (quita los espacios que Gmail muestra)

4. Actualiza `settings.py` para usar decouple:
   ```python
   from decouple import config
   
   EMAIL_HOST_USER = config('EMAIL_HOST_USER')
   EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
   ```

#### Opción B: Variables de Entorno del Sistema (Recomendado para producción)

**En Windows (PowerShell):**
```powershell
$env:EMAIL_HOST_USER = "tu_correo@gmail.com"
$env:EMAIL_HOST_PASSWORD = "abcdefghijklmnop"
```

Para hacerlo permanente:
```powershell
[System.Environment]::SetEnvironmentVariable('EMAIL_HOST_USER', 'tu_correo@gmail.com', 'User')
[System.Environment]::SetEnvironmentVariable('EMAIL_HOST_PASSWORD', 'abcdefghijklmnop', 'User')
```

### 4. Probar la Configuración

Ejecuta el servidor y prueba el botón de Email en la página de Gestión de Costos:
```bash
python manage.py runserver
```

Ve a: http://127.0.0.1:8000/costos/

Haz clic en el botón **Email** de algún viaje. Deberías ver un mensaje de éxito y el conductor recibirá el email.

## Solución de Problemas

### Error: "Authentication failed"
- Verifica que la contraseña de aplicación esté correcta (sin espacios)
- Asegúrate de que la verificación en 2 pasos esté activada
- Intenta generar una nueva contraseña de aplicación

### Error: "SMTPException: STARTTLS extension not supported"
- Verifica que `EMAIL_USE_TLS = True` esté configurado en settings.py
- Asegúrate de usar el puerto 587

### El conductor no recibe el email
- Verifica que el conductor tenga un email registrado en el sistema
- Revisa la carpeta de Spam del conductor
- Verifica que el email del conductor sea correcto

### Error: "No module named 'decouple'"
- Instala python-decouple: `pip install python-decouple`

## Seguridad

⚠️ **IMPORTANTE:**
- NUNCA compartas tu contraseña de aplicación
- NUNCA subas el archivo `.env` a GitHub
- El archivo `.env` debe estar en `.gitignore`
- En producción, usa variables de entorno del servidor

## Formato del Email

El email enviado incluye:
- **Asunto**: `Formulario de Costos - Viaje [PLACA] ([FECHA])`
- **Cuerpo**: 
  - Saludo personalizado al conductor
  - Detalles del viaje (bus, ruta, fecha, estado)
  - Instrucciones para editar PDF en móviles
  - Aplicaciones recomendadas (Adobe Reader, Xodo, Foxit)
  - Enlaces a tiendas de aplicaciones
- **Adjunto**: PDF interactivo con formulario de costos

## Configuración Actual en settings.py

```python
# Email Configuration (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', 'noreply@flotagest.com')
```
