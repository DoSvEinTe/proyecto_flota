# 🎨 Guía de Estilos - Sistema de Gestión de Flota

## Mejoras Visuales Implementadas

Este documento describe las mejoras de personalización y diseño visual implementadas en el proyecto.

---

## 📋 Tabla de Contenidos

1. [Paleta de Colores](#paleta-de-colores)
2. [Tipografía](#tipografía)
3. [Componentes](#componentes)
4. [Estructura Visual](#estructura-visual)
5. [Cómo Usar los Estilos](#cómo-usar-los-estilos)

---

## 🎨 Paleta de Colores

La siguiente paleta de colores ha sido definida como variables CSS en la raíz del proyecto:

| Color | Código | Uso |
|-------|--------|-----|
| **Primario** | `#1e40af` | Botones principales, encabezados |
| **Secundario** | `#0d47a1` | Gradientes, énfasis |
| **Éxito** | `#10b981` | Operaciones exitosas, alertas positivas |
| **Peligro** | `#ef4444` | Eliminación, alertas de error |
| **Advertencia** | `#f59e0b` | Acciones de edición, advertencias |
| **Información** | `#06b6d4` | Detalles, información adicional |
| **Acento** | `#fbbf24` | Destacar, énfasis especial |

### Variables CSS Disponibles

```css
:root {
    --primary-color: #1e40af;
    --secondary-color: #0d47a1;
    --accent-color: #fbbf24;
    --success-color: #10b981;
    --danger-color: #ef4444;
    --warning-color: #f59e0b;
    --info-color: #06b6d4;
    --light-bg: #f8fafc;
    --card-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 🔤 Tipografía

### Fuente Principal
- **Familia**: Poppins (Google Fonts)
- **Pesos**: 300, 400, 500, 600, 700
- **Fallback**: Sistema sans-serif predeterminado

### Escala de Tamaños
- **H1**: 2.5rem (Títulos principales)
- **H2**: 2rem (Subtítulos)
- **H3**: 1.5rem (Secciones)
- **H4**: 1.25rem (Subsecciones)
- **Body**: 1rem (Texto regular)
- **Small**: 0.875rem (Texto pequeño)

---

## 🧩 Componentes Personalizados

### 1. Navbar (Barra de Navegación)
```html
<nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-main">
        <span class="navbar-brand">
            <i class="fas fa-bus"></i>
            <span>FlotaGest</span>
        </span>
    </div>
</nav>
```
- **Estilo**: Gradiente azul profesional
- **Características**: Logo, estado del sistema

### 2. Tarjetas de Estadísticas
```html
<div class="card stat-card card-primary">
    <div class="stat-card-body">
        <div class="stat-info">
            <h5>Total Buses</h5>
            <h2>{{ total }}</h2>
        </div>
        <div class="stat-icon">
            <i class="fas fa-bus"></i>
        </div>
    </div>
</div>
```
- **Clases**: `stat-card`, `card-primary/success/info/warning`
- **Efectos**: Hover con elevación y sombra
- **Animación**: Transición suave de 0.3s

### 3. Botones

#### Botón Primario
```html
<a href="#" class="btn btn-primary">
    <i class="fas fa-plus-circle"></i>
    Crear
</a>
```

#### Botones de Acción
```html
<!-- Editar -->
<a href="#" class="btn btn-sm btn-action btn-edit">
    <i class="fas fa-edit"></i>
</a>

<!-- Eliminar -->
<a href="#" class="btn btn-sm btn-action btn-delete">
    <i class="fas fa-trash-alt"></i>
</a>

<!-- Detalles -->
<a href="#" class="btn btn-sm btn-action btn-details">
    <i class="fas fa-eye"></i>
</a>
```

**Estilos de Botones Disponibles:**
- `btn-primary`: Azul gradiente
- `btn-success`: Verde gradiente
- `btn-danger`: Rojo gradiente
- `btn-warning`: Naranja gradiente
- `btn-info`: Turquesa gradiente
- `btn-outline-primary`: Contorno azul

### 4. Tablas

```html
<div class="card">
    <div class="table-responsive">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Columna 1</th>
                    <th>Columna 2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Dato 1</td>
                    <td>Dato 2</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
```

**Características:**
- Encabezados con gradiente
- Hover effect en filas
- Responsive y con sombra

### 5. Formularios

```html
<div class="form-group">
    <label for="nombre" class="form-label">Nombre</label>
    <input type="text" class="form-control" id="nombre" placeholder="Ingrese el nombre">
</div>
```

**Estilos:**
- Bordes suaves de 2px
- Focus con color primario y sombra
- Placeholder en gris suave
- Transiciones suaves

### 6. Alertas

```html
<div class="alert alert-success">
    ¡Operación realizada exitosamente!
</div>
```

**Tipos disponibles:**
- `alert-success`: Fondo verde claro
- `alert-danger`: Fondo rojo claro
- `alert-warning`: Fondo naranja claro
- `alert-info`: Fondo azul claro

### 7. Badges

```html
<span class="badge badge-success">Activo</span>
```

**Tipos:**
- `badge-primary`
- `badge-success`
- `badge-danger`
- `badge-warning`
- `badge-info`

### 8. Footer

```html
<footer class="footer-custom">
    <p><strong>Sistema de Gestión de Flota</strong> © 2025</p>
    <small>Desarrollado con <i class="fas fa-heart"></i> para eficiencia</small>
</footer>
```

---

## 📐 Estructura Visual

### Espaciado Estándar
- **Margen/Padding normal**: 1rem (16px)
- **Margen/Padding grande**: 2rem (32px)
- **Margen/Padding pequeño**: 0.5rem (8px)
- **Brecha entre elementos**: gap: 0.75rem

### Border Radius
- **Estándar**: 8px (botones, inputs, cards)
- **Grande**: 12px (tarjetas principales)
- **Redondo**: 20px (badges)

### Sombras
```css
--card-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
--hover-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
```

### Transiciones
```css
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 🚀 Cómo Usar los Estilos

### 1. Incluir el CSS en Base Template
```html
{% load static %}
<link href="{% static 'css/custom_styles.css' %}" rel="stylesheet">
```

### 2. Usar Variables CSS
```css
.mi-elemento {
    color: var(--primary-color);
    transition: var(--transition);
}
```

### 3. Gradientes
Para botones y encabezados:
```css
background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
```

### 4. Clases de Utilidad

#### Texto
- `.text-primary`: Color primario
- `.text-success`: Color de éxito
- `.text-danger`: Color de peligro
- `.text-warning`: Color de advertencia

#### Fondo
- `.bg-light-primary`: Fondo azul claro
- `.bg-light-success`: Fondo verde claro
- `.bg-light-danger`: Fondo rojo claro

#### Bordes
- `.border-primary`: Borde izquierdo azul de 4px

### 5. Efectos de Hover

Los botones y tarjetas tienen efectos de hover incorporados:

```css
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.btn:hover {
    transform: translateY(-2px);
}
```

---

## 📱 Responsive Design

El proyecto es completamente responsive con breakpoints Bootstrap:

- **Extra Small**: < 576px
- **Small**: ≥ 576px
- **Medium**: ≥ 768px
- **Large**: ≥ 992px
- **Extra Large**: ≥ 1200px

### Grid System
Usa clases de Bootstrap:
```html
<div class="row">
    <div class="col-md-6 col-lg-3">...</div>
    <div class="col-md-6 col-lg-3">...</div>
</div>
```

---

## 📦 Archivos de Estilos

- **`static/css/custom_styles.css`**: Estilos personalizados globales
- **`templates/base.html`**: Template base con navbar y footer

---

## 🎯 Mejoras Implementadas

✅ **Navbar personalizada** con gradiente y logo  
✅ **Footer personalizado** con información  
✅ **Tarjetas de estadísticas** con efectos hover  
✅ **Botones con gradientes** y transiciones suaves  
✅ **Tablas mejoradas** con estilos profesionales  
✅ **Formularios con enfoque visual**  
✅ **Iconos Font Awesome** integrados  
✅ **Animaciones suaves** en todo el proyecto  
✅ **Paleta de colores coherente**  
✅ **Tipografía profesional** (Poppins)

---

## 💡 Consejos para Mantener la Consistencia

1. **Siempre usa las variables CSS** en lugar de colores hardcodeados
2. **Mantén el espaciado consistente** usando las medidas estándar
3. **Aplica las transiciones** a elementos interactivos
4. **Usa los efectos hover** para mejorar la experiencia del usuario
5. **Respeta la paleta de colores** para mantener la identidad visual

---

## 📞 Soporte

Para preguntas sobre los estilos o para agregar nuevos componentes, consulta la paleta de colores y las variables CSS definidas.

**Última actualización**: 22 de noviembre de 2025
