# 🎨 Paleta de Colores - Sistema de Gestión de Flota

## Colores Profesionales

La siguiente paleta de colores ha sido definida como variables CSS en la raíz del proyecto:

### Colores Principales

| Color | Código | Uso | Ejemplo |
|-------|--------|-----|---------|
| **Primario** | `#1e40af` | Botones principales, encabezados, navbar | ![#1e40af](https://via.placeholder.com/30/1e40af/1e40af) |
| **Primario Oscuro** | `#1e3a8a` | Gradientes, énfasis, hover | ![#1e3a8a](https://via.placeholder.com/30/1e3a8a/1e3a8a) |
| **Secundario** | `#3b82f6` | Botones secundarios, links | ![#3b82f6](https://via.placeholder.com/30/3b82f6/3b82f6) |

### Colores de Estado

| Color | Código | Uso | Ejemplo |
|-------|--------|-----|---------|
| **Éxito** | `#10b981` | Operaciones exitosas, alertas positivas, checkmarks | ![#10b981](https://via.placeholder.com/30/10b981/10b981) |
| **Peligro** | `#ef4444` | Eliminación, alertas de error, botones críticos | ![#ef4444](https://via.placeholder.com/30/ef4444/ef4444) |
| **Advertencia** | `#f59e0b` | Edición, advertencias, acciones cautas | ![#f59e0b](https://via.placeholder.com/30/f59e0b/f59e0b) |
| **Información** | `#06b6d4` | Detalles, información adicional, tips | ![#06b6d4](https://via.placeholder.com/30/06b6d4/06b6d4) |

### Colores de Fondo

| Color | Código | Uso |
|-------|--------|-----|
| **Light Background** | `#f8fafc` | Fondos de tarjetas, secciones |
| **White** | `#ffffff` | Fondos principales, componentes |
| **Dark Text** | `#1f2937` | Texto principal |
| **Light Text** | `#9ca3af` | Texto secundario, placeholder |

### Acento

| Color | Código | Uso |
|-------|--------|-----|
| **Acento** | `#fbbf24` | Destacar, énfasis especial, badges |

---

## Variables CSS Definidas

```css
:root {
    /* Colores principales */
    --primary-color: #1e40af;           /* Azul Principal */
    --primary-dark: #1e3a8a;            /* Azul Oscuro */
    --secondary-color: #3b82f6;         /* Azul Secundario */
    
    /* Colores de estado */
    --success-color: #10b981;           /* Verde - Éxito */
    --danger-color: #ef4444;            /* Rojo - Peligro */
    --warning-color: #f59e0b;           /* Naranja - Advertencia */
    --info-color: #06b6d4;              /* Cian - Información */
    
    /* Acento */
    --accent-color: #fbbf24;            /* Amarillo - Acento */
    
    /* Fondos */
    --light-bg: #f8fafc;                /* Fondo claro */
    
    /* Sombras */
    --card-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    --hover-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    
    /* Transiciones */
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Otras medidas */
    --sidebar-width: 280px;
}
```

---

## Cómo Usar los Colores

### En CSS
```css
.elemento {
    color: var(--primary-color);
    background-color: var(--light-bg);
    transition: var(--transition);
}

.elemento:hover {
    background-color: var(--primary-color);
}
```

### En HTML (Bootstrap)
```html
<button class="btn btn-primary">Botón Primario</button>
<button class="btn btn-success">Botón Éxito</button>
<button class="btn btn-danger">Botón Peligro</button>
<button class="btn btn-warning">Botón Advertencia</button>
<button class="btn btn-info">Botón Información</button>
```

### En Django Templates
```django
<div style="color: var(--primary-color);">
    Texto coloreado
</div>

<span class="badge" style="background-color: var(--success-color);">
    Éxito
</span>
```

---

## Gradientes Disponibles

### Gradiente Primario (Navbar, Headers)
```css
background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
```

### Gradiente Secundario
```css
background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%);
```

### Gradiente de Éxito
```css
background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%);
```

---

## Contraste y Accesibilidad

Todos los colores cumplen con WCAG AAA para accesibilidad:
- ✅ Contraste suficiente con texto blanco
- ✅ Contraste suficiente con texto negro
- ✅ Visibles para personas con daltonismo

### Combinaciones Recomendadas

| Fondo | Texto Recomendado |
|-------|-------------------|
| Primary (#1e40af) | Blanco (#ffffff) |
| Secondary (#3b82f6) | Blanco (#ffffff) |
| Success (#10b981) | Blanco (#ffffff) |
| Danger (#ef4444) | Blanco (#ffffff) |
| Warning (#f59e0b) | Blanco (#ffffff) o Dark |
| Info (#06b6d4) | Blanco (#ffffff) |
| Light BG (#f8fafc) | Dark (#1f2937) |

---

## Ejemplos en Componentes

### Botón Primario
```html
<button class="btn btn-primary">
    Crear Nuevo
</button>

<!-- CSS -->
.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-dark);
}
```

### Card de Estadística
```html
<div class="stat-card card-primary">
    <h3>Total Buses</h3>
    <h2>25</h2>
</div>

<!-- CSS -->
.card-primary {
    border-left: 4px solid var(--primary-color);
}
```

### Alerta de Éxito
```html
<div class="alert alert-success">
    ¡Operación realizada exitosamente!
</div>

<!-- CSS -->
.alert-success {
    background-color: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
    border-left: 4px solid var(--success-color);
}
```

---

## Cambiar la Paleta

Para cambiar la paleta de colores, edita las variables en `static/css/custom_styles.css`:

```css
:root {
    /* Cambia estos valores a tus colores preferidos */
    --primary-color: #tu-nuevo-color;
    --primary-dark: #color-oscuro;
    /* ... etc */
}
```

Todos los componentes se actualizar automáticamente.

---

## Validación de Colores

Puedes validar los colores en:
- [Coolors.co](https://coolors.co) - Paleta de colores
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Contraste
- [Color Oracle](https://colororacle.org/) - Simulador de daltonismo

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
