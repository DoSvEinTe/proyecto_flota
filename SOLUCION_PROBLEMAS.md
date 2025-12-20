# 🔧 SOLUCIÓN DE PROBLEMAS AVANZADA

## 🆘 PROBLEMAS DURANTE LA INSTALACIÓN

### **"pip: El término no se reconoce"**

**Causa**: Python no está en PATH

**Solución**:
1. Instala Python nuevamente desde https://www.python.org/
2. **IMPORTANTE**: Marca "Add Python to PATH"
3. Reinicia la computadora
4. Intenta nuevamente

---

### **"mysqlclient falla al instalar"**

**Causa**: Faltan herramientas de compilación en Windows

**Solución rápida**:
1. Abre PowerShell como Administrador
2. Ejecuta:
   ```powershell
   pip install mysqlclient --only-binary :all:
   ```

**Solución completa**:
1. Instala "Microsoft C++ Build Tools"
2. Descarga desde: https://visualstudio.microsoft.com/es/visual-cpp-build-tools/
3. Ejecuta nuevamente `INSTALAR.bat`

---

### **"Error: ModuleNotFoundError"**

**Causa**: Dependencias no instaladas correctamente

**Solución**:
```bash
# Abre PowerShell en la carpeta del proyecto y ejecuta:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --force-reinstall
```

---

## 🌐 PROBLEMAS CON BASE DE DATOS

### **"can't connect to MySQL server"**

**Causa**: MySQL no está ejecutándose

**Solución**:

**Si tienes XAMPP**:
1. Abre XAMPP Control Panel
2. Haz click en "Start" para MySQL
3. Espera a que se ponga en verde

**Si tienes WAMP**:
1. Abre WAMP
2. Verifica que MySQL esté en verde

**Si tienes MySQL instalado solo**:
1. Presiona `Win + R`
2. Escribe: `services.msc`
3. Busca "MySQL80" (o similar)
4. Click derecho → "Iniciar"

---

### **"Access denied for user 'root'@'localhost'"**

**Causa**: Contraseña incorrecta en `.env`

**Solución**:
1. Abre el archivo `.env` con Bloc de Notas
2. Verifica que dice:
   ```
   DB_USER=root
   DB_PASSWORD=Contra.12
   ```
3. Si tu contraseña es diferente, cámbiala
4. Reinicia el servidor

---

### **"Unknown database 'flota_db'"**

**Causa**: La base de datos no existe

**Solución**:
1. Abre http://localhost/phpmyadmin
2. Click en "Nueva" (parte superior)
3. Nombre: `flota_db`
4. Collation: `utf8_unicode_ci`
5. Click en "Crear"
6. Ejecuta nuevamente `INSTALAR.bat`

---

## 🌐 PROBLEMAS DE PUERTO

### **"port 8000 already in use" o "Puerto 8000 en uso"**

**Causa**: Ya hay otro programa usando ese puerto

**Solución A** (Rápida):
1. Cierra todas las instancias de FlotaGest
2. Cierra el navegador
3. Intenta nuevamente

**Solución B** (Cambiar puerto):
1. Abre `launcher.py` con Bloc de Notas
2. Busca: `"runserver"`
3. Reemplaza por: `"runserver", "8001"`
4. Guarda
5. Intenta nuevamente

**Solución C** (Liberar puerto desde PowerShell):
```powershell
# Como Administrador:
netstat -ano | findstr :8000
taskkill /PID [número_pid] /F
```

---

## 🌍 PROBLEMAS DE NAVEGADOR

### **"No se puede acceder a http://127.0.0.1:8000/"**

**Causa**: El servidor tardó en iniciar

**Solución**:
1. Espera 10 segundos
2. Presiona F5 para refrescar
3. Intenta con un navegador diferente (Chrome, Firefox)

---

### **"Página en blanco" o "Error 500"**

**Causa**: Error en la aplicación Django

**Solución**:
1. Revisa si hay errores en la consola (ventana de PowerShell)
2. Toma captura de pantalla del error
3. Detén el servidor
4. Ejecuta:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```
5. Reinicia el servidor

---

## 💾 PROBLEMAS DE ARCHIVOS

### **"Permission denied" o "Acceso denegado"**

**Causa**: Permisos insuficientes

**Solución**:
1. Cierra todos los programas que accedan a la carpeta
2. Cierra el navegador
3. Detén el servidor
4. Intenta nuevamente

---

### **"File not found" o "Archivo no encontrado"**

**Causa**: Ruta incorrecta

**Solución**:
1. Verifica que la carpeta NO tenga caracteres especiales
2. Verifica que NO tenga espacios en el nombre
3. Mueve a: `C:\Proyectos\flota`

---

## 📧 PROBLEMAS DE EMAIL

### **"SMTPAuthenticationError"**

**Causa**: Credenciales de Gmail incorrectas

**Solución**:
1. Usa "Contraseña de Aplicación" (no la contraseña normal)
2. Ve a: https://myaccount.google.com/
3. Seguridad → Contraseñas de aplicación
4. Genera una para Gmail
5. Cópiala en `.env` en `EMAIL_HOST_PASSWORD`

---

## 🔍 VERIFICAR QUE TODO FUNCIONA

### Ejecuta el script de verificación:

```bash
python verificar_sistema.py
```

Esto te dirá exactamente qué está bien y qué falta.

---

## 📊 INFORMACIÓN ÚTIL

### Ver logs del servidor:

1. Busca el archivo `servidor.log` en la carpeta del proyecto
2. Ábrelo con Bloc de Notas
3. Mira los errores

### Ver base de datos:

1. Abre http://localhost/phpmyadmin
2. Usuario: `root`
3. Contraseña: `Contra.12`
4. Verifica la tabla `flota_db`

### Ver puerto en uso:

```powershell
netstat -ano | findstr :8000
```

---

## 📞 SI NADA FUNCIONA

1. Ejecuta como Administrador
2. Reinicia la computadora
3. Ejecuta nuevamente `INSTALAR.bat`
4. Verifica todos los requisitos previos
5. Copia los logs del error
6. Contacta al soporte técnico

---

**¡La mayoría de problemas se resuelven con Reinstalar! 🔄**
