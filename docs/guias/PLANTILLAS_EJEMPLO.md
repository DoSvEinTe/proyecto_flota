# 📋 Plantillas de Ejemplo - Sistema de Gestión de Flota

Estos son ejemplos de cómo estructurar nuevas páginas usando los estilos personalizados.

---

## 1️⃣ Plantilla para Página de Lista

Copia esta estructura para crear nuevas vistas de listado:

```html
{% extends 'base.html' %}

{% block title %}Mi Lista - Sistema de Gestión de Flota{% endblock %}

{% block extra_css %}
<style>
    .page-header {
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .page-header h1 {
        margin: 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
    }

    .empty-state i {
        color: #d1d5db;
        margin-bottom: 1rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="page-header">
    <h1>
        <i class="fas fa-list"></i>
        Mi Lista
    </h1>
    <a href="{% url 'crear_url' %}" class="btn btn-primary">
        <i class="fas fa-plus-circle"></i>
        Crear Nuevo
    </a>
</div>

{% if items %}
    <div class="card">
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th><i class="fas fa-tag me-2"></i>Campo 1</th>
                        <th>Campo 2</th>
                        <th>Campo 3</th>
                        <th style="width: 120px; text-align: center;">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in items %}
                    <tr>
                        <td><strong>{{ item.nombre }}</strong></td>
                        <td>{{ item.campo2 }}</td>
                        <td>{{ item.campo3 }}</td>
                        <td style="text-align: center;">
                            <a href="{% url 'actualizar' item.pk %}" class="btn btn-sm btn-action btn-edit">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="{% url 'eliminar' item.pk %}" class="btn btn-sm btn-action btn-delete">
                                <i class="fas fa-trash-alt"></i>
                            </a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
{% else %}
    <div class="card">
        <div class="empty-state">
            <i class="fas fa-inbox fa-4x"></i>
            <h4 class="text-muted mt-3 mb-2">No hay registros</h4>
            <p class="text-muted mb-4">Comienza creando tu primer registro</p>
            <a href="{% url 'crear_url' %}" class="btn btn-primary">
                <i class="fas fa-plus-circle"></i>
                Crear Primero
            </a>
        </div>
    </div>
{% endif %}
{% endblock %}
```

---

## 2️⃣ Plantilla para Página de Detalles

```html
{% extends 'base.html' %}

{% block title %}Detalles - Sistema de Gestión de Flota{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
            <h1>
                <i class="fas fa-eye"></i>
                Detalles de {{ objeto.nombre }}
            </h1>
            <div>
                <a href="{% url 'actualizar' objeto.pk %}" class="btn btn-warning me-2">
                    <i class="fas fa-edit"></i>
                    Editar
                </a>
                <a href="{% url 'lista_url' %}" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i>
                    Volver
                </a>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h5>Información General</h5>
            </div>
            <div class="card-body">
                <p>
                    <strong><i class="fas fa-user me-2"></i>Nombre:</strong>
                    {{ objeto.nombre }}
                </p>
                <p>
                    <strong><i class="fas fa-envelope me-2"></i>Email:</strong>
                    {{ objeto.email }}
                </p>
                <p>
                    <strong><i class="fas fa-phone me-2"></i>Teléfono:</strong>
                    {{ objeto.telefono }}
                </p>
                <p class="mb-0">
                    <strong><i class="fas fa-calendar me-2"></i>Creado:</strong>
                    {{ objeto.fecha_creacion|date:"d/m/Y" }}
                </p>
            </div>
        </div>
    </div>

    <div class="col-lg-4">
        <div class="card">
            <div class="card-header">
                <h5>Estado</h5>
            </div>
            <div class="card-body">
                {% if objeto.activo %}
                    <span class="badge badge-success">Activo</span>
                {% else %}
                    <span class="badge badge-danger">Inactivo</span>
                {% endif %}
            </div>
        </div>

        <div class="card mt-3">
            <div class="card-header">
                <h5>Acciones</h5>
            </div>
            <div class="card-body">
                <div class="d-grid gap-2">
                    <a href="{% url 'actualizar' objeto.pk %}" class="btn btn-warning">
                        <i class="fas fa-edit"></i>
                        Editar
                    </a>
                    <a href="{% url 'eliminar' objeto.pk %}" class="btn btn-danger">
                        <i class="fas fa-trash"></i>
                        Eliminar
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 3️⃣ Plantilla para Formulario

```html
{% extends 'base.html' %}

