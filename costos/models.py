from django.db import models
from viajes.models import Viaje
from core.validators import validate_comprobante_file


class CostosViaje(models.Model):
    """
    Modelo para registrar y calcular costos de cada viaje.
    """
    viaje = models.OneToOneField(Viaje, on_delete=models.CASCADE, related_name='costos')
    km_inicial = models.IntegerField(null=True, blank=True, help_text='Kilometraje inicial real del viaje')
    km_final = models.IntegerField(null=True, blank=True, help_text='Kilometraje final real del viaje')
    combustible = models.IntegerField(default=0, help_text='Costo en pesos')
    mantenimientos = models.ManyToManyField('flota.Mantenimiento', blank=True, related_name='costos_viaje')
    mantenimiento = models.IntegerField(default=0, help_text='Costo total de mantenimientos seleccionados en pesos')
    peajes = models.IntegerField(default=0, help_text='Costo en pesos')
    otros_costos = models.IntegerField(default=0, help_text='Costo en pesos')
    costo_total = models.IntegerField(editable=False, default=0, help_text='Costo total en pesos')
    ganancia_neta = models.IntegerField(null=True, blank=True, help_text='Ganancia neta en pesos')
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Costo Viaje'
        verbose_name_plural = 'Costos Viajes'

    def calcular_costo_combustible(self):
        """Calcula el costo total de combustible sumando todos los puntos de recarga."""
        total = sum(punto.costo_total for punto in self.puntos_recarga.all())
        self.combustible = total
        return total

    def save(self, *args, **kwargs):
        # Calcular el costo total de los mantenimientos seleccionados
        if self.pk:
            self.mantenimiento = sum(int(m.costo) for m in self.mantenimientos.all())
        # Sumar todos los valores (ya son enteros)
        self.costo_total = int(self.combustible) + int(self.mantenimiento) + int(self.peajes) + int(self.otros_costos)
        
        # Cambiar automáticamente el estado del viaje a COMPLETADO
        if self.viaje.estado != 'completado':
            self.viaje.estado = 'completado'
            self.viaje.save()
        
        # Si el viaje tiene un viaje relacionado (ida-vuelta), marcarlo como completado también
        if self.viaje.viaje_relacionado and self.viaje.viaje_relacionado.estado != 'completado':
            self.viaje.viaje_relacionado.estado = 'completado'
            self.viaje.viaje_relacionado.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Costos - {self.viaje.bus.placa} ({self.viaje.fecha_salida.date()})"


class PuntoRecarga(models.Model):
    """
    Modelo para registrar cada punto de recarga de combustible en un viaje.
    """
    costos_viaje = models.ForeignKey(CostosViaje, on_delete=models.CASCADE, related_name='puntos_recarga')
    orden = models.IntegerField(help_text='Orden del punto de recarga en el viaje')
    kilometraje = models.IntegerField(help_text='Kilometraje al llegar a este punto')
    precio_combustible = models.IntegerField(help_text='Precio por litro/galón de combustible en pesos')
    litros_cargados = models.IntegerField(help_text='Litros de combustible cargados')
    kilometros_recorridos = models.IntegerField(editable=False, default=0, help_text='Kilómetros desde el punto anterior')
    costo_total = models.IntegerField(editable=False, default=0, help_text='Costo total de esta recarga en pesos')
    ubicacion = models.CharField(max_length=200, blank=True, help_text='Nombre o ubicación del punto de recarga')
    comprobante = models.FileField(
        upload_to='combustible/comprobantes/', 
        blank=True, 
        null=True, 
        validators=[validate_comprobante_file],
        help_text='Comprobante de recarga'
    )
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Punto de Recarga'
        verbose_name_plural = 'Puntos de Recarga'

    def save(self, *args, **kwargs):
        # Calcular costo total de esta recarga
        self.costo_total = self.litros_cargados * self.precio_combustible

        # Calcular kilómetros recorridos desde el punto anterior
        if self.orden == 1:
            # Primer punto: calcular desde el kilometraje inicial REAL del viaje
            if self.costos_viaje.km_inicial is not None:
                self.kilometros_recorridos = self.kilometraje - self.costos_viaje.km_inicial
            else:
                # Si no hay km_inicial registrado, no podemos calcular kilómetros recorridos
                self.kilometros_recorridos = 0
        else:
            # Puntos posteriores: calcular desde el punto anterior
            punto_anterior = PuntoRecarga.objects.filter(
                costos_viaje=self.costos_viaje,
                orden__lt=self.orden
            ).order_by('-orden').first()
            if punto_anterior:
                self.kilometros_recorridos = self.kilometraje - punto_anterior.kilometraje
            else:
                self.kilometros_recorridos = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Punto {self.orden} - {self.ubicacion} (Km: {self.kilometraje})"


class Peaje(models.Model):
    """
    Modelo para registrar peajes pagados en viajes.
    """
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='peajes')
    costos_viaje = models.ForeignKey('CostosViaje', on_delete=models.CASCADE, related_name='peajes_costos', null=True, blank=True)
    lugar = models.CharField(max_length=150)
    monto = models.IntegerField(help_text='Monto del peaje en pesos')
    fecha_pago = models.DateTimeField()
    comprobante = models.FileField(
        upload_to='peajes/vouchers/', 
        blank=True, 
        null=True,
        validators=[validate_comprobante_file]
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Peaje'
        verbose_name_plural = 'Peajes'

    def __str__(self):
        return f"Peaje en {self.lugar} - ${self.monto}"
