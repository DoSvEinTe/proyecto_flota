from django.db import models


class Conductor(models.Model):
    """
    Modelo para registrar conductores de la flota.
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    cedula_frontal = models.ImageField(upload_to='cedulas/', null=True, blank=True, help_text='Foto frontal de la cédula de identidad')
    cedula_trasera = models.ImageField(upload_to='cedulas/', null=True, blank=True, help_text='Foto trasera de la cédula de identidad')
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_contratacion = models.DateField()
    licencia_conducir_frontal = models.ImageField(upload_to='licencias/', null=True, blank=True, help_text='Foto frontal de la licencia de conducir')
    licencia_conducir_trasera = models.ImageField(upload_to='licencias/', null=True, blank=True, help_text='Foto trasera de la licencia de conducir')
    licencias = models.CharField(
        max_length=50,
        help_text='Tipos de licencias (A, B, C, etc.)',
        blank=True,
        default=''
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Lugar(models.Model):
    """
    Modelo para registrar lugares (origen, destino, paradas).
    """
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, default='Ecuador')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ciudad', 'nombre']
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'

    def __str__(self):
        return f"{self.nombre}, {self.ciudad}"


class Pasajero(models.Model):
    """
    Modelo para registrar pasajeros del sistema.
    """
    nombre_completo = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, null=True, blank=True, help_text='RUT para ciudadanos chilenos')
    pasaporte = models.CharField(max_length=20, null=True, blank=True, help_text='Pasaporte para extranjeros')
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre_completo']
        verbose_name = 'Pasajero'
        verbose_name_plural = 'Pasajeros'

    def __str__(self):
        return self.nombre_completo
