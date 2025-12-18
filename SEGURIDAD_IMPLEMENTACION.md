# 🔒 Implementación de Seguridad - OWASP Top 10

**Fecha:** 17 de diciembre de 2025  
**Estado:** ✅ Cambios críticos aplicados

---

## 📋 Cambios Realizados

### 1️⃣ **Configuración de DEBUG** (OWASP #5: Security Misconfiguration)

**Antes:**
```python
DEBUG = True
```

**Después:**
```python
DEBUG = config('DEBUG', default='False') == 'True'
```

✅ **Impacto:** En producción, `DEBUG=False` oculta tracebacks sensibles y mensajes de error detallados.

---

### 2️⃣ **Configuración de ALLOWED_HOSTS** (OWASP #5: Security Misconfiguration)

**Antes:**
```python
ALLOWED_HOSTS = []
```

**Después:**
```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
```

✅ **Impacto:** Previene ataques HTTP Host Header Injection. En `.env`:

```env
# Desarrollo
ALLOWED_HOSTS=localhost,127.0.0.1

# Producción
ALLOWED_HOSTS=mi-dominio.com,www.mi-dominio.com
```

---

### 3️⃣ **SECRET_KEY sin Fallback Inseguro** (OWASP #2: Cryptographic Failures)

**Antes:**
```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-change-in-production')
```

**Después:**
```python
SECRET_KEY = config('SECRET_KEY', default=None)
if not SECRET_KEY:
    raise ValueError(
        'La variable de entorno SECRET_KEY no está configurada. '
        'Añade SECRET_KEY a tu archivo .env en producción.'
    )
```

✅ **Impacto:** Fuerza que `SECRET_KEY` venga de variable de entorno. Genera error si no existe.

**Para generar una SECRET_KEY nueva:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 4️⃣ **Protección HTTPS/SSL** (OWASP #2: Cryptographic Failures)

**Añadido a settings.py:**
```python
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default='False') == 'True'
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default='False') == 'True'
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default='False') == 'True'
```

En `.env` para producción:
```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

✅ **Impacto:** 
- Redirige automáticamente HTTP → HTTPS
- Cookies solo se envían por HTTPS
- Previene ataques man-in-the-middle (MITM)

---

### 5️⃣ **HSTS (HTTP Strict-Transport-Security)** (OWASP #2: Cryptographic Failures)

**Añadido a settings.py:**
```python
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default='0', cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default='False') == 'True'
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default='False') == 'True'
```

En `.env` para producción (después de probar):
```env
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

✅ **Impacto:** 
- HSTS obliga a navegadores a usar HTTPS siempre
- 31536000 segundos = 1 año
- Preload permite incluir dominio en listas HSTS de navegadores

---

### 6️⃣ **Cookies Seguras y HTTPOnly** (OWASP #2: Cryptographic Failures)

**Añadido a settings.py:**
```python
SESSION_COOKIE_HTTPONLY = True      # Previene acceso JS
CSRF_COOKIE_HTTPONLY = False        # Django lo requiere así
```

✅ **Impacto:** 
- `HTTPOnly` previene robo de cookies vía JavaScript (XSS)
- Sesiones solo accesibles desde servidor

---

### 7️⃣ **Protección XSS** (OWASP #10: Cross-Site Scripting)

**Añadido a settings.py:**
```python
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

✅ **Impacto:** 
- XSS Filter: navegadores detectan XSS reflejado
- DENY: previene clickjacking (app no puede ser frame)

---

### 8️⃣ **Activación Automática en Producción**

**Añadido a settings.py:**
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

✅ **Impacto:** Cuando `DEBUG=False` (producción), todas las protecciones se activan automáticamente.

---

## 🚀 Cómo Implementar en Producción

### Paso 1: Copiar y configurar `.env`

```bash
cp .env.example .env
```

Editar `.env` con valores de producción:
```env
SECRET_KEY=<generar-con-comando-arriba>
DEBUG=False
ALLOWED_HOSTS=mi-dominio.com,www.mi-dominio.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Paso 2: Asegurar HTTPS

- Obtener certificado SSL (Let's Encrypt gratuito)
- Configurar en servidor web (Nginx, Apache)
- Redirigir HTTP → HTTPS

### Paso 3: Verificar configuración

```bash
python manage.py check --deploy
```

Debería mostrar "System check identified no issues."

### Paso 4: Testear en staging primero

Antes de activar en producción, probar HSTS en staging:
```env
SECURE_HSTS_SECONDS=3600  # 1 hora
```

Si todo funciona, cambiar a 1 año (31536000).

---

## ✅ Checklist de Seguridad

- [x] DEBUG configurado según entorno
- [x] ALLOWED_HOSTS configurado
- [x] SECRET_KEY sin fallback inseguro
- [x] HTTPS/SSL configurado
- [x] Cookies seguras (Secure + HTTPOnly)
- [x] HSTS habilitado en producción
- [x] Protección XSS/clickjacking
- [ ] **FALTA:** Rate limiting en login (django-ratelimit)
- [ ] **FALTA:** MFA para admins (django-otp)
- [ ] **FALTA:** Logging/monitoring centralizado (Sentry)
- [ ] **FALTA:** Validación de uploads (tipo MIME, tamaño)
- [ ] **FALTA:** Escaneo de dependencias (pip-audit)

---

## 📊 Impacto en Funcionalidad

❌ **NO afecta:**
- Interfaz de usuario
- Operaciones (crear/editar/eliminar)
- Estética o diseño
- Experiencia del usuario (excepto páginas de error en prod)

✅ **Mejora:**
- Seguridad contra ataques comunes
- Protección de datos en tránsito
- Confianza del usuario
- Cumplimiento de estándares (OWASP)

---

## 🔍 Verificar Configuración Actual

```bash
python manage.py shell
```

```python
from django.conf import settings
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print(f"SECURE_HSTS_SECONDS: {settings.SECURE_HSTS_SECONDS}")
```

---

## 🆘 Troubleshooting

### "Variable de entorno SECRET_KEY no está configurada"
```bash
# Generar y añadir a .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### "Invalid HTTP_HOST header"
Añadir dominio a `ALLOWED_HOSTS` en `.env`

### "CSRF cookie not set"
Asegurar que `DEBUG=False` y cookies están configuradas

### "Certificado SSL/TLS no válido"
Usar `https://` con certificado válido antes de activar `SECURE_SSL_REDIRECT=True`

---

## 📚 Referencias

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)

