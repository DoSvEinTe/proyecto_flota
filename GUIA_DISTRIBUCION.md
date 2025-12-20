# 📦 GUÍA DE DISTRIBUCIÓN - Sistema FlotaGest

## Para desarrolladores que necesitan distribuir el sistema

---

## 🎯 OPCIÓN 1: Distribución Simple (SIN compilación)

### Archivos necesarios para distribuir:

```
FlotaGest/
├── INSTALAR.bat          ← Ejecutar PRIMERO
├── EJECUTAR.bat          ← Ejecutar DESPUÉS
├── launcher.py
├── instalar.py
├── manage.py
├── requirements.txt
├── .env
├── verificar_sistema.py
├── GUIA_INSTALACION.md
├── INICIO_RAPIDO.txt
├── core/                 (todo el contenido)
├── costos/              (todo el contenido)
├── flota/               (todo el contenido)
├── viajes/              (todo el contenido)
├── templates/           (todo el contenido)
├── static/              (todo el contenido)
├── sistema_flota/       (todo el contenido)
└── ... (otros archivos)
```

### Pasos para el usuario final:

1. Descarga la carpeta completa
2. Abre `INSTALAR.bat` (espera 5-10 minutos)
3. Abre `EJECUTAR.bat` cada vez que quiera usar
4. Abre navegador en `http://127.0.0.1:8000/`

---

## 🚀 OPCIÓN 2: Distribución con EXE (MÁS PROFESIONAL)

### Ventaja: Usuario solo descarga y ejecuta

### Pasos:

1. En tu máquina, ejecuta:
   ```bash
   GENERAR_EXE.bat
   ```

2. Se creará una carpeta `dist/` con `FlotaGest.exe`

3. Copia a distribuir:
   ```
   FlotaGest/
   ├── dist/
   │   └── FlotaGest.exe          ← El ejecutable
   ├── INSTALAR.bat
   ├── manage.py
   ├── requirements.txt
   ├── ... (todo el proyecto)
   ```

### Instrucciones para usuario:

1. Descarga la carpeta
2. Doble click en `INSTALAR.bat`
3. Doble click en `dist/FlotaGest.exe`
4. Click en "Iniciar Sistema"
5. Abre navegador

---

## 🔒 SEGURIDAD ANTES DE DISTRIBUIR

### Verificar credenciales de producción:

```bash
# Ver contenido del .env
cat .env
```

**IMPORTANTE:** Cambia estas variables según el cliente:

```
SECRET_KEY=tu-secret-key-segura
DB_PASSWORD=contraseña-segura
EMAIL_HOST_PASSWORD=contraseña-aplicacion-gmail
```

### Generar SECRET_KEY segura:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 📝 CÓMO CREAR UN PAQUETE ZIP

### Con 7-Zip o WinRAR:

1. Click derecho en carpeta FlotaGest
2. "Enviar a" → "Carpeta comprimida"
3. Renombra a `FlotaGest_v1.0.zip`
4. ¡Listo para distribuir!

### Con PowerShell:

```powershell
# Abre PowerShell en la carpeta padre de FlotaGest
Compress-Archive -Path FlotaGest -DestinationPath FlotaGest_v1.0.zip
```

---

## ✅ LISTA DE VERIFICACIÓN ANTES DE DISTRIBUIR

- [ ] Archivo `.env` con credenciales correctas
- [ ] Base de datos MySQL creada y funcional
- [ ] Ejecutado `INSTALAR.bat` al menos una vez
- [ ] Verificado con `verificar_sistema.py`
- [ ] Probado en otra carpeta (simular usuario)
- [ ] Documentación actualizada (GUIA_INSTALACION.md)
- [ ] README.md claro para usuario final

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### "ModuleNotFoundError"

Ejecuta nuevamente `INSTALAR.bat`

### "MySQL no conecta"

Verifica en `.env`:
- Usuario: `root`
- Contraseña: `Contra.12`
- Host: `localhost`

### "Puerto 8000 en uso"

Cambia el puerto en launcher.py:
```python
# Busca: python manage.py runserver
# Reemplaza con: python manage.py runserver 8001
```

---

## 📊 ESTADÍSTICAS DE DISTRIBUCIÓN

**Tamaño sin EXE**: ~500 MB (incluye node_modules y caché)
**Tamaño con EXE**: ~700 MB

**Tiempo de instalación**:
- Primera vez: 5-10 minutos
- Siguientes: 10 segundos

---

## 🎁 BONUS: Crear icono personalizado

1. Crea un imagen PNG (256x256)
2. Convierte a ICO en: https://convertio.co/es/png-ico/
3. Guarda como `icon.ico` en la carpeta raíz
4. Modifica `GENERAR_EXE.bat`:
   ```bat
   pyinstaller --onefile --windowed --icon=icon.ico launcher.py
   ```

---

**¡Tu sistema está listo para distribuir!** 🎉
