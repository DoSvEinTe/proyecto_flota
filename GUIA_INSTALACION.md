# 🚌 GUÍA DE INSTALACIÓN Y EJECUCIÓN - Sistema FlotaGest

## 📋 Pasos Rápidos (Usuario sin conocimientos técnicos)

### **PASO 1: Instalar Python (si no lo tienes)**

1. Descarga Python desde: https://www.python.org/downloads/
2. **IMPORTANTE**: Durante la instalación, marca la opción **"Add Python to PATH"**
3. Instala normalmente

### **PASO 2: Ejecutar el Instalador**

1. Abre el archivo `INSTALAR.bat` (doble click)
2. Espera a que termine (puede tomar 5-10 minutos)
3. Verás mensajes ✅ cuando termine

### **PASO 3: Iniciar el Sistema**

1. Abre el archivo `EJECUTAR.bat` (doble click)
2. Se abrirá una ventana visual
3. Haz click en **"▶ INICIAR SISTEMA"**
4. Espera 3-5 segundos hasta que se inicie

### **PASO 4: Acceder al Sistema**

1. Abre tu navegador web (Chrome, Firefox, Edge, etc.)
2. Ve a: **http://127.0.0.1:8000/**
3. ¡Listo! Usa el sistema

---

## ⚙️ REQUISITOS PREVIOS

### **MySQL debe estar ejecutándose**

- **Windows con XAMPP**: 
  - Abre XAMPP Control Panel
  - Haz click en "Start" para MySQL
  - Verás que se pone en verde

- **Windows con WAMP**:
  - Abre WAMP
  - Verifica que MySQL esté en verde

- **MySQL instalado directamente**:
  - Abre Services (servicios)
  - Busca "MySQL" y verifica que esté "Running"

**Usuario**: `root`  
**Contraseña**: `Contra.12` (configurada en `.env`)  
**Host**: `localhost:3306`

---

## 🔧 MÉTODO ALTERNATIVO: Crear EXE (Más Profesional)

Si quieres que tus usuarios solo hagan doble click en un EXE:

### **Paso 1: Instalar PyInstaller**

```bash
pip install pyinstaller
```

### **Paso 2: Crear el EXE**

```bash
pyinstaller --onefile --windowed --icon=icon.ico launcher.py
```

Esto crea una carpeta `dist/` con el archivo `launcher.exe`

### **Paso 3: Distribuir**

Crea una carpeta con:
```
flota/
  ├── INSTALAR.bat
  ├── launcher.exe
  ├── manage.py
  ├── requirements.txt
  ├── ... (todo el proyecto)
```

Así tus usuarios:
1. Ejecutan `INSTALAR.bat`
2. Ejecutan `launcher.exe`
3. ¡Listo!

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **"Python no está instalado"**

- Descarga e instala Python desde https://www.python.org/
- **IMPORTANTE**: Marca "Add Python to PATH"

### **"Error de base de datos"**

1. Verifica que MySQL esté corriendo
2. Abre: http://localhost/phpmyadmin
3. Verifica usuario: `root`, contraseña: `Contra.12`

### **"El navegador no abre"**

- Abre manualmente: **http://127.0.0.1:8000/**
- Si no carga, espera 5 segundos más

### **El sistema es lento la primera vez**

- Normal, está generando archivos de caché
- Espera 1-2 minutos

---

## 📱 CREAR ACCESO RÁPIDO EN ESCRITORIO

### **Para Windows:**

1. Haz click derecho en el escritorio
2. Selecciona "Nuevo" → "Acceso directo"
3. Escribe la ruta completa: `C:\ruta\del\proyecto\EJECUTAR.bat`
4. Click siguiente
5. Nombre: "Iniciar FlotaGest"
6. Finalizar

Ahora tienes un acceso directo en el escritorio para ejecutar el sistema.

---

## 🚀 PARA USUARIOS FINALES

**Resumen en 3 pasos:**

1. **Primer uso**: Ejecuta `INSTALAR.bat` una sola vez
2. **Cada vez que quieras usar**: Ejecuta `EJECUTAR.bat`
3. **En tu navegador**: Ve a http://127.0.0.1:8000/

---

## 📞 SOPORTE

Si hay problemas:

1. Verifica que MySQL esté corriendo
2. Intenta reiniciar la computadora
3. Ejecuta nuevamente `INSTALAR.bat`
4. Abre el archivo `.env` y verifica las credenciales de MySQL

---

**¡Listo! Tu sistema está preparado para usuarios sin conocimientos técnicos!** 🎉