{% block title %}Formulario - Sistema de Gestión de Flota{% endblock %}

{% block extra_css %}
<style>
    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-label {
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.75rem;
    }

    .invalid-feedback {
        display: block;
        color: #ef4444;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8 offset-lg-2">
        <h1 class="mb-4">
            <i class="fas fa-form"></i>
            {% if form.instance.pk %}
                Editar
            {% else %}
                Crear Nuevo
            {% endif %}
        </h1>

        <div class="card">
            <div class="card-header">
                <h5>Información del Formulario</h5>
            </div>
            <div class="card-body">
                <form method="post" novalidate>
                    {% csrf_token %}

                    <!-- Mensajes de error generales -->
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger" role="alert">
                            <i class="fas fa-exclamation-circle me-2"></i>
                            <strong>Error:</strong>
                            {% for error in form.non_field_errors %}
                                <div>{{ error }}</div>
                            {% endfor %}
                        </div>
                    {% endif %}

                    <!-- Campos del formulario -->
                    {% for field in form %}
                        <div class="form-group">
                            {{ field.label_tag }}
                            
                            {% if field.widget.input_type == "checkbox" %}
                                <div class="form-check">
                                    {{ field }}
                                    <label class="form-check-label" for="{{ field.id_for_label }}">
                                        {{ field.label }}
                                    </label>
                                </div>
                            {% elif field.widget.input_type == "select" %}
                                {{ field }}
                            {% else %}
                                {{ field }}
                            {% endif %}

                            {% if field.errors %}
                                <div class="invalid-feedback" style="display: block;">
                                    {% for error in field.errors %}
                                        <i class="fas fa-times-circle me-2"></i>{{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}

                            {% if field.help_text %}
                                <small class="form-text text-muted">
                                    {{ field.help_text|safe }}
                                </small>
                            {% endif %}
                        </div>
                    {% endfor %}

                    <!-- Botones -->
                    <div class="d-flex gap-2 mt-4">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i>
                            {% if form.instance.pk %}Actualizar{% else %}Crear{% endif %}
                        </button>
                        <a href="{% url 'lista_url' %}" class="btn btn-secondary">
                            <i class="fas fa-times"></i>
                            Cancelar
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 4️⃣ Plantilla Dashboard con Múltiples Tarjetas

```html
{% extends 'base.html' %}

{% block title %}Dashboard - Sistema de Gestión de Flota{% endblock %}

{% block content %}
<div class="page-header mb-4">
    <h1>
        <i class="fas fa-chart-line"></i>
        Dashboard
    </h1>
    <p class="text-muted">Bienvenido al panel de control</p>
</div>

<!-- Fila de Estadísticas -->
<div class="row mb-4">
    <div class="col-md-6 col-lg-3 mb-4">
        <div class="card stat-card card-primary">
            <div class="stat-card-body">
                <div class="stat-info">
                    <h5>Total Items</h5>
                    <h2>{{ total_items }}</h2>
                </div>
                <div class="stat-icon">
                    <i class="fas fa-box"></i>
                </div>
            </div>
            <div class="stat-card-footer">
                <a href="{% url 'items_list' %}">
                    Ver todos <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>

    <div class="col-md-6 col-lg-3 mb-4">
        <div class="card stat-card card-success">
            <div class="stat-card-body">
                <div class="stat-info">
                    <h5>Completados</h5>
                    <h2>{{ completados }}</h2>
                </div>
                <div class="stat-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
            </div>
            <div class="stat-card-footer">
                <a href="{% url 'completados' %}">
                    Ver <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>

    <div class="col-md-6 col-lg-3 mb-4">
        <div class="card stat-card card-warning">
            <div class="stat-card-body">
                <div class="stat-info">
                    <h5>Pendientes</h5>
                    <h2>{{ pendientes }}</h2>
                </div>
                <div class="stat-icon">
                    <i class="fas fa-hourglass"></i>
                </div>
            </div>
            <div class="stat-card-footer">
                <a href="{% url 'pendientes' %}">
                    Ver <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>

    <div class="col-md-6 col-lg-3 mb-4">
        <div class="card stat-card card-info">
            <div class="stat-card-body">
                <div class="stat-info">
                    <h5>Recientes</h5>
                    <h2>{{ recientes }}</h2>
                </div>
                <div class="stat-icon">
                    <i class="fas fa-clock"></i>
                </div>
            </div>
            <div class="stat-card-footer">
                <a href="{% url 'items_list' %}">
                    Ver <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>
</div>

<!-- Fila de Contenido -->
<div class="row">
    <div class="col-lg-8">
        <!-- Última actividad o tabla -->
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-list me-2"></i>Últimos Items</h5>
            </div>
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in ultimos_items %}
                        <tr>
                            <td>{{ item.nombre }}</td>
                            <td>
                                {% if item.completado %}
                                    <span class="badge badge-success">Completado</span>
                                {% else %}
                                    <span class="badge badge-warning">Pendiente</span>
                                {% endif %}
                            </td>
                            <td>
                                <a href="{% url 'detalles' item.pk %}" class="btn btn-sm btn-action btn-details">
                                    <i class="fas fa-eye"></i>
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="col-lg-4">
        <!-- Acciones Rápidas -->
        <div class="card quick-actions mb-3">
            <div class="card-header">
                <h5><i class="fas fa-bolt me-2"></i>Acciones Rápidas</h5>
            </div>
            <div class="card-body">
                <div class="d-grid gap-2">
                    <a href="{% url 'crear' %}" class="btn btn-primary">
                        <i class="fas fa-plus-circle"></i>
                        Crear Nuevo
                    </a>
                    <a href="{% url 'reportes' %}" class="btn btn-info">
                        <i class="fas fa-chart-bar"></i>
                        Ver Reportes
                    </a>
                    <a href="{% url 'configuracion' %}" class="btn btn-secondary">
                        <i class="fas fa-cog"></i>
                        Configuración
                    </a>
                </div>
            </div>
        </div>

        <!-- Información -->
        <div class="card info-section">
            <div class="card-header">
                <h5><i class="fas fa-info-circle me-2"></i>Información</h5>
            </div>
            <div class="card-body">
                <p>Última actualización: <strong>{% now "d/m/Y H:i" %}</strong></p>
                <p>Estado: <span class="badge badge-success">Operativo</span></p>
                <p class="mb-0">Versión: <strong>2.0.0</strong></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 5️⃣ Plantilla para Error 404 Personalizado

```html
{% extends 'base.html' %}

{% block title %}Página no encontrada{% endblock %}

{% block content %}
<div class="text-center py-5">
    <h1 class="display-1">404</h1>
    <h2 class="mb-3">
        <i class="fas fa-exclamation-triangle"></i>
        Página no encontrada
    </h2>
    <p class="lead mb-4">La página que buscas no existe o ha sido eliminada.</p>
    
    <a href="{% url 'home' %}" class="btn btn-primary me-2">
        <i class="fas fa-home"></i>
        Ir a Inicio
    </a>
    <a href="javascript:history.back()" class="btn btn-secondary">
        <i class="fas fa-arrow-left"></i>
        Volver Atrás
    </a>
</div>
{% endblock %}
```

---

## 📝 Notas Importantes

1. **Reemplaza `{% url 'nombre_url' %}` con tus propias URLs**
2. **Usa los iconos de Font Awesome** disponibles
3. **Mantén la consistencia de clases** CSS
4. **Personaliza los colores** usando variables CSS si es necesario
5. **Prueba en diferentes tamaños** de pantalla (responsive)

---

## 🎨 Colores Disponibles para Tarjetas

- `card-primary` - Azul
- `card-success` - Verde
- `card-info` - Turquesa
- `card-warning` - Naranja
- `card-danger` - Rojo (si necesitas)

---

¡Usa estas plantillas como base para crear nuevas páginas en tu aplicación! 🚀
