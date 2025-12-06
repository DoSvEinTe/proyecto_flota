# 🔒 Configuración de Seguridad

## Variables de Entorno

Este proyecto usa variables de entorno para mantener las credenciales seguras y fuera del control de versiones.

### Configuración Inicial

1. **Copia el archivo de ejemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Edita el archivo `.env` con tus credenciales reales:**
   ```env
   EMAIL_HOST_USER=tu_correo@gmail.com
   EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion_aqui
   ```

### ⚠️ IMPORTANTE

- **NUNCA** subas el archivo `.env` a GitHub
- El archivo `.env` ya está incluido en `.gitignore`
- Solo comparte credenciales de forma segura (nunca por email o chat público)

### Generar Contraseña de Aplicación de Gmail

1. Ve a [Google Account](https://myaccount.google.com/)
2. **Seguridad** → **Verificación en 2 pasos** (debe estar activada)
3. **Contraseñas de aplicaciones**
4. Selecciona **Correo** y **Windows Computer**
5. Copia la contraseña de 16 caracteres generada
6. Pégala en `EMAIL_HOST_PASSWORD` en tu archivo `.env`

### Verificación

Para verificar que todo funciona correctamente:

```bash
python scripts/test_email.py
```

## Archivos Sensibles

Los siguientes archivos **NO deben** subirse a GitHub:

- `.env` - Credenciales locales
- `db.sqlite3` - Base de datos local
- `media/*` - Archivos subidos por usuarios
- `staticfiles/*` - Archivos estáticos recolectados

Todos estos ya están en `.gitignore`.
