# 🔐 GUÍA RÁPIDA - GESTIÓN DE CONTRASEÑAS

## 🎯 ¿QUÉ PUEDES HACER?

### USUARIO REGULAR

#### 1. Cambiar Mi Contraseña
1. En la esquina superior derecha, haz click en el **menú de usuario** (icono 👤)
2. Selecciona **"Cambiar Contraseña"**
3. Se abre formulario con 3 campos:
   - 🔐 **Contraseña Maestra**: Ingresa `admin123` (o la configurada)
   - 🔑 **Nueva Contraseña**: Ingresa tu nueva contraseña
   - ✓ **Confirmar Contraseña**: Repite la contraseña
4. Haz click en **"Cambiar Contraseña"**
5. ✅ Se desloguea automáticamente
6. Inicia sesión con tu **nueva contraseña**

#### 2. Mi Configuración
1. En el menú de usuario, selecciona **"Configuración"**
2. Puedes ver:
   - **Seguridad**: Acceso rápido a cambio de contraseña
   - **Mi Perfil**: Tu información de usuario
   - **Mi Cuenta**: Detalles de registro y estado

#### 3. Cerrar Sesión
- En el menú de usuario, selecciona **"Cerrar Sesión"**

---

### ADMINISTRADOR (ADEMÁS DE LO ANTERIOR)

#### 1. Gestionar Usuarios
1. En el menú de usuario, selecciona **"Gestionar Usuarios"**
2. Se abre tabla con TODOS los usuarios del sistema
3. Columnas disponibles:
   - 👤 Usuario
   - 📧 Email
   - 👥 Nombre Completo
   - 🛡️ Tipo (Admin/Usuario)
   - ⚙️ Acciones

#### 2. Cambiar Contraseña de Otro Usuario
1. En tabla de usuarios, busca al usuario
2. En columna **Acciones**, haz click en icono **🔑**
3. Se abre formulario para cambiar contraseña
4. Ingresa:
   - 🔑 **Nueva Contraseña**: Nueva contraseña del usuario
   - ✓ **Confirmar Contraseña**: Repite la contraseña
5. Haz click en **"Cambiar Contraseña"**
6. ✅ Contraseña cambiada exitosamente
7. El usuario debe usar la **nueva contraseña** en próximo login

#### 3. Editar Usuario en Django Admin
1. En tabla de usuarios, columna **Acciones**
2. Haz click en icono **✏️** para abrir editor de Django

---

## 📋 REQUISITOS DE CONTRASEÑA

La nueva contraseña DEBE cumplir:

✅ **Mínimo 8 caracteres**
```
❌ Débil:    pass123
✅ Correcto: MyPassword123!
```

✅ **Incluir MAYÚSCULAS**
```
❌ Débil:    mypassword123!
✅ Correcto: MyPassword123!
```

✅ **Incluir minúsculas**
```
❌ Débil:    MYPASSWORD123!
✅ Correcto: MyPassword123!
```

✅ **Incluir NÚMEROS**
```
❌ Débil:    MyPassword!
✅ Correcto: MyPassword123!
```

✅ **Incluir CARACTERES ESPECIALES**
```
❌ Débil:    MyPassword123
✅ Correcto: MyPassword123!
```

