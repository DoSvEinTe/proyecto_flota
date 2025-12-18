from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Bus(models.Model):
    """
    Modelo para registrar buses de la flota.
    """
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('inactivo', 'Inactivo'),
    ]
    
    placa = models.CharField(max_length=20, unique=True)  # SE MANTIENE PLACA
    marca = models.CharField(max_length=50)  # Campo obligatorio
    modelo = models.CharField(max_length=100)
    año_fabricacion = models.IntegerField()
    capacidad_pasajeros = models.IntegerField()
    kilometraje_ingreso = models.IntegerField(default=0, help_text='Kilometraje cuando ingresó a la flota')
    numero_chasis = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Opcional
    numero_motor = models.CharField(max_length=30, unique=True, blank=True, null=True)  # Opcional
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    fecha_adquisicion = models.DateField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['placa']  # SE MANTIENE ORDEN POR PLACA
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'

    def __str__(self):
        return f"{self.placa} - {self.modelo}"  # SE MANTIENE PLACA EN REPRESENTACIÓN
    
    def clean(self):
        """Validar que la capacidad de pasajeros no exceda 70 y que la fecha sea válida"""
        if self.capacidad_pasajeros > 70:
            raise ValidationError({'capacidad_pasajeros': 'La capacidad máxima de pasajeros es 70.'})
        if self.capacidad_pasajeros < 1:
            raise ValidationError({'capacidad_pasajeros': 'La capacidad mínima de pasajeros es 1.'})
        
        # Validar que el año de fabricación no sea superior al año actual
        año_actual = date.today().year
        if self.año_fabricacion > año_actual:
            raise ValidationError({'año_fabricacion': f'El año de fabricación no puede ser superior a {año_actual}.'})
        
        # Validar que la fecha de adquisición no sea superior al día actual
        if self.fecha_adquisicion > date.today():
            raise ValidationError({'fecha_adquisicion': 'La fecha de adquisición no puede ser superior al día actual.'})


class DocumentoVehiculo(models.Model):
    """
    Modelo para registrar documentos del vehículo (SOAT, REC, etc).
    """
    TIPO_DOCUMENTO = [
        ('soat', 'SOAT'),
        ('rec', 'REC'),
        ('matricula', 'Matrícula'),
        ('revision', 'Revisión Técnica'),
        ('circulacion', 'Permiso de Circulación'),  # Nuevo tipo
        ('seguro', 'Seguro'),  # Nuevo tipo
        ('documentacion', 'Documentación Vehicular'),  # Nuevo tipo
        ('otro', 'Otro'),
    ]
    
    ESTADO_DOCUMENTO = [  # Nuevo campo de estado
        ('vigente', 'Vigente'),
        ('por_vencer', 'Por Vencer'),
        ('vencido', 'Vencido'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=20, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=50)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_DOCUMENTO, default='vigente')  # Nuevo campo
    archivo = models.FileField(upload_to='documentos_vehiculos/')
    observaciones = models.TextField(blank=True, null=True)  # Nuevo campo
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_vencimiento']
        verbose_name = 'Documento Vehículo'
        verbose_name_plural = 'Documentos Vehículos'

    def __str__(self):
        return f"{self.bus.placa} - {self.get_tipo_display()}"  # SE MANTIENE PLACA
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.fecha_emision > date.today():
            raise ValidationError({'fecha_emision': 'La fecha de emisión no puede ser superior al día actual.'})
        if self.fecha_vencimiento < self.fecha_emision:
            raise ValidationError({'fecha_vencimiento': 'La fecha de vencimiento no puede ser anterior a la fecha de emisión.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        self.actualizar_estado()
        super().save(*args, **kwargs)
    
    def actualizar_estado(self):
        """
        Actualiza automáticamente el estado del documento basado en la fecha de vencimiento
        """
        hoy = date.today()
        dias_para_vencer = (self.fecha_vencimiento - hoy).days
        
        if dias_para_vencer < 0:
            self.estado = 'vencido'
        elif dias_para_vencer <= 30:
            self.estado = 'por_vencer'
        else:
            self.estado = 'vigente'


class Mantenimiento(models.Model):
    """
    Modelo para registrar mantenimientos realizados en los buses.
    """
    TIPO_MANTENIMIENTO = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('predictivo', 'Predictivo'),  # Nuevo tipo
        ('mecanico', 'Mecánico'),
        ('electrico', 'Eléctrico'),
        ('otro', 'Otro'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='mantenimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_MANTENIMIENTO)
    descripcion = models.TextField()
    fecha_mantenimiento = models.DateField()
    kilometraje = models.IntegerField()
    costo = models.IntegerField(help_text='Costo del mantenimiento en pesos')
    proveedor = models.CharField(max_length=150, blank=True, null=True)  # Nuevo campo
    taller = models.CharField(max_length=150, blank=True)
    observaciones = models.TextField(blank=True)
    comprobante = models.FileField(upload_to='mantenimientos/comprobantes/', blank=True, null=True, help_text='Comprobante de mantenimiento')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_mantenimiento']
        verbose_name = 'Mantenimiento'
        verbose_name_plural = 'Mantenimientos'

    def __str__(self):
        placa = self.bus.placa if self.bus else 'Sin Bus'
        return f"{placa} - {self.get_tipo_display()} ({self.fecha_mantenimiento})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Validar que la fecha de mantenimiento no sea superior al día actual
        if self.fecha_mantenimiento > date.today():
            raise ValidationError({'fecha_mantenimiento': 'La fecha de mantenimiento no puede ser superior al día actual.'})
        
        # Validar que el kilometraje sea mayor o igual al kilometraje_ingreso del bus
        # Solo si el bus existe
        try:
            if self.bus and self.kilometraje < self.bus.kilometraje_ingreso:
                raise ValidationError({'kilometraje': f'El kilometraje debe ser mayor o igual a {self.bus.kilometraje_ingreso} km (kilometraje de ingreso del bus).'})
        except:
            # Si hay algún error accediendo al bus, simplemente ignorar
            pass
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)