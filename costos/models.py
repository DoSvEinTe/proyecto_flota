from django.db import models
from viajes.models import Viaje


class CostosViaje(models.Model):
    """
    Modelo para registrar y calcular costos de cada viaje.
    """
    viaje = models.OneToOneField(Viaje, on_delete=models.CASCADE, related_name='costos')
    km_inicial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Kilometraje inicial real del viaje')
    km_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Kilometraje final real del viaje')
    combustible = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mantenimientos = models.ManyToManyField('flota.Mantenimiento', blank=True, related_name='costos_viaje')
    mantenimiento = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Costo total de mantenimientos seleccionados')
    peajes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    otros_costos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    ganancia_neta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
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
        from decimal import Decimal
        # Calcular el costo total de los mantenimientos seleccionados
        if self.pk:
            self.mantenimiento = sum(Decimal(m.costo) for m in self.mantenimientos.all())
        # Convertir todos los valores a Decimal antes de sumar
        combustible = Decimal(self.combustible)
        mantenimiento = Decimal(self.mantenimiento)
        peajes = Decimal(self.peajes)
        otros_costos = Decimal(self.otros_costos)
        self.costo_total = combustible + mantenimiento + peajes + otros_costos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Costos - {self.viaje.bus.placa} ({self.viaje.fecha_salida.date()})"


class PuntoRecarga(models.Model):
    """
    Modelo para registrar cada punto de recarga de combustible en un viaje.
    """
    costos_viaje = models.ForeignKey(CostosViaje, on_delete=models.CASCADE, related_name='puntos_recarga')
    orden = models.IntegerField(help_text='Orden del punto de recarga en el viaje')
    kilometraje = models.DecimalField(max_digits=10, decimal_places=2, help_text='Kilometraje al llegar a este punto')
    precio_combustible = models.DecimalField(max_digits=10, decimal_places=2, help_text='Precio por litro/galón de combustible')
    litros_cargados = models.DecimalField(max_digits=10, decimal_places=2, help_text='Litros de combustible cargados')
    kilometros_recorridos = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0, help_text='Kilómetros desde el punto anterior')
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0, help_text='Costo total de esta recarga')
    ubicacion = models.CharField(max_length=200, blank=True, help_text='Nombre o ubicación del punto de recarga')
    comprobante = models.FileField(upload_to='combustible/comprobantes/', blank=True, null=True, help_text='Comprobante de recarga')
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
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField()
    comprobante = models.FileField(upload_to='peajes/vouchers/', blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Peaje'
        verbose_name_plural = 'Peajes'

    def __str__(self):
        return f"Peaje en {self.lugar} - ${self.monto}"
