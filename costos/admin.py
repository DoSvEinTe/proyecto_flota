from django.contrib import admin
from .models import CostosViaje, Peaje, PuntoRecarga


class PuntoRecargaInline(admin.TabularInline):
    model = PuntoRecarga
    extra = 1
    fields = ('orden', 'kilometraje', 'litros_cargados', 'precio_combustible', 'ubicacion', 'kilometros_recorridos', 'costo_total')
    readonly_fields = ('kilometros_recorridos', 'costo_total')


@admin.register(CostosViaje)
class CostosViajeAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'combustible', 'peajes', 'costo_total', 'ganancia_neta', 'num_puntos_recarga')
    list_filter = ('creado_en',)
    search_fields = ('viaje__bus__placa',)
    inlines = [PuntoRecargaInline]
    fieldsets = (
        ('Viaje', {
            'fields': ('viaje',)
        }),
        ('Desglose de Costos', {
            'fields': ('combustible', 'mantenimiento', 'peajes', 'otros_costos')
        }),
        ('Totales', {
            'fields': ('costo_total', 'ganancia_neta')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
    )
    readonly_fields = ('combustible', 'costo_total', 'creado_en', 'actualizado_en')

    def num_puntos_recarga(self, obj):
        return obj.puntos_recarga.count()
    num_puntos_recarga.short_description = 'Puntos Recarga'


@admin.register(PuntoRecarga)
class PuntoRecargaAdmin(admin.ModelAdmin):
    list_display = ('costos_viaje', 'orden', 'ubicacion', 'kilometraje', 'kilometros_recorridos', 'litros_cargados', 'precio_combustible', 'costo_total')
    list_filter = ('creado_en',)
    search_fields = ('costos_viaje__viaje__bus__placa', 'ubicacion')
    readonly_fields = ('kilometros_recorridos', 'costo_total', 'creado_en')
    fieldsets = (
        ('Información del Punto', {
            'fields': ('costos_viaje', 'orden', 'ubicacion')
        }),
        ('Datos de Recarga', {
            'fields': ('kilometraje', 'kilometros_recorridos', 'litros_cargados', 'precio_combustible', 'costo_total')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
    )


@admin.register(Peaje)
class PeajeAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'lugar', 'monto', 'fecha_pago', 'comprobante')
    list_filter = ('fecha_pago',)
    search_fields = ('viaje__bus__placa', 'lugar')
    fieldsets = (
        ('Información del Peaje', {
            'fields': ('viaje', 'lugar', 'monto')
        }),
        ('Registro', {
            'fields': ('fecha_pago', 'comprobante')
        }),
    )
