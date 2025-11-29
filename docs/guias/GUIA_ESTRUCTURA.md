# 🏗️ Guía de la Nueva Estructura de Navegación

## 📋 Descripción General

El proyecto **proyecto_buses** utiliza una arquitectura moderna basada en **sidebar lateral** en lugar de tabs horizontales. Esta estructura proporciona mejor UX y es más escalable.

## 🎨 Componentes Principales

### Sidebar (Lateral Izquierdo)
- **Navegación vertical fija**
- **Menú dinámico según rol**
- **Ancho: 280px (configurable)**
- **Scroll interno si es necesario**
- **Responsive: colapsa en móvil**

### Top Navbar (Barra Superior)
- **Título dinámico según página actual**
- **Usuario logueado + rol**
- **Botón logout**
- **Información del sistema**

### Main Content Area (Contenido Principal)
- **Área flexible para contenido**
- **Usa espacio restante del sidebar**
- **100% responsive**
- **Padding consistente**

## 🗺️ Estructura de Menú

```
FlotaGest (Logo)
├─ 🏠 Inicio
│
├─ OPERACIONES (Solo Admin)
│  ├─ 🚌 Buses
│  └─ 👨‍✈️ Conductores
│
└─ GESTIÓN (Todos)
   ├─ 🛣️ Viajes
   ├─ 📍 Lugares
   └─ 👥 Pasajeros
```

## 📱 Responsive Design

### Desktop (≥ 768px)
- ✅ Sidebar siempre visible
- ✅ Ancho fijo en 280px
- ✅ Contenido usa espacio restante

### Mobile (< 768px)
- ✅ Sidebar oculto por defecto
- ✅ Toggle button (hamburguesa)
- ✅ Desliza desde la izquierda
- ✅ Contenido ocupa todo el ancho

## 🎯 Características Principales

### 1. Navegación Intuitiva
- Menú claramente organizado
- Iconos Font Awesome
- Estados activos resaltados
- Enlaces siempre accesibles

### 2. Dinámico
- Menú cambia según rol del usuario
- Título del navbar actualiza automáticamente
- Mostrador de usuario en navbar
- Menú colapsable en móvil

### 3. Estilos
- Gradiente profesional
- Hover effects
- Transiciones suaves
- Colores coherentes

### 4. Accesibilidad
- Navegación clara
- Labels descriptivos
- Iconos informativos
- Responsive completo

## 🔗 URLs y Rutas

| Icono | Sección | URL | Protección |
|-------|---------|-----|-----------|
| 🏠 | Inicio | `/` | `@login_required` |
| 🚌 | Buses | `/flota/buses/` | `@admin_required` |
| 👨‍✈️ | Conductores | `/core/conductores/` | `@admin_required` |
| 🛣️ | Viajes | `/viajes/` | `@usuario_or_admin_required` |
| 📍 | Lugares | `/core/lugares/` | `@usuario_or_admin_required` |
| 👥 | Pasajeros | `/core/pasajeros/` | `@usuario_or_admin_required` |

## 🎨 CSS Variables

```css
:root {
    --sidebar-width: 280px;
    --primary-color: #1e40af;
    --primary-dark: #1e3a8a;
    --secondary-color: #3b82f6;
    /* ... más variables */
}
```

## 📐 Espaciado y Layout

### Estructura HTML
```html
<body>
    <nav class="sidebar">
        <!-- Menú lateral -->
    </nav>
    
    <div class="main-wrapper">
        <nav class="navbar-top">
            <!-- Navbar superior -->
        </nav>
        
        <main class="main-content">
            <!-- Contenido principal -->
        </main>
    </div>
</body>
```

### Cálculo de Ancho
```css
.main-wrapper {
    margin-left: var(--sidebar-width);
    width: calc(100% - var(--sidebar-width));
}

@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        transform: translateX(-100%);
    }
    
    .main-wrapper {
        margin-left: 0;
        width: 100%;
    }
}
```

## 🔄 Lógica de Estados Activos

El sidebar resalta el elemento activo según la URL actual:

```django
{% if 'bus' in request.resolver_match.url_name %}
    <li class="nav-item active">...</li>
{% endif %}
```

## 🚀 Ventajas de esta Estructura

| Aspecto | Ventaja |
|---------|---------|
| **UX** | Navegación clara y siempre accesible |
| **Mobile** | Mejor adaptación a pantallas pequeñas |
| **Escalabilidad** | Fácil agregar nuevas secciones |
| **Professional** | Aspecto moderno y profesional |
| **Performance** | Sin impacto en rendimiento |

## 🎯 Próximas Mejoras Sugeridas

- [ ] Toggle sidebar colapsable
- [ ] Search bar en navbar
- [ ] Submenu expandible
- [ ] Breadcrumbs
- [ ] Notificaciones
- [ ] Dark mode
- [ ] Historial de navegación

---

**Versión**: 2.0.0  
**Última actualización**: Noviembre 2025
