import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from viajes.models import Viaje
from costos.models import CostosViaje

viajes_ida = Viaje.objects.filter(es_ida_vuelta=True, tipo_trayecto='ida')
costos_ids = CostosViaje.objects.values_list('viaje_id', flat=True)
pendientes = viajes_ida.exclude(id__in=costos_ids)

print(f'Viajes de IDA pendientes de registrar costos: {pendientes.count()}')
print('=' * 60)

for v in pendientes[:5]:
    print(f'ID: {v.id}')
    print(f'  Ruta: {v.get_origen_display()} -> {v.get_destino_display()}')
    print(f'  Bus: {v.bus.placa}')
    print(f'  Conductor: {v.conductor.nombre} {v.conductor.apellido}')
    print(f'  Fecha: {v.fecha_salida}')
    if v.viaje_relacionado:
        print(f'  Viaje de vuelta: ID {v.viaje_relacionado.id}')
    print('-' * 60)
