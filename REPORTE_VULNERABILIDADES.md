# 🔍 Reporte de Escaneo de Dependencias

**Fecha:** 17 de diciembre de 2025  
**Herramienta:** pip-audit  
**Tema:** OWASP #6 - Vulnerable and Outdated Components

---

## ⚠️ Vulnerabilidades Encontradas

### Resumen
- **Total de vulnerabilidades:** 13
- **Paquetes vulnerables:** 7
- **Severidad:** Media-Alta (requiere actualización)

---

## 📋 Vulnerabilidades por Paquete

### 🔴 CRÍTICO - ACTUALIZAR AHORA

#### 1. **Django 5.2.8** → Actualizar a 5.2.9
```
CVE-2025-13372: Vulnerability in Django 5.2.8
CVE-2025-64460: Vulnerability in Django 5.2.8
```
**Impacto:** Vulnerabilidades en seguridad de Django  
**Solución:**
```bash
pip install --upgrade Django==5.2.9
```

#### 2. **Jinja2 3.1.4** → Actualizar a 3.1.6
```
CVE-2024-56326: Jinja2 vulnerability
CVE-2024-56201: Jinja2 vulnerability
CVE-2025-27516: Jinja2 vulnerability
```
**Impacto:** Vulnerabilidades en templating (posible XSS)  
**Solución:**
```bash
pip install --upgrade Jinja2==3.1.6
```

#### 3. **urllib3 2.2.3** → Actualizar a 2.6.0
```
CVE-2025-50182: urllib3 vulnerability
CVE-2025-50181: urllib3 vulnerability
CVE-2025-66418: urllib3 vulnerability
CVE-2025-66471: urllib3 vulnerability
```
**Impacto:** Vulnerabilidades en conexiones HTTPS  
**Solución:**
```bash
pip install --upgrade urllib3==2.6.0
```

---

### 🟠 ALTO - ACTUALIZAR PRONTO

#### 4. **requests 2.32.3** → Actualizar a 2.32.4
```
CVE-2024-47081: requests vulnerability
```
**Solución:**
```bash
pip install --upgrade requests==2.32.4
```

#### 5. **djangorestframework 3.14.0** → Actualizar a 3.15.2
```
CVE-2024-21520: DRF vulnerability
```
**Solución:**
```bash
pip install --upgrade djangorestframework==3.15.2
```

#### 6. **djangorestframework-simplejwt 5.3.0** → Actualizar a 5.5.1
```
CVE-2024-22513: JWT vulnerability
```
**Solución:**
```bash
pip install --upgrade djangorestframework-simplejwt==5.5.1
```

#### 7. **pip 25.1.1** → Actualizar a 25.3
```
CVE-2025-8869: pip vulnerability
```
**Solución:**
```bash
pip install --upgrade pip==25.3
```

---

## 🚀 Cómo Actualizar TODO Rápido

### Opción 1: Actualizar un paquete
```bash
pip install --upgrade Django==5.2.9
```

### Opción 2: Actualizar todos
```bash
pip install --upgrade Django==5.2.9 Jinja2==3.1.6 urllib3==2.6.0 requests==2.32.4 djangorestframework==3.15.2 djangorestframework-simplejwt==5.5.1 pip==25.3
```

### Opción 3: Usar requirements.txt
```bash
pip install -r requirements.txt --upgrade
```

---

## 📝 Actualizar `requirements.txt`

**Cambios recomendados:**
```diff
- Django>=5.0
+ Django==5.2.9

- Jinja2 (implícita en Django)
+ Jinja2==3.1.6

- requests>=2.31.0
+ requests==2.32.4

+ urllib3==2.6.0
+ djangorestframework==3.15.2
+ djangorestframework-simplejwt==5.5.1
```

---

## ✅ Cómo Verificar que Funcionó

Después de actualizar, ejecutar de nuevo:
```bash
pip-audit
```

**Resultado esperado:**
```
No known vulnerabilities found  ✅
```

---

## 🔄 Automatizar Escaneos Futuros

### En tu CI/CD (GitHub Actions, GitLab CI, etc.)
```yaml
- name: Scan for vulnerabilities
  run: pip-audit
```

### Ejecutar regularmente
```bash
# Semanalmente
0 0 * * 0 pip-audit
```

---

## 📚 Referencias

- [OWASP #6: Vulnerable and Outdated Components](https://owasp.org/www-project-top-ten/2021/A06_2021-Vulnerable_and_Outdated_Components/)
- [pip-audit Documentation](https://github.com/pypa/pip-audit)
- [Django Security Releases](https://docs.djangoproject.com/en/5.2/releases/security/)

---

## 🎯 Resumen de Acciones

| Tarea | Urgencia | Estado |
|-------|----------|--------|
| Actualizar Django 5.2.9 | 🔴 Crítico | ⏳ Pendiente |
| Actualizar Jinja2 3.1.6 | 🔴 Crítico | ⏳ Pendiente |
| Actualizar urllib3 2.6.0 | 🔴 Crítico | ⏳ Pendiente |
| Actualizar requests 2.32.4 | 🟠 Alto | ⏳ Pendiente |
| Actualizar DRF 3.15.2 | 🟠 Alto | ⏳ Pendiente |
| Actualizar JWT 5.5.1 | 🟠 Alto | ⏳ Pendiente |
| Actualizar pip 25.3 | 🟠 Alto | ⏳ Pendiente |

**Tiempo estimado para actualizar todas:** ~5 minutos

