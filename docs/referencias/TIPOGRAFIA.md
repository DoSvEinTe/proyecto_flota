# 🔤 Tipografía - Sistema de Gestión de Flota

## Familia de Fuentes

### Fuente Principal: Poppins
- **Proveedor**: Google Fonts
- **Pesos disponibles**: 300, 400, 500, 600, 700
- **Uso**: Toda la aplicación
- **Fallback**: `sans-serif`

### Cómo está importada
```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
}
```

---

## Escala de Tamaños

### Encabezados

| Elemento | Tamaño | Peso | Uso |
|----------|--------|------|-----|
| **H1** | 2.5rem (40px) | 700 Bold | Títulos principales de página |
| **H2** | 2rem (32px) | 700 Bold | Subtítulos principales |
| **H3** | 1.5rem (24px) | 600 SemiBold | Títulos de secciones |
| **H4** | 1.25rem (20px) | 600 SemiBold | Subtítulos de secciones |
| **H5** | 1.125rem (18px) | 600 SemiBold | Títulos de cards |
| **H6** | 1rem (16px) | 600 SemiBold | Títulos pequeños |

### Texto

| Elemento | Tamaño | Peso | Uso |
|----------|--------|------|-----|
| **Body** | 1rem (16px) | 400 Regular | Texto principal |
| **Lead** | 1.25rem (20px) | 400 Regular | Texto de introducción |
| **Small** | 0.875rem (14px) | 400 Regular | Texto pequeño |
| **Smaller** | 0.75rem (12px) | 400 Regular | Etiquetas, badges |

### Énfasis

| Elemento | Peso | Tamaño | Uso |
|----------|------|--------|-----|
| **Bold** | 700 | 1rem | Énfasis fuerte |
| **SemiBold** | 600 | 1rem | Énfasis moderado |
| **Light** | 300 | 1rem | Texto secundario |

---

## Línea Base y Espaciado

### Line Height (Altura de Línea)
```css
body {
    line-height: 1.6;  /* 1.6x el tamaño de la fuente */
}

h1, h2, h3, h4, h5, h6 {
    line-height: 1.2;  /* Encabezados más apretados */
}
```

### Letter Spacing (Espaciado entre letras)
```css
h1, h2, h3 {
    letter-spacing: -0.02em;  /* Ligeramente más apretado */
}

.uppercase {
    letter-spacing: 0.05em;   /* Más espaciado */
}
```

---

## Ejemplos de Uso

### En HTML
```html
<h1>Título Principal</h1>
<h2>Subtítulo</h2>
<p>Texto normal del cuerpo</p>
<small>Texto pequeño</small>
<strong>Texto en negrita</strong>
<em>Texto en cursiva</em>
```

### En CSS
```css
.titulo-principal {
    font-size: 2.5rem;
    font-weight: 700;
    font-family: 'Poppins', sans-serif;
    line-height: 1.2;
    margin-bottom: 1.5rem;
}

.texto-normal {
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.6;
}

.texto-pequeno {
    font-size: 0.875rem;
    font-weight: 500;
    color: #9ca3af;
}
```

### En Django Templates
```django
<h1 class="titulo-principal">{{ page_title }}</h1>
<p class="texto-normal">{{ description }}</p>
<span class="texto-pequeno">{{ additional_info }}</span>
```

---

## Combos Tipográficos Recomendados

### Para Títulos
```css
h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
}
```

### Para Cuerpo de Texto
```css
p, li, span {
    font-family: 'Poppins', sans-serif;
    font-weight: 400;
    line-height: 1.6;
    font-size: 1rem;
}
```

### Para Botones
```css
.btn {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
```

### Para Labels
```css
label {
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
```

---

## Jerarquía Tipográfica

La jerarquía visual se logra mediante:

1. **Tamaño**: H1 > H2 > H3 > Body > Small
2. **Peso**: 700 Bold > 600 SemiBold > 500 Medium > 400 Regular > 300 Light
3. **Color**: Primary > Secondary > Tertiary (Grays)
4. **Espaciado**: Mayor espaciado = Mayor importancia

---

## Responsive Tipografía

### En Desktop
```css
h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
p { font-size: 1rem; }
```

### En Tablet
```css
@media (max-width: 768px) {
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    p { font-size: 0.95rem; }
}
```

### En Mobile
```css
@media (max-width: 576px) {
    h1 { font-size: 1.75rem; }
    h2 { font-size: 1.25rem; }
    p { font-size: 0.9rem; }
}
```

---

## Monoespaciada (Código)

Para bloques de código y ejemplos, usa monoespaciada:

```html
<code>python manage.py runserver</code>
<pre><code>def hello():
    print("Hello, World!")
</code></pre>
```

```css
code, pre {
    font-family: 'Courier New', 'Courier', monospace;
    font-size: 0.875rem;
    background-color: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}
```

---

## Utilidades Tipográficas

### Clases Helper
```css
.font-bold { font-weight: 700; }
.font-semibold { font-weight: 600; }
.font-medium { font-weight: 500; }
.font-normal { font-weight: 400; }
.font-light { font-weight: 300; }

.text-uppercase { text-transform: uppercase; }
.text-lowercase { text-transform: lowercase; }
.text-capitalize { text-transform: capitalize; }

.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }
```

---

## Performance y Optimización

### Google Fonts Optimizado
```html
<!-- Preconectar para mejor rendimiento -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Cargar solo los pesos necesarios -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Font Display Strategy
- **display=swap**: Mejor visibilidad de contenido durante carga

---

## Accesibilidad Tipográfica

✅ **Contraste**: Mínimo 4.5:1 para texto normal  
✅ **Tamaño**: Mínimo 16px en móvil, 14px en desktop  
✅ **Line Height**: Mínimo 1.5 en párrafos  
✅ **Letter Spacing**: Máximo -0.02em en negativos  
✅ **Ligadura de Líneas**: Ancho máximo 80 caracteres  

---

## Validación de Tipografía

Puedes validar:
- [WebAIM](https://webaim.org/) - Herramientas de accesibilidad
- [Google Fonts](https://fonts.google.com/) - Información de fuentes
- [Typography.com](https://www.typography.com/) - Recursos tipográficos

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
