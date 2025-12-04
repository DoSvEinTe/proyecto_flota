"""
Script para migrar los datos de lugares desde ForeignKey a campos directos en viajes.
"""
from django.core.management.base import BaseCommand
from viajes.models import Viaje


class Command(BaseCommand):
    help = 'Migra los datos de lugares desde ForeignKey a campos directos en viajes'

    def handle(self, *args, **options):
        viajes = Viaje.objects.all()
        total = viajes.count()
        migrados = 0
        
        self.stdout.write(self.style.WARNING(f'Encontrados {total} viajes para migrar...'))
        
        for viaje in viajes:
            actualizado = False
            
            # Migrar origen si existe y no está ya migrado
            if viaje.lugar_origen and not viaje.origen_nombre:
                viaje.origen_nombre = viaje.lugar_origen.nombre
                viaje.origen_ciudad = viaje.lugar_origen.ciudad
                viaje.origen_provincia = viaje.lugar_origen.provincia
                viaje.origen_pais = viaje.lugar_origen.pais
                if viaje.lugar_origen.latitud:
                    viaje.latitud_origen = viaje.lugar_origen.latitud
                    viaje.longitud_origen = viaje.lugar_origen.longitud
                actualizado = True
            
            # Migrar destino si existe y no está ya migrado
            if viaje.lugar_destino and not viaje.destino_nombre:
                viaje.destino_nombre = viaje.lugar_destino.nombre
                viaje.destino_ciudad = viaje.lugar_destino.ciudad
                viaje.destino_provincia = viaje.lugar_destino.provincia
                viaje.destino_pais = viaje.lugar_destino.pais
                if viaje.lugar_destino.latitud:
                    viaje.latitud_destino = viaje.lugar_destino.latitud
                    viaje.longitud_destino = viaje.lugar_destino.longitud
                actualizado = True
            
            if actualizado:
                viaje.save()
                migrados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Viaje #{viaje.id} migrado: {viaje.get_origen_display()} → {viaje.get_destino_display()}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Migración completada: {migrados} de {total} viajes migrados')
        )