### Caracteres Especiales Válidos:
```
! @ # $ % ^ & * ( ) - _ = + [ ] { } ; : ' " , . < > ? / \ | `
```

### Ejemplos de Contraseñas Válidas:
```
✅ MiFlota2025!@#
✅ Sistemas123$abc
✅ Gestion*Flota99
✅ Admin#Seguro2025
✅ Password!123ABC
```

---

## 🔒 LA CONTRASEÑA MAESTRA

¿QUÉ ES?
- Una contraseña adicional que se requiere para cambiar tu propia contraseña
- Evita que alguien que acceda a tu PC pueda cambiar tu contraseña

¿CUÁL ES LA CONTRASEÑA MAESTRA?
- Por defecto: `admin123`
- Puede ser diferente según la configuración del administrador

¿DÓNDE SE USA?
- SOLO cuando un **usuario regular** cambia su propia contraseña
- Admin NO necesita ingresar contraseña maestra para cambiar la de otros

¿QUÉ PASA SI LA OLVIDO?
- Contacta al administrador del sistema
- El admin puede cambiarla en el archivo `.env`

---

## 🚨 ERRORES COMUNES

### "Las contraseñas no coinciden"
```
Causa: Escribiste diferente en "Nueva Contraseña" y "Confirmar"
Solución: Escribe exactamente igual en ambos campos
```

### "Contraseña maestra incorrecta"
```
Causa: Escribiste mal la contraseña maestra
Solución: Verifica que escribas: admin123 (sin espacios)
```

### "La contraseña es demasiado corta"
```
Causa: Tienes menos de 8 caracteres
Solución: Usa al menos 8 caracteres
```

### "La contraseña no contiene..."
```
Causa: Falta algún requisito (mayúscula, número, símbolo)
Solución: Agrega lo que falta (ej: si falta número, agrega 123)
```

### "Usuario o contraseña incorrectos al iniciar"
```
Causa: Escribiste mal la contraseña nueva al iniciar
Solución: Verifica que escribas exactamente igual
Recuerda: MAYÚSCULAS y minúsculas son DIFERENTES
```

---

## 💡 CONSEJOS DE SEGURIDAD

1. **No comparta su contraseña maestra**
   - Es como la contraseña del banco
   - Solo para ti

2. **Use contraseñas diferentes para cada cuenta**
   - No uses la misma contraseña en múltiples sitios
   - Si uno se compromete, los otros están seguros

3. **Cambie su contraseña regularmente**
   - Cada 3-6 meses es recomendable
   - Especialmente si sospecha que fue comprometida

4. **No use información personal**
   - Evita: fecha de nacimiento, nombre de familia, etc.
   - Usa combinaciones aleatorias

5. **Escriba correctamente**
   - MAYÚSCULAS son diferentes de minúsculas
   - MyPassword123! ≠ mypassword123!

---

## 🎯 FLUJO VISUAL

### Usuario Cambia Su Contraseña:
```
┌─ Menú Usuario (👤)
├─ Cambiar Contraseña
├─ Ingresa: Contraseña Maestra (admin123)
├─ Ingresa: Nueva Contraseña (MiPass123!)
├─ Confirma: Nueva Contraseña (MiPass123!)
├─ Click: "Cambiar Contraseña"
├─ ✅ Se desloguea
└─ Login con: Nueva Contraseña
```

### Admin Cambia Contraseña de Usuario:
```
┌─ Menú Usuario (👤)
├─ Gestionar Usuarios
├─ Busca: Usuario en tabla
├─ Click: Icono 🔑 (Cambiar)
├─ Ingresa: Nueva Contraseña (NewPass456!)
├─ Confirma: Nueva Contraseña (NewPass456!)
├─ Click: "Cambiar Contraseña"
├─ ✅ Vuelve a tabla
└─ Usuario: Debe usar nueva contraseña
```

---

## 📞 SOPORTE

### ¿Olvidé mi contraseña?
→ Pide al admin que la cambie desde "Gestionar Usuarios"

### ¿Olvidé la contraseña maestra?
→ Contacta al administrador de sistemas

### ¿La contraseña no me funciona al iniciar?
1. Verifica que escribas exactamente igual
2. Recuerda: MAYÚSCULAS son diferentes
3. Pide al admin que verifique

### ¿Necesito cambiar la contraseña maestra?
→ Solo el admin puede hacerlo en `.env`

---

## ✅ RESUMEN

**LO QUE NECESITAS RECORDAR:**

1. **Acceso**: Menú usuario (esquina superior derecha)
2. **Para cambiar TU contraseña**: Necesitas contraseña maestra
3. **Si eres ADMIN**: Puedes cambiar cualquier contraseña sin maestra
4. **Requisitos**: 8+ caracteres, mayúsculas, minúsculas, números, símbolos
5. **Después de cambiar**: Desloguea y login con nueva contraseña

---

**¡Sistema seguro y fácil de usar!** 🔐✅
