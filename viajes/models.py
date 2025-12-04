from django.db import models
from core.models import Conductor, Lugar, Pasajero
from flota.models import Bus


class Viaje(models.Model):
    """
    Modelo para registrar viajes planificados de la flota.
    """
    ESTADO_VIAJE = [
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True, related_name='viajes')
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, related_name='viajes')
    lugar_origen = models.ForeignKey(Lugar, on_delete=models.PROTECT, related_name='viajes_origen', null=True, blank=True)
    lugar_destino = models.ForeignKey(Lugar, on_delete=models.PROTECT, related_name='viajes_destino', null=True, blank=True)
    
    # Información del origen (guardado directamente en el viaje)
    origen_nombre = models.CharField(max_length=150, blank=True)
    origen_ciudad = models.CharField(max_length=100, blank=True)
    origen_provincia = models.CharField(max_length=100, blank=True)
    origen_pais = models.CharField(max_length=100, default='Ecuador')
    latitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Información del destino (guardado directamente en el viaje)
    destino_nombre = models.CharField(max_length=150, blank=True)
    destino_ciudad = models.CharField(max_length=100, blank=True)
    destino_provincia = models.CharField(max_length=100, blank=True)
    destino_pais = models.CharField(max_length=100, default='Ecuador')
    latitud_destino = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_destino = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    fecha_salida = models.DateTimeField()
    fecha_llegada_estimada = models.DateTimeField()
    fecha_llegada_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_VIAJE, default='programado')
    pasajeros = models.ManyToManyField(Pasajero, through='ViajePasajero', blank=True, related_name='viajes')
    pasajeros_confirmados = models.IntegerField(default=0)
    distancia_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Distancia calculada en kilómetros')
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_salida']
        verbose_name = 'Viaje'
        verbose_name_plural = 'Viajes'

    def __str__(self):
        origen = self.origen_nombre or (self.lugar_origen.nombre if self.lugar_origen else 'Sin origen')
        destino = self.destino_nombre or (self.lugar_destino.nombre if self.lugar_destino else 'Sin destino')
        placa = self.bus.placa if self.bus else 'Sin bus'
        return f"{placa} - {origen} -> {destino} ({self.fecha_salida.date()})"
    
    def get_origen_display(self):
        """Retorna el nombre completo del origen"""
        if self.origen_nombre:
            return f"{self.origen_nombre}, {self.origen_ciudad}"
        elif self.lugar_origen:
            return f"{self.lugar_origen.nombre}, {self.lugar_origen.ciudad}"
        return "No especificado"
    
    def get_destino_display(self):
        """Retorna el nombre completo del destino"""
        if self.destino_nombre:
            return f"{self.destino_nombre}, {self.destino_ciudad}"
        elif self.lugar_destino:
            return f"{self.lugar_destino.nombre}, {self.lugar_destino.ciudad}"
        return "No especificado"
    
    def get_pasajeros_count(self):
        return self.pasajeros.count()
    
    def calcular_distancia_real(self):
        """
        Calcula la distancia real por carretera usando OSRM API.
        Retorna la distancia en kilómetros.
        """
        import requests
        
        # Obtener coordenadas
        lat_origen = self.latitud_origen
        lon_origen = self.longitud_origen
        lat_destino = self.latitud_destino
        lon_destino = self.longitud_destino
        
        # Verificar que tengamos coordenadas
        if not all([lat_origen, lon_origen, lat_destino, lon_destino]):
            return None
        
        try:
            # Usar OSRM API (gratuita)
            url = f"http://router.project-osrm.org/route/v1/driving/{lon_origen},{lat_origen};{lon_destino},{lat_destino}"
            params = {
                'overview': 'false',
                'geometries': 'geojson'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'Ok' and data.get('routes'):
                    # La distancia viene en metros, convertir a kilómetros
                    distancia_metros = data['routes'][0]['distance']
                    distancia_km = round(distancia_metros / 1000, 2)
                    
                    # Guardar la distancia calculada
                    self.distancia_km = distancia_km
                    self.save(update_fields=['distancia_km'])
                    
                    return distancia_km
        except Exception as e:
            print(f"Error al calcular distancia: {e}")
        
        return None


class ViajePasajero(models.Model):
    """
    Modelo intermedio para la relación entre Viaje y Pasajero.
    """
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    asiento = models.CharField(max_length=10, blank=True, null=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('viaje', 'pasajero')
        verbose_name = 'Pasajero en Viaje'
        verbose_name_plural = 'Pasajeros en Viajes'
    
    def __str__(self):
        return f"{self.pasajero.nombre_completo} - {self.viaje}"
