# ✅ REQUISITOS Y VERIFICACIÓN DE INSTALACIÓN

## 🔍 REQUISITOS MÍNIMOS PARA INSTALAR EN OTRA PC

### **Sistema Operativo**
- ✅ Windows 10/11 (Recomendado)
- ✅ Linux (Ubuntu 18.04+)
- ✅ macOS (Catalina+)

### **Software Obligatorio**

#### 1. **Python 3.8 o superior** (OBLIGATORIO)
- Descargar desde: https://www.python.org/downloads/
- **IMPORTANTE**: Durante la instalación, marcar "Add Python to PATH"
- Verificar: `python --version` (debe mostrar 3.8+)

#### 2. **MySQL 8.0 o superior** (OBLIGATORIO)
Opciones de instalación:

**Opción A: XAMPP (Recomendado para principiantes)**
- Descargar desde: https://www.apachefriends.org/
- Instala Apache, MySQL y phpMyAdmin
- Iniciar XAMPP Control Panel y activar MySQL

**Opción B: WAMP**
- Descargar desde: http://www.wampserver.com/
- Iniciar WAMP y verificar que MySQL esté verde

**Opción C: Instalación directa de MySQL**
- Descargar desde: https://dev.mysql.com/downloads/mysql/
- Instalar normalmente
- Verificar que el servicio "MySQL" esté ejecutándose en Servicios

### **Requisitos Opcionales pero Recomendados**

- **Git** (para clonar desde GitHub): https://git-scm.com/
- **Visual Studio Code** (editor): https://code.visualstudio.com/
- **Navegador moderno** (Chrome, Firefox, Edge)

---

## ✅ VERIFICACIÓN PRE-INSTALACIÓN

Antes de ejecutar INSTALAR.bat, verifica:

### **1. Python instalado correctamente**
```bash
python --version
# Resultado esperado: Python 3.8.x o superior
```

### **2. MySQL ejecutándose**
```bash
# En Windows, abre Services (servicios) y verifica MySQL8.0 está "Running"
# O en XAMPP, verifica que MySQL esté verde
```

### **3. Permisos de carpeta**
- Asegúrate de que la carpeta del proyecto NO está protegida
- No instalar en "Program Files" (puede causar problemas)
- Instalar en: `C:\Users\[Tu Usuario]\Desktop\` o similar

---

## 🚀 PROCESO DE INSTALACIÓN PASO A PASO

### **Opción 1: Descargada desde GitHub**

```bash
# 1. Descargar el ZIP desde GitHub
# O clonar con Git:
git clone https://github.com/[usuario]/proyecto_flota.git
cd proyecto_flota

# 2. INSTALAR (doble click en INSTALAR.bat)
# O desde terminal:
python instalar.py

# 3. EJECUTAR (doble click en EJECUTAR.bat)
# Se abrirá ventana gráfica del launcher

# 4. Hacer click en "INICIAR SISTEMA"
# El servidor iniciará en http://127.0.0.1:8000/
```

### **Opción 2: Instalación manual (Usuarios avanzados)**

```bash
# 1. Entrar a la carpeta
cd proyecto_flota

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear archivo .env (copiar desde .env.example)
copy .env.example .env

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear usuarios por defecto (opcional)
python initialize_system.py

# 6. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 7. Iniciar servidor
python manage.py runserver
```

---

## 🔐 CREDENCIALES POR DEFECTO (Después de instalar)

| Rol | Usuario | Contraseña |
|-----|---------|-----------|
| Regular | `usuario` | `pene1234` |
| Admin | `admin` | `NOSE_4321` |

⚠️ **CAMBIAR ESTAS CONTRASEÑAS INMEDIATAMENTE DESPUÉS DE LA PRIMERA INSTALACIÓN**

---

## ❓ SOLUCIÓN DE PROBLEMAS COMUNES

### **Error: "Python no está instalado"**
- Asegúrate de marcar "Add Python to PATH" al instalar
- Reinicia la PC después de instalar Python

### **Error: "MySQL no está ejecutándose"**
- Abre XAMPP Control Panel y haz click en "Start" para MySQL
- O abre Servicios (services.msc) y verifica MySQL8.0 esté "Running"

### **Error: "No se puede conectar a la base de datos"**
- Verifica que MySQL esté ejecutándose
- Verifica usuario: `root` y contraseña en `.env`
- Por defecto la contraseña es vacía

### **Error: "Puerto 8000 ya está en uso"**
- Ejecuta en terminal: `netstat -ano | findstr :8000`
- Encuentra el proceso y termínalo, o cambia el puerto

### **Error: "Acceso denegado a carpeta"**
- No instalar en "Program Files"
- Ejecutar INSTALAR.bat como administrador (click derecho)

---

## ✅ VERIFICACIÓN DE INSTALACIÓN EXITOSA

Después de instalar, verifica:

```bash
# Ejecutar verificador
python verificar_instalacion.py

# Resultado esperado:
# ✓ Python OK
# ✓ Django OK
# ✓ MySQL OK
# ✓ Archivos estáticos OK
# ✓ Base de datos OK
```

---

## 📁 ARCHIVOS INCLUIDOS EN LA DISTRIBUCIÓN

Necesarios para instalar en otra PC:

```
✅ INSTALAR.bat                 - Script de instalación automática
✅ EJECUTAR.bat                 - Script para ejecutar el sistema
✅ instalar.py                  - Instalador Python
✅ launcher.py                  - Interfaz gráfica
✅ initialize_system.py         - Crear usuarios por defecto
✅ verificar_instalacion.py     - Verificar instalación
✅ manage.py                    - Django management
✅ requirements.txt             - Dependencias Python
✅ .env.example                 - Plantilla de configuración
✅ README.md                    - Guía principal
✅ GUIA_INSTALACION.md          - Guía detallada
✅ CONFIGURACION_EMAIL.md       - Configuración SMTP
✅ SEGURIDAD.md                 - Variables de entorno
✅ SOLUCION_PROBLEMAS.md        - Troubleshooting
✅ Carpetas (core, flota, costos, viajes, etc) - Código fuente
✅ templates/                   - Plantillas HTML
✅ static/                      - CSS, JavaScript
```

---

## 🎯 CHECKLIST FINAL

Antes de usar en producción:

- [ ] Python 3.8+ instalado con PATH configurado
- [ ] MySQL 8.0+ ejecutándose
- [ ] INSTALAR.bat ejecutado exitosamente
- [ ] verificar_instalacion.py pasó todas las verificaciones
- [ ] Puedes acceder a http://127.0.0.1:8000/
- [ ] Puedes iniciar sesión con usuario/admin
- [ ] Puedes cambiar contraseñas de usuarios
- [ ] Email está configurado (opcional)
- [ ] Contraseñas por defecto han sido cambiadas

---

## 📞 SOPORTE

Si tienes problemas:

1. Revisa `SOLUCION_PROBLEMAS.md`
2. Revisa `CONFIGURACION_EMAIL.md` si hay errores de email
3. Revisa `SEGURIDAD.md` para variables de entorno
4. Ejecuta `python verificar_instalacion.py` para diagnosticar

---

**Última actualización**: 22 de diciembre de 2025
**Estado**: LISTO PARA DISTRIBUCIÓN ✅
