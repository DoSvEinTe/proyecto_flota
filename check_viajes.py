"""Script para verificar el estado de los viajes"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from viajes.models import Viaje

viajes = Viaje.objects.all().order_by('id')
print('\n=== VIAJES EN BASE DE DATOS ===\n')
print(f"{'ID':<5} {'Bus':<10} {'Tipo':<10} {'Ida/Vuelta':<12} {'Relacionado':<12} {'Estado':<12}")
print('-' * 70)

for v in viajes:
    relacionado = str(v.viaje_relacionado.id) if v.viaje_relacionado else 'None'
    print(f"{v.id:<5} {v.bus.placa:<10} {v.tipo_trayecto:<10} {str(v.es_ida_vuelta):<12} {relacionado:<12} {v.estado:<12}")

print(f'\n📊 Total viajes: {viajes.count()}')
print(f'   - Tipo IDA: {viajes.filter(tipo_trayecto="ida").count()}')
print(f'   - Tipo VUELTA: {viajes.filter(tipo_trayecto="vuelta").count()}')
print(f'   - Tipo SIMPLE: {viajes.filter(tipo_trayecto="simple").count()}')
